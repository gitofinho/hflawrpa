import pythoncom
import streamlit as st
from HwpRecommend import HwpRecommender
from io import BytesIO
import requests

# FastAPI 서버 주소
FASTAPI_ENDPOINT = "http://localhost:8000"
# COM 라이브러리 초기화
pythoncom.CoInitialize()

uploaded_files = st.file_uploader("Choose a HWP file-", accept_multiple_files=True, type=["hwp"])

# 파일 업로드 상태 관리를 위한 세션 상태 초기화
if 'uploaded_files_status' not in st.session_state:
    st.session_state['uploaded_files_status'] = {}

for uploaded_file in uploaded_files:
    # 각 파일별 처리 상태 확인
    if uploaded_file is not None and not st.session_state['uploaded_files_status'].get(uploaded_file.name, False):
        with st.spinner('Processing...'):
            files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
            response = requests.post(f"{FASTAPI_ENDPOINT}/upload-hwp/", files=files)
            # 파일 처리 후 다운로드 URL을 생성
            if response.status_code == 200:
                st.success("File uploaded successfully.")
                download_text1 = "Download Memo Version File"
                download_url1 = f"{FASTAPI_ENDPOINT}/download-hwp/{response.json()['memo_filename']}"
                download_text2 = "Download Correction Version File"
                download_url2 = f"{FASTAPI_ENDPOINT}/download-hwp/{response.json()['cor_filename']}"
                # 두 다운로드 링크를 인라인으로 배치
                st.markdown(f'''
                    <div>
                        <a href="{download_url1}" download style="color: Black; background-color: #E0E0E0; padding: 10px; border-radius: 5px; text-decoration: none; display: inline-block; margin-right: 10px;">{download_text1}</a>
                        <a href="{download_url2}" download style="color: Black; background-color: #E0E0E0; padding: 10px; border-radius: 5px; text-decoration: none; display: inline-block;">{download_text2}</a>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.error("Failed to upload file.")

# COM 라이브러리 정리
pythoncom.CoUninitialize()
