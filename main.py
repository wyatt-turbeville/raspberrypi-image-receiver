from fastapi import FastAPI, File, UploadFile, Form
import datetime, os, shutil, sqlite3
from exif import Image

app = FastAPI()

upload_dirs = {
    1: "~/Pictures/plot1/",
    2: "~/Pictures/plot2/",
    3: "~/Pictures/plot3/",
    4: "~/Pictures/plot4/",
    5: "~/Pictures/plot5/",
    6: "~/Pictures/plot6/",
    7: "~/Pictures/plot7/",
    8: "~/Pictures/plot8/"
}

@app.post('/save_image/')
async def recieve_upload_file(
    image: UploadFile = File(...),
    cameraID: int = Form(...),
    ):

    target_dir = upload_dirs[cameraID]
    full_dir = os.path.expanduser(target_dir)
    os.makedirs(full_dir, exist_ok=True)
    file_path = os.path.join(full_dir, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    with open(file_path, 'rb') as image_file:
        meta_image = Image(image_file)

    exif_datetime_original = meta_image.datetime_original
    img_datetime = datetime.datetime.strptime(exif_datetime_original, '%Y:%m:%d %H:%M:%S')

    try:
        with sqlite3.connect("my.db") as conn:
            # interact with database
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
        return { "status": "Failed: Database Error"}
    
    return {
        "status": "success",
        "cameraID": cameraID,
        "filename": image.filename,
        "datetime": img_datetime,
        "saved_path": file_path
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="100.76.229.28", port=8000, reload=True)