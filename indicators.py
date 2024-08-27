import math
import os
import pandas as pd

filePath = os.listdir("pastdata")
testdata = pd.read_csv("pastdata/"+filePath[0])

def resourceData(resource: str, df: pd.DataFrame) -> pd.DataFrame: # get data for a specific resource
    return df[df['resource'] == resource] #food - 166163 cells

def cleanData(df: pd.DataFrame) -> pd.DataFrame: # remove outliers
    df = df[(df['price'] < df['price'].mean() + 4 * df['price'].std()) & (df['price'] > df['price'].mean() - 4 * df['price'].std())]
    return df

def baselineStats(resource: str, df: pd.DataFrame) -> float: # mean and standard deviation of resource
    resource_data = resourceData(resource, df)
    return resource_data['price'].mean(), resource_data['price'].std()

def sma(resource: str, period: int, df: pd.DataFrame) -> float: # simple moving average
    filtered_df = resourceData(resource, df).sort_values(by='date_accepted')
    if len(filtered_df) < period:
        raise ValueError(f"Not enough data points available for resource '{resource}'")
    filtered_df = cleanData(filtered_df)
    sma_values = filtered_df['price'].rolling(window=period)
    return sma_values.mean().iloc[-1]

def bollingerBands(rawResource: str, period: int, df: pd.DataFrame) -> tuple: # bollinger bands
    resource_data = df[df['resource'] == rawResource]['price'].tail(period)
    if len(resource_data) < period:
        raise ValueError("Not enough data to calculate Bollinger Bands - period too long")
    else:
        sma = resource_data.mean()
        std = resource_data.std()
        return (sma + 2 * std, sma, sma - 2 * std)

def rsi(resource: str, period: int, df: pd.DataFrame) -> float: # relative strength index
    resource_data = resourceData(resource, df)
    if len(resource_data) < period:
        raise ValueError(f"Not enough data points available for resource '{resource}'")
    resource_data = cleanData(resource_data)
    delta = resource_data['price'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def printStats(resource: str, df: pd.DataFrame) -> None:
    mean, std = baselineStats(resource, df)
    print(f"Resource: {resource}")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")
    print(f"Simple Moving Average: {sma(resource, 5, df)}")
    print(f"Bollinger Bands: {bollingerBands(resource, 5, df)}")
    print(f"Relative Strength Index: {rsi(resource, 5, df)}")

# #print amount of rows in food
# print((resourceData("food", testdata)).shape[0])

print(printStats("food", testdata))
# print(testdata.columns.to_list)