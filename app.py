import pythoncom
import streamlit as st
from HwpRecommend import HwpRecommender
from io import BytesIO
import requests

# FastAPI 서버 주소
FASTAPI_ENDPOINT = "http://localhost:8000"  
# COM 라이브러리 초기화
pythoncom.CoInitialize()

# Streamlit 세션 상태 초기화
if 'run_once' not in st.session_state:
    st.session_state['run_once'] = False

uploaded_files = st.file_uploader("Choose a HWP file-", accept_multiple_files=True, type=["hwp"])

for uploaded_file in uploaded_files:
    if uploaded_file is not None and not st.session_state['run_once']:
        with st.spinner('Wait for it...'):
            files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
            response = requests.post(f"{FASTAPI_ENDPOINT}/upload-hwp/", files=files)
            if response.status_code == 200:
                st.success("File uploaded successfully.")
                st.session_state['run_once'] = True  # run() 실행 플래그 설정
                st.success('Done!')
                try:
                    # FastAPI 서버에서 파일 내용을 가져오기
                    file_path = f"http://localhost:8000/download-hwp/{response.json()['filename']}"
                    download_filename = response.json()['filename']
                    response = requests.get(file_path)
                    if response.status_code == 200:
                        # 메모리에 파일 내용 저장
                        to_download = BytesIO(response.content)
                        to_download.seek(0)
                        # Streamlit의 다운로드 버튼에 파일 내용 전달
                        st.download_button(label="Download Result",
                                        data=to_download,
                                        file_name=download_filename,  # 파일 이름을 문자열로 지정
                                        mime="application/octet-stream")
                    else:
                        st.error("Failed to download file.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Failed to upload file.")

# COM 라이브러리 정리
pythoncom.CoUninitialize()
