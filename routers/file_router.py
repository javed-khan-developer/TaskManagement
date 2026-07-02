from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import BackgroundTasks
import os

router = APIRouter()

@router.post("/upload")
async def uploadFile(backgroundTask: BackgroundTasks, file: UploadFile):
    contents= await file.read()
    filepath= os.path.join("uploads",file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    backgroundTask.add_task(process_file,file.filename)

    return {
        "filename": file.filename,
        "message": "Uploaded Successfully",
        "size": len(contents)
        }



def process_file(filename: str):

    print(f"Processing {filename}")