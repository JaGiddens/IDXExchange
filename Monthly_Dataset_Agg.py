# imports
import pandas as pd
import os

# initalize df arrays
listing_dfs = []
sold_dfs = []


# start filling in arrays
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

print(f"before concating sum of rows for listing: {sum(len(df) for df in listing_dfs)}") # 814890
print(f"before concating sum of rows for sold: {sum(len(df) for df in sold_dfs)}") # 568154


# filter and check row counts
if listing_dfs:

    # concat rows
    combined = pd.concat(listing_dfs)
    print(f"after concating sum of rows for listing: {len(combined)}") # 814890

    # filter
    combined = combined[combined["PropertyType"] == "Residential"]
    print(f"after filtering for property type sum of rows for listing: {len(combined)}") # 515204

    # save to csv file
    combined.to_csv("listed.csv", index=False)
    print("lising files combined")
else:
    print("no listing files found")



if sold_dfs:
    combined = pd.concat(sold_dfs)
    print(f"after concating sum of rows for sold: {len(combined)}") # 568154

    combined = combined[combined["PropertyType"] == "Residential"]
    print(f"after filtering for property type sum of rows for listing: {len(combined)}") # 381846

    combined.to_csv("sold.csv", index=False)
    print("sold files combined")
else:
    print("no sold files found")
