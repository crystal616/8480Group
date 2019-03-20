'''
Created on Dec 4, 2018

@author: Ying
'''

import pandas as pd
import numpy as np

df = pd.read_csv("filter-ratings.csv")

print(df.head())

def random_index_sample(total_rows, row_sample):
    sample_capacity = np.ceil(total_rows * row_sample).astype(int)
    row_num = range(total_rows)
    return np.random.choice(row_num, sample_capacity, replace=False)
 
def user_sampling_from_df(ui_df, row_col_label, user_sample):
    print("Rows in source df {}".format(ui_df.shape[0]))
    num_rows = ui_df.shape[0]
    random_index = random_index_sample(num_rows, user_sample)
    # preserve order of rows after sampling
#     ui_df = ui_df.ix[random_index]
    rt = ui_df.iloc[random_index]
    print("Rows in df after user sampling {}".format(rt.shape[0]))
    return rt
 
selected = user_sampling_from_df(df, "userId", 0.2)
traindata = df[~df.isin(selected)].dropna()

traindata.to_csv("train.csv", index=False)
selected.to_csv("test.csv", index=False)

print(len(df))
print(len(selected))
