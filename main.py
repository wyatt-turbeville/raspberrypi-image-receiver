from fastapi import FastAPI, File, UploadFile, Form
import datetime, os, shutil, sqlite3
from exif import Image

app = FastAPI()

@app.post('/save_image/')
async def recieve_upload_file(
    image: UploadFile = File(...),
    cameraID: int = Form(...),
    ):
    
    image.file.seek(0)
    meta_image = Image(image.file)
    img_datetime = datetime.datetime.strptime(meta_image.datetime_original, '%Y:%m:%d %H:%M:%S')

    target_dir = f"~/Pictures/plot_{cameraID}"
    full_dir = os.path.expanduser(target_dir)
    os.makedirs(full_dir, exist_ok=True)
    file_path = os.path.join(full_dir, image.filename)

    image.file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
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