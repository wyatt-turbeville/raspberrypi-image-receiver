from fastapi import FastAPI, File, UploadFile, Form, Request
import datetime, os, shutil, connection
from exif import Image
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

    connection.insertPictureData(cameraID, img_datetime, file_path, image.filename)
    
    return {
        "status": "success",
        "cameraID": cameraID,
        "filename": image.filename,
        "datetime": img_datetime,
        "saved_path": file_path
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    camera_ids = connection.countCameras()

    context = {
        "request": request, 
        "camera_ids": camera_ids
    }
    
    return templates.TemplateResponse(request=request, name="index.html", context=context)

if __name__ == "__main__":
    import uvicorn

    connection.initTables()
    connection.initRows()

    uvicorn.run("main:app", host="100.76.229.28", port=8000, reload=True)