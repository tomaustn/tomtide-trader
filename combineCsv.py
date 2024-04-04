import os
import pandas as pd

path = os.listdir("pastdata")

#sample data: 
#columns: trade_id	date_created	offerer_nation_id	receiver_nation_id	offer_type	buy_or_sell	resource	quantity	price	accepted	original_trade_id	date_accepted
# 16081085	11/18/2023 0:11	203465	136638	0	sell	food	300000	148	1	16081046	11/18/2023 0:15
# 16081090	11/18/2023 0:14	263794	492905	0	sell	gasoline	800	2885	1	16081081	11/18/2023 0:15
# 16081094	11/18/2023 0:14	263794	520789	0	sell	gasoline	1200	2885	1	16081081	11/18/2023 0:16
# 16081100	11/18/2023 0:10	462977	579657	0	sell	coal	31	3666	1	16081039	11/18/2023 0:17
# 16081102	11/18/2023 0:14	263794	520789	0	sell	gasoline	900	2885	1	16081081	11/18/2023 0:17

# 1. read all csv files in pastdata
# 2. combine them into one dataframe
# 3. all trades where accepted = 1 
# 4. write to new csv file

def get_month(file: list[str]) -> str:
    monthDict = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    return monthDict[file.split("-")[2]]

def get_year(file: list[str]) -> str:
    return file.split("-")[1]

def clean_dataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["accepted"] == 1]
    df = df[["buy_or_sell", "resource", "quantity", "price", "date_accepted"]]
    #strip time from date_accepted
    #11/17/2023  12:15:19 AM
    df["date_accepted"] = df["date_accepted"].apply(lambda x: x.split(" ")[0])
    return df

def combine_csv(path: list[str]) -> any:
    df = pd.DataFrame()
    try:
        for file in path:
            temp = pd.read_csv("pastdata/"+file)
            df = pd.concat([df, temp])
        df = clean_dataFrame(df)
        df.to_csv(f"compiledMonthlyData/{get_year(path[0])}{get_month(path[0])}-trades.csv", index=False)
    except:
        print("Error combining csv files")

combine_csv(path)