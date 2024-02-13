# import pythoncom
import streamlit as st
from HwpRecommend import HwpRecommender

# COM 라이브러리 초기화
# pythoncom.CoInitialize()

# Streamlit 세션 상태 초기화
if 'run_once' not in st.session_state:
    st.session_state['run_once'] = False

uploaded_files = st.file_uploader("Choose a HWP file-", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    if uploaded_file is not None and not st.session_state['run_once']:
        with open("temp_file.hwp", "wb") as f:
            f.write(uploaded_file.getbuffer())  # 업로드된 파일을 임시 파일로 저장
        temp_hwp_path = "temp_file.hwp"
        st.write("filename:", uploaded_file.name)
        
        with st.spinner('Wait for it...'):
            recommender = HwpRecommender(hwp_path=temp_hwp_path)
            modified_hwp_path = recommender.run()
            st.session_state['run_once'] = True  # run() 실행 플래그 설정
        st.success('Done!')

        with open(modified_hwp_path, 'rb') as file:
            btn = st.download_button(
                    label="Download Result",
                    data=file,
                    file_name=modified_hwp_path,
                )

# COM 라이브러리 정리
# pythoncom.CoUninitialize()
