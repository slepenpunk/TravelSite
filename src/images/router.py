import shutil

from fastapi import APIRouter, UploadFile

from tasks.tasks import process_pic

image_router = APIRouter(prefix="/images", tags=["Upload images"])


@image_router.post("/upload")
async def load_picture(name: str, file: UploadFile):
    celery_path = f"static/images/{name}.webp"
    open_path = f"src/static/images/{name}.webp"
    with open(open_path, "wb+") as picture:
        shutil.copyfileobj(file.file, picture)
    process_pic.delay(celery_path)
