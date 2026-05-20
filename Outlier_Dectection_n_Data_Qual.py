# Week 7 – Outlier Detection and Data Quality

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


# buisness rule flags
# close price
df['Invalid_ClosePrice'] = (
    df['ClosePrice'] <= 0
)

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
    'Invalid_ClosePrice',
    'Invalid_LivingArea',
    'Invalid_DaysOnMarket'
]

for f in b_flags:
    print(f, df[df[f]].shape[0])


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
cols = [
    'ClosePrice',
    'LivingArea',
    'DaysOnMarket',
]

for col in cols:
    flag_outliers(col)



# create one flag for all flags ( including previous weeks)
df['flagged'] = (

    # invalid numeric values
    df['invalid_flag'] |

    # geographic issues
    df['invalid_latlong'] |

    # date issues
    df['listing_after_close_flag'] |
    df['purchase_after_close_flag'] |
    df['negative_timeline_flag'] |

    # business rules
    df['Invalid_ClosePrice'] |
    df['Invalid_LivingArea'] |
    df['Invalid_DaysOnMarket'] |

    # outlier flags
    df['ClosePrice_outlier'] |
    df['LivingArea_outlier'] |
    df['DaysOnMarket_outlier']
)


# make new dataframe without outliers and flags
cleaned_df = df[df['flagged'] == False].copy()

cols_to_drop = cleaned_df.filter(
    regex=r'(^Invalid)|(^invalid)|(flag$)|(outlier$)|(flagged$)'
).columns

cleaned_df = cleaned_df.drop(columns=cols_to_drop)
cleaned_df.head()

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



print("The dataset decreased from 377148 rows to 293853 rows after filtering, " \
"removing about 22% of observations. Median ClosePrice decreased slightly " \
"from $825000.0 to $780000.0. Median LivingArea also decreased slightly from 1641.0 to 1572.0. DaysOnMarket only decreased by 1.")


