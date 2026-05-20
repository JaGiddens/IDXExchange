# Week 6 – Feature Engineering and Market Metrics

# imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
import datetime as dt


print("\n")
print("Load in Dataset")
print("\n")

# load dataset and convert date cols
df = pd.read_csv("data/sold_with_rates_and_filtered.csv", 
                 parse_dates=['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate'])

print(f"This dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
print(df.head())


# 1. Make Key Metrics
print("\n")
print("Make Key Metrics")
print("\n")

# make time columns to do future time series analysis
# Year / Month / YrMo
df['year'] = df['CloseDate'].dt.year
df['month'] = df['CloseDate'].dt.month
df['yrmo'] = df['CloseDate'].dt.to_period('M')

print(f"Rang of Years: {df['year'].min()} - {df['year'].max()}")


# Price Ratio -> Measures negotiation strength (simply: higher = better)
df['price_ratio'] = df['ClosePrice'] / df['OriginalListPrice']
print(f"Rang of price ratio: {df['price_ratio'].min()} - {df['price_ratio'].max()}")

# Price Per Sq Ft -> Normalizes price across sizes
df['price_per_sqft'] = df['ClosePrice'] / df['LivingArea']

# Clost to List Ratio -> Captures full price reduction history
df['close_to_list_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

# Listing to Contract Days -> Measures time from lising to accepted offer
df['listing_to_contract_days'] = (
    df['PurchaseContractDate'] - df['ListingContractDate']
).dt.days

# Contract to Close Days -> Escrow and closing period duration
df['contract_to_close_days'] = (
    df['CloseDate'] - df['PurchaseContractDate']
).dt.days


# 2. Do Segment Analysis
print("\n")
print("Segment Analysis")
print("\n")

# PropertyType and PropertySubType
print("PropertyType and PropertySubType Comparison")

def segment_analysis(c1,c2):
    print(f"Analyzing {c1} and {c2}")
    segment = df.groupby([c1, c2]).agg({
    'price_ratio': ['mean', 'median'],
    'price_per_sqft': ['mean', 'median'],
    'close_to_list_ratio': ['mean', 'median'],
    'contract_to_close_days': ['mean', 'median'],
    'listing_to_contract_days': ['mean', 'median']
    }).round(2)

    print(segment.sort_values(('price_ratio', 'mean'), ascending=False))

segment_analysis('PropertyType', 'PropertySubType')
segment_analysis('CountyOrParish', 'MLSAreaMajor')
segment_analysis('ListOfficeName', 'BuyerOfficeName')