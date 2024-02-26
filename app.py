import streamlit as st
import requests
import pythoncom

# FastAPI 서버 주소
FASTAPI_ENDPOINT = "http://localhost:8000"
# COM 라이브러리 초기화
pythoncom.CoInitialize()

st.set_page_config(page_title='HFDT-Platform' ,layout="wide",page_icon='🚀')
"## 🚀 HFRPA-LAW"
st.write("")
st.info("내규 제·개정 대상 전후대비표, 원문을 업로드 해주세요. 정비 대상 용어를 확인해줍니다.")

uploaded_files = st.file_uploader("Choose a HWP file-", accept_multiple_files=True, type=["hwp"])

# 파일 업로드 상태 관리를 위한 세션 상태 초기화
if 'uploaded_files_status' not in st.session_state:
    st.session_state['uploaded_files_status'] = {}

for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        # 파일별 처리 상태 확인 및 파일이 아직 처리되지 않았다면 처리 진행
        if not st.session_state['uploaded_files_status'].get(uploaded_file.name, False):
            with st.spinner('Processing...'):
                files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
                response = requests.post(f"{FASTAPI_ENDPOINT}/upload-hwp/", files=files)
                if response.status_code == 200:
                    # 파일 처리 상태 업데이트
                    st.session_state['uploaded_files_status'][uploaded_file.name] = True
                    
                    st.success(f"{response.json()['memo_filename']} File uploaded and processed successfully.")
                    download_text1 = f"Download Memo Version File"
                    download_url1 = f"{FASTAPI_ENDPOINT}/download-hwp/{response.json()['memo_filename']}"
                    download_text2 = f"Download Correction Version File"
                    download_url2 = f"{FASTAPI_ENDPOINT}/download-hwp/{response.json()['cor_filename']}"
                    st.markdown(f'''
                        <div>
                            <a href="{download_url1}" download style="color: Black; background-color: #E0E0E0; padding: 10px; border-radius: 5px; text-decoration: none; display: inline-block; margin-right: 10px;">{download_text1}</a>
                            <a href="{download_url2}" download style="color: Black; background-color: #E0E0E0; padding: 10px; border-radius: 5px; text-decoration: none; display: inline-block;">{download_text2}</a>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    # 파일 처리 실패 시 상태 업데이트는 필요 없음
                    st.error("Failed to upload file.")


# COM 라이브러리 정리
pythoncom.CoUninitialize()
