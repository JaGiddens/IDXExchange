# weeks 4-6: Data Cleaning and Prep

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from scipy.stats import mode
import sys


print("\n")
print("Load in Dataset")
print("\n")

# load in dataset
# Sold Dataset: ../data/sold_with_rates.csv
# Listings Dataset: ../data/listings_with_rates.csv
csv_path = sys.argv[1]
print(csv_path)
df = pd.read_csv(csv_path)
print(f"This dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
print(df.head())

print("\n")
print("Convert date fields to datetime format")
print("\n")

# 1. Convert date fields to datetime format
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')

# confirm type change
print(df[date_cols].dtypes)

print("\n")
print("Handle missing values appropriately")
print("\n")

# 2. Remove unnecessary or redundant columns 

"""""
For the listings dataset I will remove information that's
only known after the listings is bought. These are the columns 
that have the most missing values

ClosePrice	374468	72.683442	float64
BuyerOfficeAOR	373297	72.456153	object
BuyerOfficeName	363643	70.582332	object
BuyerAgentFirstName	362170	70.296426	object
BuyerAgentMlsId	361572	70.180356	object
BuyerAgentLastName	361466	70.159781	object
CloseDate	355046	68.913673	datetime64[ns]
SubdivisionName	325448	63.168764	object
PurchaseContractDate	258481	50.170612	datetime64[ns]

"""
answer = input("Remove unnecessary columns from listings dataset? (y/n): ")

if answer.lower() == "y":
    print(f"before removing:{df.shape[1]}")
    cols_to_remove = [
    "ClosePrice",
    "BuyerOfficeAOR",
    "BuyerOfficeName",
    "BuyerAgentFirstName",
    "BuyerAgentMlsId",
    "BuyerAgentLastName",
    "CloseDate",
    "SubdivisionName",
    "PurchaseContractDate"
    ]

    df = df.drop(columns=cols_to_remove)
    print(f"after removing:{df.shape[1]}")
    


# 3. Handle missing values appropriately
# display missing counts and percentages per column
# missing counts and percenrages per col
missing = pd.DataFrame({
    'missing_count': df.isna().sum(),
    'missing_percent': df.isna().mean() * 100,
    'data_type':df.dtypes

}).sort_values('missing_percent', ascending=False)

print(f"There are {(missing[missing['missing_percent']>75].shape[0])} columns with greater than 75% of their data missing")
# There should be no columns with greater than 75% of their data missing as we dropped
# them earlier in the analysis
print("Top 5 columns with missing data")
print(missing[missing['missing_count']>0].head())

print(f"Number of columns with no missing data: {missing[missing['missing_count']==0].shape[0]}")

# impute missing data based on postal code
# filter to only pc with at least 20 rows
postal_code_counts = df['PostalCode'].value_counts()
valid_postal_codes = postal_code_counts[postal_code_counts >= 20].index

df_filtered = df[df['PostalCode'].isin(valid_postal_codes)].copy()

# fill by pc with appropriate methods
df_filtered['AssociationFee'] = df_filtered.groupby('PostalCode')['AssociationFee'].transform(
    lambda x: x.fillna(x.mean())
)
df_filtered['AssociationFeeFrequency'] = df_filtered.groupby('PostalCode')['AssociationFeeFrequency'].transform(
    lambda x: x.fillna(x.mode()[0]) if len(x.mode()) > 0 else x
)
df_filtered['HighSchoolDistrict'] = df_filtered.groupby('PostalCode')['HighSchoolDistrict'].transform(
    lambda x: x.fillna(x.mode()[0]) if len(x.mode()) > 0 else x
)


print("\n")
print("Ensure numeric fields are properly typed")
print("\n")


# 4. Ensure numeric fields are properly typed


# to do this we will print the data tyles of all the columns to ensure they are correct
print(df_filtered.dtypes)

# everything seems in order

print("\n")
print("Flag invalid numeric values")
print("\n")


# 5. Flag invalid numeric values
# flag invalid numeric values 
df_filtered['invalid_flag'] = (
    (df_filtered['ListPrice'] <= 0) |
    (df_filtered['LivingArea'] <= 0) |
    (df_filtered['DaysOnMarket'] < 0) |
    (df_filtered['BedroomsTotal'] < 0) |
    (df_filtered['BathroomsTotalInteger'] < 0)
)

# geographic checks
df_filtered['invalid_latlong'] = (
    df_filtered['Latitude'].isna() |
    df_filtered['Longitude'].isna() |
    (df_filtered['Latitude'] == 0) |
    (df_filtered['Longitude'] == 0) |
    (df_filtered['Longitude'] > 0) |
    (~df_filtered['Latitude'].between(32, 42)) |
    (~df_filtered['Longitude'].between(-125, -114))
)


# date consistency checks - only do if working with sold dataset
answer = input("do date consistency checks - only do if working with sold dataset: (y/n)")

if answer == "y":
    df_filtered['listing_after_close_flag'] = (
        df_filtered['ListingContractDate'] > df_filtered['CloseDate']
    )

    df_filtered['purchase_after_close_flag'] = (
        df_filtered['PurchaseContractDate'] > df_filtered['CloseDate']
    )

    df_filtered['negative_timeline_flag'] = (
        (df_filtered['ListingContractDate'] > df_filtered['PurchaseContractDate']) |
        (df_filtered['PurchaseContractDate'] > df_filtered['CloseDate']) |
        (df_filtered['ListingContractDate'] > df_filtered['CloseDate'])
    )


    # count the number of flags
    flags = [
        'invalid_flag',
        'invalid_latlong',
        'listing_after_close_flag',
        'purchase_after_close_flag',
        'negative_timeline_flag'
    ]

    for f in flags:
        print(f, df_filtered[df_filtered[f]].shape[0])

else:
    # count the number of flags for listings dataset
    flags = [
        'invalid_flag',
        'invalid_latlong'
    ]

    for f in flags:
        print(f, df_filtered[df_filtered[f]].shape[0])




"""
    The most counted flags are from the invalid lat and long column.
"""

print("\n")
print("New Shape")
print("\n")

# new shape
print(f"Original rows and cols: {df.shape}")
print(f"Filtered rows and cols: {df_filtered.shape}")


num_added_cols = df_filtered.shape[1] -  df.shape[1]
print(f"Number of columns added: {num_added_cols}")

print("\n")


# make a new dataframe with flagged columns
print("Save new data frame with added columns")
output_name = input("Enter output CSV filename: ")

if not output_name.endswith(".csv"):
    output_name += ".csv"

df_filtered.to_csv(f"data/{output_name}", index=False)




