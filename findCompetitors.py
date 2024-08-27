# Script to find the most active traders for a specific commodity in the last day.
import math
import os
import pandas as pd
import time

path = os.listdir("pastdata")
testdata = pd.read_csv("pastdata/"+path[-1]) # get the most recent data

def resourceData(resource: str, df: pd.DataFrame) -> pd.DataFrame: # get data for a specific resource
    return df[df['resource'] == resource] 

def returnCompetitors(resource: str, df: pd.DataFrame) -> pd.DataFrame: # get whoever bought the most of a resource
    data = resourceData(resource, df)
    #7/17/2024 13:40
    date = time.strftime('%m/%d/%Y')
    # 2024-08-23 23:34:42
    # return data[data['date_accepted'][:-8] == date].groupby('receiver_nation_id')['quantity'].sum().sort_values(ascending=True)
    return data.groupby('receiver_nation_id')['quantity'].sum().sort_values(ascending=True)


print(returnCompetitors("lead", testdata))

