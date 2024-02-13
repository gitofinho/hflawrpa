import pandas as pd
from pyhwpx import Hwp
from datetime import datetime

# read recommendation terms file 
df = pd.read_excel('target.xlsx', engine='openpyxl')

# load hwp
hwp = Hwp()
hwp.open("example.hwp")
content = hwp.get_text_file()

# find term and replace with reccomendation
for idx, val in enumerate(df.Target):
    count = content.count(val)
    for i in range(count):
        hwp.find(val, "Backward")
        act = hwp.create_action("CharShape")
        cs = act.CreateSet()
        act.GetDefault(cs)
        if cs.Item("UnderlineType"):
            hwp.insert_memo(df.iloc[idx].Recommendation)

# hwp save as
current_time = datetime.now().strftime("%y%m%d%H%M%S")
hwp.save_as(f"./memo_revision_{current_time}.hwp")