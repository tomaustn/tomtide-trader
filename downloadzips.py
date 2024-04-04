import os
import zipfile
import requests


url = "https://politicsandwar.com/data/trades/"
#https://politicsandwar.com/data/trades/trades-2024-03-20.csv.zip

req = requests.get(url)

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    return local_filename


try:
    os.mkdir("pastdata")
except:
    if os.path.exists("pastdata"):
        print("pastdata folder already exists")
finally:
    for i in range(1, 13):
        for j in range(1, 32):
            url = "https://politicsandwar.com/data/trades/trades-2024-{:02d}-{:02d}.csv.zip".format(i,j)
            print(url)
            filename = download_file(url)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall("pastdata")
            os.remove(filename)
