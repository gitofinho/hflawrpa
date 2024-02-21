# server.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from HwpRecommend import HwpRecommender
import os

app = FastAPI()

UPLOAD_DIRECTORY = "./uploaded_files"

@app.post("/upload-hwp/")
async def upload_hwp(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
            # 내규 제개정 호출
            recommender = HwpRecommender(hwp_path=file_path)
            modified_hwp_path = recommender.run()
        return {"filename": modified_hwp_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

@app.get("/download-hwp/{file_name}")
async def download_hwp(file_name: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
    raise HTTPException(status_code=404, detail="File not found")
