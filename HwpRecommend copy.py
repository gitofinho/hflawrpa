import pandas as pd
from pyhwpx import Hwp
from datetime import datetime
import os

UPLOAD_DIRECTORY = "./uploaded_files"
PROCESS_DIRECTORY = "./processed_files"

class HwpRecommender:
    def __init__(self, excel_path = "target.xlsx", hwp_path="", file_name="None"):
        self.excel_path = excel_path
        self.hwp_path = hwp_path
        self.df = None
        self.hwp = None
        self.new_file_path = ""
        self.file_name = file_name

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

    def save_hwp(self):
        current_time = datetime.now().strftime("%y%m%d%H%M%S")
        new_file_name = f"./memo_revision_{current_time}.hwp"
        file_path = os.path.join(PROCESS_DIRECTORY, new_file_name)
        self.hwp.save_as(file_path)
        return new_file_name  # 수정된 파일의 경로를 반환

    def save_hwp(self):
        # 현재 날짜 기반으로 폴더 이름 생성 (예: '20230220')
        date_folder = datetime.now().strftime("%Y%m%d")
        # 최종 경로에 날짜 폴더 포함
        final_directory = os.path.join(PROCESS_DIRECTORY, date_folder)
        
        # 해당 날짜의 폴더가 없으면 생성
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        
        # 파일 이름 생성
        current_time = datetime.now().strftime("%y%m%d%H%M%S")
        new_file_name = f"{self.file_name}_memo.hwp"
        # 파일 전체 경로 설정
        file_path = os.path.join(final_directory, new_file_name)
        
        # 파일 저장
        self.hwp.save_as(file_path)
        
        # 저장된 파일의 경로 반환
        return file_path

    def down(self):
        self.hwp.FileQuit()

    # 프로세스 실행
    def run(self):
        self.read_excel()
        self.load_hwp()
        self.replace_terms()
        self.new_file_path = self.save_hwp()
        self.down()
        return self.new_file_path

# 사용 예
excel_path = 'target.xlsx'
hwp_path = '240219_19_test.hwp'
file_name
recommender = HwpRecommender(excel_path, hwp_path, file_name)
path = recommender.run()
print(path)



import pandas as pd
from pyhwpx import Hwp
from datetime import datetime
import os

UPLOAD_DIRECTORY = "./uploaded_files"
PROCESS_DIRECTORY = "./processed_files"

class HwpRecommender:
    def __init__(self, excel_path = "target.xlsx", hwp_path=""):
        self.excel_path = excel_path
        self.hwp_path = hwp_path
        self.df = None
        self.hwp = None
        self.new_file_path = ""

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

    def save_hwp(self):
        current_time = datetime.now().strftime("%y%m%d%H%M%S")
        new_file_name = f"./memo_revision_{current_time}.hwp"
        file_path = os.path.join(PROCESS_DIRECTORY, new_file_name)
        self.hwp.save_as(file_path)
        return new_file_name  # 수정된 파일의 경로를 반환

    def down(self):
        self.hwp.FileQuit()

    # 프로세스 실행
    def run(self):
        self.read_excel()
        self.load_hwp()
        self.replace_terms()
        self.new_file_path = self.save_hwp()
        self.down()
        return self.new_file_path

# # 사용 예
# excel_path = 'target.xlsx'
# hwp_path = '240219_19_test.hwp'
# recommender = HwpRecommender(excel_path, hwp_path)
# path = recommender.run()
# print(path)