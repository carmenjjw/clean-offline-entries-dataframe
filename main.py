import pandas as pd
import os
from datetime import datetime as dt

# find the xlsx file based on the current directory
script_dir =os.path.dirname(os.path.realpath(__file__))

def get_xlsx_path(xlsx_file_name):
    xlsx_dir = os.path.join(script_dir, xlsx_file_name)
    return xlsx_dir


# clean the xlsx files per country
def get_clean_entry(country):
    
    xlsx_dir = get_xlsx_path(f"raw_{country}.xlsx")
    xlsx = pd.read_excel(xlsx_dir)

    xlsx = xlsx.dropna(how="all")
    xlsx_clean = xlsx.iloc[1:, 1].to_frame()
    xlsx_clean.columns = ["Date"]

    date = xlsx_clean["Date"]
    xlsx_clean["Dedup Date"] = pd.to_datetime(date, format = "%Y-%m-%d %H:%M:%S.%f", errors='coerce').dt.strftime("%Y%m%d")

    result = xlsx_clean.groupby("Dedup Date").size().reset_index(name="Count")
    result.to_csv(os.path.join(script_dir, f"result_{country}.csv"), index = False)

country = ["SE", "NO", "FI", "DK"]

for item in country:
    try:
        get_clean_entry(item)
    except Exception as error:
        print(error)



