import pandas as pd
import os

listing_dfs = []
sold_dfs = []


folder = "raw" 
for file in os.listdir(folder):
    if file.endswith(".csv") and "listing" in file.lower():
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        listing_dfs.append(df)
    elif file.endswith(".csv") and "sold" in file.lower():
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        sold_dfs.append(df)

if listing_dfs:
    combined = pd.concat(listing_dfs)
    combined.to_csv("listed.csv", index=False)
    print("lising files combined")
else:
    print("no listing files found")


if sold_dfs:
    combined = pd.concat(sold_dfs)
    combined.to_csv("sold.csv", index=False)
    print("sold files combined")
else:
    print("no sold files found")
