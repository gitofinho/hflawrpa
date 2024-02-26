# server.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from urllib.parse import unquote
from HwpRecommend import HwpRecommender
import os
from datetime import datetime
import time

app = FastAPI()

UPLOAD_DIRECTORY = "./uploaded_files"
PROCESS_DIRECTORY = "./processed_files"

@app.post("/upload-hwp/")
async def upload_hwp(file: UploadFile = File(...)):
    # 현재 날짜 기반으로 폴더 이름 생성
    date_folder = datetime.now().strftime("%Y%m%d")
    # 최종 경로에 날짜 폴더 포함
    temp_directory = os.path.join(UPLOAD_DIRECTORY, date_folder)
    file_path = os.path.join(temp_directory, file.filename)
    os.makedirs(temp_directory, exist_ok=True)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read()) 
        try:
            recommender = HwpRecommender(hwp_path=file_path, file_name=file.filename)
            memo_file_name = recommender.process_hwp("memo")
            time.sleep(0.5)
            cor_file_name = recommender.process_hwp("cor")

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=f"Failed to process HWP file: {e}")
        return {"memo_filename": memo_file_name, "cor_filename": cor_file_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")


@app.get("/download-hwp/{file_name}")
async def download_hwp(file_name: str):
    try:
        # 현재 날짜 기반으로 폴더 이름 생성
        date_folder = datetime.now().strftime("%Y%m%d")
        # 최종 경로에 날짜 폴더 포함
        download_directory = os.path.join(PROCESS_DIRECTORY, date_folder)
        decoded_file_name = unquote(file_name)
        file_path = os.path.join(download_directory, decoded_file_name)
        os.makedirs(PROCESS_DIRECTORY, exist_ok=True)
        if os.path.exists(file_path):
            return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="File not found")