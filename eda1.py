# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# load listed and sold datasets
dfs = [pd.read_csv("listed.csv"), pd.read_csv("sold.csv")]

# unique property types 
for i in range(0,1):
    df = dfs[i]

    # unique property types 
    print(f"There is {len(df['PropertyType'].unique())} property type in the listed dataset.")
    print(f"The unique property type is {df['PropertyType'].unique()[0]}")

    # dataset understanding
    if i == 0:
        print(f"The listed dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
    else: 
        print(f"The sold dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")

    # check for duplicated rows and cols, drop if any found
    print(f"There are {df.duplicated().sum()} rows")
    df = df.drop_duplicates()

    duplicate_cols = df.columns[df.T.duplicated()]
    print(duplicate_cols)
    df = df.drop(columns=duplicate_cols, axis = 1)
    print(f"There were {len(duplicate_cols)} duplicated columns.")

    if i == 0:
        print(f"After dropping the duplicated rows and columns, listed dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
    else: 
        print(f"After dropping the duplicated rows and columns, the sold dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")

    
    # identify any high-missing columns -> high is over 90%
    col_na_counts = df.isna().sum().sort_values(ascending=False)
    high_na = col_na_counts[col_na_counts > (df.shape[0]*.9)]
    df = df.drop(columns=high_na.index, axis = 1)
    print(f"There are {len(high_na)} columns missing more than 90% of data.")
    print(f"After dropping the new number of columns is {df.shape[1]}.")
    print(high_na)

    # missing counts and percenrages per col
    missing = pd.DataFrame({
        'missing_count': df.isna().sum(),
        'missing_percent': df.isna().mean() * 100
    }).sort_values('missing_percent', ascending=False)

    print(f"There are {(missing[missing['missing_percent']>75].shape[0])} columns with greater than 75% of their data missing")
    missing[missing['missing_count']>0]

    # drop columns with more than 60% data missing 
    df = df.drop(columns=(missing[missing['missing_percent']>75]).T.columns, axis = 1)
    print(f"After dropping them, there are {df.shape[1]} columns.")

    cols_to_investigate = [
    'ClosePrice', 
    'LivingArea', 
    'DaysOnMarket', 
    ]

    # percentile summaries 
    df[cols_to_investigate].describe()

    # make function to identify extreme outliers
    def e_outlier (col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        print(f"There are {len(outliers)}")
        return(outliers)   

    # identify any extreme outlers using the function defined above
    o = [] # to hold outliers
    for col in cols_to_investigate:
        o.append(e_outlier(col))

    o_df = pd.concat(o)
    o_df.head()

    # make visuals
    for col in cols_to_investigate:
    # histogram
        sns.histplot(df[col], bins = 10)
        plt.title(f"Distribution of {col}")
        plt.show()

        # box plot
        sns.boxplot(x = df[col])
        plt.title(f"Box Plot of {col}")
        plt.show()

    # save filtered dataset
    if i == 0:
        df.to_csv("c_listed.csv", index=False)
    else: 
        df.to_csv("c_sold.csv", index=False)

