import pandas as pd
from pyhwpx import Hwp
from datetime import datetime
import os
import time

UPLOAD_DIRECTORY = "./uploaded_files"
PROCESS_DIRECTORY = "./processed_files"

class HwpRecommender:
    def __init__(self, excel_path="target.xlsx", hwp_path="", file_name="None"):
        self.excel_path = excel_path
        self.hwp_path = hwp_path
        self.df = None
        self.hwp = None
        self.file_name = file_name.replace(".hwp", "")

    def read_excel(self):
        # Excel 파일에서 추천 용어 읽기
        self.df = pd.read_excel(self.excel_path, engine='openpyxl')

    def load_hwp(self):
        # HWP 파일 로드
        self.hwp = Hwp()
        self.hwp.open(self.hwp_path)

    def replace_terms(self):
        # HWP 내용 읽기
        content = self.hwp.get_text_file()
        
        # 용어 찾아서 추천 용어로 교체
        for idx, val in enumerate(self.df.Target):
            count = content.count(val)
            for i in range(count):
                self.hwp.find(val, "Backward")
                act = self.hwp.create_action("CharShape")
                cs = act.CreateSet()
                act.GetDefault(cs)
                if cs.Item("UnderlineType"):
                    self.hwp.insert_memo(self.df.iloc[idx].Recommendation)

    def save_hwp(self, suffix):
        # 파일 저장 공통 로직
        date_folder = datetime.now().strftime("%Y%m%d")
        final_directory = os.path.join(PROCESS_DIRECTORY, date_folder)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        new_file_name = f"{self.file_name}_{suffix}.hwp"
        file_path = os.path.join(final_directory, new_file_name)
        self.hwp.save_as(file_path)
        time.sleep(0.5)  # 파일 저장 대기
        return new_file_name

    def close_hwp(self):
        self.hwp.FileQuit()

    def process_hwp(self, type="memo"):
        # 공통 프로세스 실행
        self.read_excel()
        self.load_hwp()
        self.replace_terms()
        if type == "memo":
            file_name = self.save_hwp("memo")
        else:
            file_name = self.save_hwp("cor")
        self.close_hwp()
        return file_name

# 사용 예
recommender = HwpRecommender("target.xlsx", "240221_1613.hwp", "240221_1613.hwp")
memo_file_name = recommender.process_hwp("memo")
cor_file_name = recommender.process_hwp("cor")
