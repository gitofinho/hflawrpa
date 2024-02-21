# app.py
import streamlit as st
from io import BytesIO
import requests

FASTAPI_ENDPOINT = "http://localhost:8000"  # FastAPI 서버 주소

st.title("HWP File Upload and Download")

# 파일 업로드 섹션
uploaded_file = st.file_uploader("Choose a HWP file", type=["hwp"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
    response = requests.post(f"{FASTAPI_ENDPOINT}/upload-hwp/", files=files)
    if response.status_code == 200:
        st.success("File uploaded successfully.")
    else:
        st.error("Failed to upload file.")

# 파일 다운로드 섹션
file_name = st.text_input("Enter the name of the file you wish to download", "")
if st.button("Download HWP File"):
    if file_name:
        try:
            # FastAPI 서버에서 파일 내용을 가져오기
            file_path = f"http://localhost:8000/download-hwp/{file_name}"
            response = requests.get(file_path)
            if response.status_code == 200:
                # 메모리에 파일 내용 저장
                to_download = BytesIO(response.content)
                to_download.seek(0)
                # Streamlit의 다운로드 버튼에 파일 내용 전달
                st.download_button(label="Download file",
                    data=to_download,
                    file_name=file_name,
                    mime="application/octet-stream")
            else:
                st.error("Failed to download file.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a file name.")
