import pandas as pd
from pyhwpx import Hwp
from datetime import datetime
import os
import pythoncom

UPLOAD_DIRECTORY = "./uploaded_files"
PROCESS_DIRECTORY = "./processed_files"

class HwpRecommender:
    def __init__(self, excel_path="target.xlsx", hwp_path="", file_name="None"):
        self.excel_path = excel_path
        self.hwp_path = hwp_path
        self.df = pd.read_excel(self.excel_path, engine='openpyxl')
        self.file_name = file_name
        # 파일 이름 확장자 제거
        self.base_file_name = self.file_name.replace(".hwp", "")

    def load_hwp(self):
        """HWP 파일 로드 및 리소스 관리 개선"""
        try:
            # COM 라이브러리 초기화
            pythoncom.CoInitialize()
            self.hwp = Hwp()
            self.hwp.open(self.hwp_path)
        except Exception as e:
            print(f"Error loading HWP file: {e}")
            # 여기서 오류 발생 시, COM 라이브러리 정리를 확실하게 하기 위해 finally 블록 사용
        finally:
            # COM 라이브러리 정리
            pythoncom.CoUninitialize()

    def replace_terms(self):
        """용어 교체 로직"""
        content = self.hwp.get_text_file()
        
        for idx, val in self.df['Target'].items():
            count = content.count(val)
            for _ in range(count):
                self.hwp.find(val, "Backward")
                act = self.hwp.create_action("CharShape")
                cs = act.CreateSet()
                act.GetDefault(cs)
                if cs.Item("UnderlineType"):
                    self.hwp.insert_memo(self.df.iloc[idx].Recommendation)

    def save_hwp(self, suffix):
        """파일 저장 로직 개선"""
        date_folder = datetime.now().strftime("%Y%m%d")
        final_directory = os.path.join(PROCESS_DIRECTORY, date_folder)
        os.makedirs(final_directory, exist_ok=True)
        new_file_name = f"{self.base_file_name}_{suffix}.hwp"
        file_path = os.path.join(final_directory, new_file_name)
        self.hwp.save_as(file_path)
        return new_file_name

    def process_file(self, suffix):
        """공통 파일 처리 로직"""
        if self.load_hwp():
            self.replace_terms()
            saved_file_name = self.save_hwp(suffix)
            self.hwp.FileQuit()
            return saved_file_name
        else:
            return None

    def memo_run(self):
        """메모 삽입 파일 처리"""
        return self.process_file("memo")

    def cor_run(self):
        """교정 사항 반영 파일 처리"""
        return self.process_file("cor")
