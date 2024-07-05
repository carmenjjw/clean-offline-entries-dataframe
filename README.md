## Backstory
I received an offline data set from a client one day. They receive entries from the web and would like to visualise it together with some other online data sets to get a single-view comparison in Looker Studio. 

They have exported the raw files from their backend and will send the updated data over continuously at the end of each month. 

Before integrating this offline data set into Looker Studio, it needs to be cleaned up.

## Raw data

There are 4 files in total, one for rach country (denonymized):
- [raw_SE.xlsx](https://github.com/user-attachments/files/16106886/raw_SE.xlsx)
- [raw_NO.xlsx](https://github.com/user-attachments/files/16106884/raw_NO.xlsx)
- [raw_FI.xlsx](https://github.com/user-attachments/files/16106881/raw_FI.xlsx)
- [raw_DK.xlsx](https://github.com/user-attachments/files/16106880/raw_DK.xlsx)

The content of each file is more or less the same. The **Date** column contains the timestamp of each entry. Each row represents an entry submitted by the users. 
Each file contains about 10 000 - 20 000 rows.

![Screenshot 2024-07-05 at 10 03 31](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/0a2352fa-f831-4fb7-b44d-44b6984f860e)

Now, the question is: **How many entires were submitted per day?**

This is a seemingly a straight forward question. But we’ve got a few challenges here:

- A varied amount of entried were generated per date. 
- There are more than 10 000 rows per file.
- There are empty rows and excessive columns (All we need is just the Date column).
- There are 4 files in total for 4 countries. There some repetitive work to be done.

## Expected results

To visualise a time series chart, the expected outcome needs to contain a minimun of two columns: **Date** and **Entries**.

![Screenshot 2024-07-05 at 10 41 52](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/1acf7d16-93ff-484f-8a4c-1b05cfeb8702)

Since I expect to receive the updated raw files every month, it would be optimal to develop a solution that is scalable, efficient, and as automated as possible. The solution in main.py allows for running a few command lines whenever a new file arrives, generating the results in clean CSVs in the same directory.

The great thing about Python is that it can digest large amount of data, and achieve reading raw files, cleaning, generate the output in just one code block. 
Enough with all the clicking, saving, deleting in Excel or Google Sheet! 


![Screenshot 2024-07-05 at 10 46 18](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/99bc9bce-1898-4e08-85c4-e57af49c4f67)

## Solution: Pandas DataFrame

(The code can also be found in main.py)


```
# dependencies
import pandas as pd
import os
from datetime import datetime as dt
```

```
# find the xlsx file based on the current directory
script_dir =os.path.dirname(os.path.realpath(__file__))

def get_xlsx_path(xlsx_file_name):
    xlsx_dir = os.path.join(script_dir, xlsx_file_name)
    return xlsx_dir
```

```
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
```

```
# make a loop that repete the process for the other files
country = ["SE", "NO", "FI", "DK"]

for item in country:
    try:
        get_clean_entry(item)
    except Exception as error:
        print(error)
```

## Other methods

Of course, there are multiples ways of solving this. These are what I have tried:

1. Clean the data directly in Looker Studio (Possible but not ideal. Excessive processing downstream slows the dashboard down).
2. Google sheet functions (This was where I turned to at first. Not sustainable and crashes quite often due to a high number of rows. One Google Sheet can contain max 100 0000 rows, not sustainable in the long run).
3. BigWuery + SQL (should also be a quick option! Unofrtunately the raw data is not clean enough, encountered errors with the schema).
4. ✅ Data Analysis in ChatGPT4
5. Clean the data in Excel (Should also be a feasible option since Excel can handle this amount of data without crashing. Didn't test.)


### 4. Data Analysis in ChatGPT4
ChatGPT is actually a great alternative - since the data set doesn't contain sensitive information, I could actually share the prompt with the team and automate myself out of my job by delegating the task (oh yeah). 

Some problems I ran into are:
- sometimes it couldn't parse csv files with special seperators
- there is the need of instructing ChatGPT on an on-going basis to finetune the prompt, a bit time comsuming

1. Clean the raw file
![Screenshot 2024-07-05 at 11 31 10](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/a54c3a9d-1501-4eca-a36a-d897cbeda9a9)

2. Specify expected outcome
![Screenshot 2024-07-05 at 11 31 44](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/13a582cd-4b30-4448-8ff4-e0f20d48c115)

3. Outcome
![Screenshot 2024-07-05 at 11 33 34](https://github.com/carmenjjw/clean-offline-entries-dataframe/assets/78700539/f8f79040-7d4a-41f1-9262-d47555142305)







