# Week 7 – Outlier Detection and Data Quality

# imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
import datetime as dt
import sys


print("\n")
print("Load in Dataset")
print("\n")

# load in dataset
# Sold Dataset: data/sold_flagged.csv
# Listings Dataset: data/listings_flagged.csv

csv_path = sys.argv[1]

print(csv_path)
answer = input("Working with Sold dataset: (y/n) ")
if answer == "y":
    df = pd.read_csv(csv_path, # parse_dates to ensure datetime data type
                    parse_dates=['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate'])
    
else:
    df = pd.read_csv(csv_path, # parse_dates to ensure datetime data type
                    parse_dates=['ListingContractDate', 'ContractStatusChangeDate'])

print(f"This dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
print(df.head())


# 1. Add Buisness Rule Flags

if answer == "y":
    # close price
    df['Invalid_ClosePrice'] = (
        df['ClosePrice'] <= 0
    )
    print('Invalid_ClosePrice', df[df['Invalid_ClosePrice']].shape[0])

# living area
df['Invalid_LivingArea'] = (
    df['LivingArea'] <= 0
)

# days on market
df['Invalid_DaysOnMarket'] = (
    df['DaysOnMarket'] <= 0
)

# count num of buisness flags
b_flags = [
    'Invalid_LivingArea',
    'Invalid_DaysOnMarket'
]

for f in b_flags:
    print(f, df[df[f]].shape[0])


# 2. Add Outlier Flags
# outlier flags
og_df = df.copy()

def flag_outliers(c):
    Q1 = df[c].quantile(0.25) 
    Q3 = df[c].quantile(0.75) 
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # flag the outliers
    df[f'{c}_outlier'] = (
        (df[c] < lower) |
        (df[c] > upper)
    )

    # count the number of outliers detected
    print(c, df[df[f'{c}_outlier']].shape[0])

# cols we want to focus on

if answer == "y":
    cols = [
    'ClosePrice',
    'LivingArea',
    'DaysOnMarket',
    ]

    for col in cols:
        flag_outliers(col)
else:
    cols = [
    'LivingArea',
    'DaysOnMarket',
    ]

    for col in cols:
         flag_outliers(col)



# 3. Count All Flags

# create one flag for all flags (including from previous weeks)
flag_cols = df.filter(
    regex=r'(^Invalid)|(^invalid)|(flag$)|(outlier$)|(flagged$)'
).columns

df['flagged'] = df[flag_cols].any(axis=1)

# make new dataframe without outliers, flags, and NAs
cleaned_df = df[df['flagged'] == False].copy()

cleaned_df = cleaned_df.drop(columns=flag_cols)
cleaned_df.head()



# 4. Make Comparisons Between Cleaned and Flagged Fataset

print("\n")
print("Comparisons")

# compare before and after shapes
num_dropped = df.shape[0] - cleaned_df.shape[0]
percent = (num_dropped/df.shape[0])*100
print(f"Number of rows dropped: {num_dropped} ({percent}%)")
print(f"Old shape: {df.shape}")
print(f"New shape: {cleaned_df.shape}")


# compare medians
before_medians = df[cols].median()
print("Before filtering:")
print(before_medians)


after_medians = cleaned_df[cols].median()
print("After filtering:")
print(after_medians)


""""
The sold dataset decreased from 377148 rows to 293853 rows after filtering,
removing about 22% of observations. Median ClosePrice decreased slightly 
from $825000.0 to $780000.0. Median LivingArea also decreased slightly from 1641.0 
to 1572.0. DaysOnMarket only decreased by 1.

The listings dataset decreased from 509441 rows to 350229 rows after filtering,
removing about 31% of observations. Median LivingArea also decreased slightly from 1668.0 
to 1622.0. DaysOnMarket stayed the same.

"""


# make a new dataframe with new flagged columns
print("Save new data")
if answer == "y":
    df.to_csv("data/sold_allFlagged.csv", index = False)
    cleaned_df.to_csv("data/sold_cleaned.csv", index = False)
else:
    df.to_csv("data/listings_allFlagged.csv", index = False)
    cleaned_df.to_csv("data/listings_cleaned.csv", index = False)




