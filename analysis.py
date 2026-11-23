import cv2, connection
import numpy as np
import onnxruntime as ort

def load_model(onnx_path="turf_model.onnx"):
    ort_session = ort.InferenceSession(onnx_path)
    return ort_session

def predict_mask(ort_session, native_image):
    """
    Feeds the native image into the ONNX model at a reduced grid size,
    then upscales the resulting binary mask back to the native high-res dimensions.
    """
    input_size = (384, 384)
    native_h, native_w = native_image.shape[:2]
    
    resized_img = cv2.resize(native_image, input_size)
    
    img_blob = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img_blob = np.transpose(img_blob, (2, 0, 1))
    img_blob = np.expand_dims(img_blob, axis=0)
    
    ort_inputs = ort_session.get_inputs()[0].name
    ort_outputs = ort_session.run(None, {ort_inputs: img_blob})
    prediction_logits = ort_outputs[0].squeeze()
    
    prediction_mask = 1.0 / (1.0 + np.exp(-prediction_logits))
    binary_mask = (prediction_mask > 0.5).astype(np.uint8)
    
    binary_mask = cv2.resize(binary_mask, (native_w, native_h), interpolation=cv2.INTER_NEAREST)
    
    return binary_mask

def analyze_turf(native_image, binary_mask):

    mask_3ch = np.stack([binary_mask] * 3, axis=-1)
    
    isolated_grass = native_image * mask_3ch
    
    total_tray_pixels = isolated_grass[binary_mask == 1].shape[0]
    
    if total_tray_pixels == 0:
        return None

    green_cover = green_cover_helper(isolated_grass, binary_mask, total_tray_pixels)
    excess_green = excess_green_helper(isolated_grass, binary_mask, total_tray_pixels)
    dgci = dgci_helper(isolated_grass, binary_mask, total_tray_pixels)

    return {
        "green cover": green_cover, 
        "excess green": excess_green,
        "dgci": dgci
        }

def green_cover_helper(isolated_grass, binary_mask, total_tray_pixels):

    isolated_hsv = cv2.cvtColor(isolated_grass, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([35, 25, 0])
    upper_hsv = np.array([85, 255, 255])

    hsv_mask = cv2.inRange(isolated_hsv, lower_hsv, upper_hsv)

    valid_green_mask = (binary_mask == 1) & (hsv_mask > 0)
    green_pixels_count = np.sum(valid_green_mask)

    """# Temp bullshit !!!!
    overlay_bgr = isolated_grass.copy()
    highlight_color = np.array([0, 255, 0], dtype=np.float32)  # bright green in BGR
    alpha = 0.5  # 0.0 = original pixel, 1.0 = solid highlight color

    if np.any(valid_green_mask):
        blended = (
            (1.0 - alpha) * overlay_bgr[valid_green_mask].astype(np.float32)
            + alpha * highlight_color
        )
        overlay_bgr[valid_green_mask] = np.clip(blended, 0, 255).astype(np.uint8)

    cv2.imwrite("gc_comparison_overlay.jpg", overlay_bgr)
    # Temp bullshit !!!! """
    
    return float(round((green_pixels_count / total_tray_pixels) * 100.0, 2))

def excess_green_helper(isolated_grass, binary_mask, total_tray_pixels):

    roi = binary_mask == 1
    rgb = isolated_grass.astype(np.float32)
    b = rgb[..., 0]
    g = rgb[..., 1]
    r = rgb[..., 2]

    exg = 2.0 * g - r - b
    exr = 1.4 * r - g

    exg_minus_exr = np.zeros(binary_mask.shape, dtype=np.float32)
    exg_minus_exr[roi] = exg[roi] - exr[roi]

    comparison_mask = np.zeros(binary_mask.shape, dtype=np.uint8)
    comparison_mask[roi & (exg_minus_exr > 0)] = 1

    green_pixels_count = np.sum(comparison_mask[roi])

    """# Temp bullshit !!!!
    overlay_bgr = isolated_grass.copy()
    match = comparison_mask == 1
    highlight_color = np.array([0, 255, 0], dtype=np.float32)
    alpha = 0.5  # 0.0 = original pixel, 1.0 = solid highlight color
    blended = (
        (1.0 - alpha) * overlay_bgr[match].astype(np.float32)
        + alpha * highlight_color
    )
    overlay_bgr[match] = np.clip(blended, 0, 255).astype(np.uint8)
    cv2.imwrite("eg_comparison_overlay.jpg", overlay_bgr)
    # Temp bullshit !!!!"""

    return float(round((green_pixels_count / total_tray_pixels) * 100.0, 2))

def dgci_helper(isolated_grass, binary_mask, total_tray_pixels):

    threshold = 0.3
    roi = binary_mask == 1
    isolated_hsv = cv2.cvtColor(isolated_grass, cv2.COLOR_BGR2HSV).astype(np.float32)

    h = isolated_hsv[..., 0] * 2.0
    s = isolated_hsv[..., 1] / 255.0
    v = isolated_hsv[..., 2] / 255.0

    dgci_raw = ((h - 60.0) / 60.0 + (1.0 - s) + (1.0 - v)) / 3.0

    dgci_mask = np.zeros(binary_mask.shape, dtype=np.float32)
    dgci_mask[roi] = dgci_raw[roi]

    comparison_mask = np.zeros(binary_mask.shape, dtype=np.uint8)
    comparison_mask[roi & (dgci_mask > threshold)] = 1

    green_pixels_count = np.sum(comparison_mask[roi])

    """# Temp bullshit !!!!
    overlay_bgr = isolated_grass.copy()
    match = comparison_mask == 1
    highlight_color = np.array([0, 255, 0], dtype=np.float32)
    alpha = 0.5  # 0.0 = original pixel, 1.0 = solid highlight color
    blended = (
        (1.0 - alpha) * overlay_bgr[match].astype(np.float32)
        + alpha * highlight_color
    )
    overlay_bgr[match] = np.clip(blended, 0, 255).astype(np.uint8)
    cv2.imwrite("dgci_comparison_overlay.jpg", overlay_bgr)
    # Temp bullshit !!!!"""

    return float(round((green_pixels_count / total_tray_pixels) * 100.0, 2))

def analyze_images(ort_session):

    file_paths = connection.tenPull()

    for image_id, path in file_paths:
        image = cv2.imread(path)
        mask = predict_mask(ort_session, image)
        values = analyze_turf(image, mask)

        for test in values:
            connection.insertAnalysisData(test, values[test], image_id)

if __name__ == "__main__":
    ort_session = load_model("turf_model.onnx")

    analyze_images(ort_session)