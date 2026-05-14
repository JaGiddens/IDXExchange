# weeks 4-6: Data Cleaning and Prep

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from scipy.stats import mode

print("\n")
print("Load in Dataset")
print("\n")

# load in dataset
df = pd.read_csv("sold_with_rates.csv")
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

# 2. Remove unnecessary or redundant columns - Will do this throughly when analysis decided


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

"""
    The top 3 columns with missing data include SubdivisonName (62%), AssociationFeeFrequency (58%) and MainLevelBedrooms (42%).'

    Instead of dropping an rows with missing values, I decided to impute some of the columns with values based on the zip code 
    assocated with that row.

    I focused on AssociationFee, AssociationFeeFrequency, and HighSchoolDistrict. So for any rows with these values missing, 
    based I imputed the mean association fee, the most frequent association fee frequency and the most frequent high school 
    district of that postal code.

"""

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


# date consistency checks
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

# print the number of rows that've been flagged

flags = [
    'invalid_flag',
    'invalid_latlong',
    'listing_after_close_flag',
    'purchase_after_close_flag',
    'negative_timeline_flag'
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
df_filtered.to_csv("sold_with_rates_and_filtered.csv", index=False)






