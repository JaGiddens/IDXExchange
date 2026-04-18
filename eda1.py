# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import os

# load listed and sold datasets
dfs = [pd.read_csv("listed.csv"), pd.read_csv("sold.csv")]

# unique property types 
for i in range(0,2):
    df = dfs[i]
    # stat which dataset it being analysed 
    if i == 0:
        print("----------- Listed Dataset Analysis -----------")
        print(f"The listed dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
    else:
        print("----------- Sold Dataset Analysis -----------")
        print(f"The sold dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
    
    
    
    # unique property types 
    print(f"There is {len(df['PropertyType'].unique())} property type in the listed dataset.")
    print(f"The unique property type is {df['PropertyType'].unique()[0]}")
    
    
    # check for duplicated rows and cols, drop if any found
    duplicated_rows  = df[df.duplicated()]
    
    if len(duplicated_rows) > 0:
    
        print(f"There are {len(duplicated_rows)} duplicated rows")
        print(duplicated_rows)
    
        input("Pres enter to drop duplicated rows and continue")
        df = df.drop_duplicates()
    
    else: print("There were no duplicated rows")
    
    
    duplicate_cols = df.columns[pd.Series(map(tuple,df.values.T)).duplicated()]
    
    if len(duplicate_cols) > 0:
        
        print(f"There are {len(duplicate_cols)} duplicated rows")
        print(duplicate_cols)
    
        input("Pres enter to drop duplicated columns and continue")
        df = df.drop(columns=duplicate_cols)
    
    else: print("There were no duplicated rows")
    
    
    print(f"After dropping the duplicated rows and columns, the dataset has {df.shape[0]} rows and {df.shape[1]} coloumns.")
    
    
    
    # identify any high-missing columns -> high is over 90%
    col_na_counts = df.isna().sum().sort_values(ascending=False)
    high_na = col_na_counts[col_na_counts > (df.shape[0]*.9)]
    print(high_na)
    input("Press Enter to drop the high_na columns and continue")
    df = df.drop(columns=high_na.index)
    print(f"There are {len(high_na)} columns missing more than 90% of data.")
    print(f"After dropping the new number of columns is {df.shape[1]}.")
    print(high_na)
    
    # missing counts and percenrages per col
    missing = pd.DataFrame({
        'missing_count': df.isna().sum(),
        'missing_percent': df.isna().mean() * 100
    }).sort_values('missing_percent', ascending=False)
    
    print(f"There are {(missing[missing['missing_percent']>75].shape[0])} columns with greater than 75% of their data missing")
    missing_75 = missing[missing['missing_percent']>75]
    print(missing_75)
    
    # drop columns with more than 60% data missing 
    df = df.drop(columns=missing_75.index)
    print(f"After dropping them, there are {df.shape[1]} columns.")
    
    cols_to_investigate = [
    'ClosePrice', 
    'LivingArea', 
    'DaysOnMarket', 
    ]
    
    # percentile summaries 
    print(df[cols_to_investigate].describe())
    print("Median values: ")
    print(df[cols_to_investigate].median())
    input("Press Enter to continue to identify outliers...")
    
    
    # make function to identify extreme outliers
    def e_outlier (col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
    
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
    
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        print(f"In the {col} column there are {len(outliers)} outliers")
        return(outliers)   
    
    # identify any extreme outlers using the function defined above
    o = [] # to hold outliers
    for col in cols_to_investigate:
        o.append(e_outlier(col))
    
    o_df = pd.concat(o)
    print(o_df)
    input("Press Enter to continue to make visuals ...")
    
    # make visuals
    os.makedirs("plots", exist_ok=True)  # create folder if it doesn't exist
    
    for col in cols_to_investigate:
        # original data
        plt.figure()
        sns.histplot(df[col], bins=10)
        plt.title(f"Distribution of {col}")
        plt.savefig(f"plots/{col}_hist.png", bbox_inches="tight")
        plt.close()
    
        plt.figure()
        sns.boxplot(x=df[col])
        plt.title(f"Box Plot of {col}")
        plt.savefig(f"plots/{col}_box.png", bbox_inches="tight")
        plt.close()
    
    
        #logged data
        log_col = np.log1p(df[col])
    
        plt.figure()
        sns.histplot(log_col, bins=10)
        plt.title(f"Log Distribution of {col}")
        plt.savefig(f"plots/{col}_log_hist.png", bbox_inches="tight")
        plt.close()
    
        plt.figure()
        sns.boxplot(x=log_col)
        plt.title(f"Log Box Plot of {col}")
        plt.savefig(f"plots/{col}_log_box.png", bbox_inches="tight")
        plt.close()
    
    input("Press enter to save the filtered dataset")
    # save filtered dataset
    if i == 0:
        df.to_csv("c_listed.csv", index=False)
        print("Finished part 1 analysis on Listed dataset")
    else: 
        df.to_csv("c_sold.csv", index=False)
        print("Finished part 1 analysis on Sold dataset")


