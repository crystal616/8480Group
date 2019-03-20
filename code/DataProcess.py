'''
DataProcess.py
Author: Ying Cai
Date: 11/01/12
Description: 
Remove movies which have less than 25 watchers from dataset.
Remove users who have watched less than 25 movies.
Randomly split dataset into training and test sets. For each user, 20% of movies in his/her watching history are selected as test sample.
'''

import pandas as pd
import numpy as np

raw_data = pd.read_csv('./ml-latest/ratings.csv')
del raw_data['timestamp']

movies = pd.read_csv('./ml-latest/movies.csv')

def filter_data(df, group_col, filter_col, threshold):
    '''
    clean data first
    '''
    entry_count = df.groupby(group_col)[filter_col].apply(np.array).apply(np.unique).apply(len)
    entry_count.sort_values(ascending = True, inplace= True)
    # drop
    drop_entries = entry_count[entry_count > threshold]
    drop_entries = drop_entries.to_frame(name='entry_count').reset_index().drop('entry_count', axis=1)
    row_number_before = df.shape[0]
    df = df.merge(drop_entries, how='inner', on=group_col)
    print("Filter {}: shape before {}, shape after {}" .format(filter_col, row_number_before, df.shape[0]))
    return df

raw_data=filter_data(raw_data, 'userId','movieId', 25)
raw_data=filter_data(raw_data,'movieId', 'userId', 25)
raw_data = raw_data.sort_values(by=['userId'])

movie_unique=raw_data['movieId'].unique()
movie_left = movies.loc[movies['movieId'].isin(movie_unique)]

raw_data.to_csv('rating_left.csv', sep=',', index=False)
movie_left.to_csv('movie_left.csv',sep=',', index=False)

# generating test-set and train-set

def random_index_sample(total_rows, row_sample):
    sample_capacity = np.ceil(
        total_rows * row_sample
    ).astype(int)
    row_num = range(total_rows)
    return np.random.choice(row_num, sample_capacity, replace=False)

def user_sampling_from_df(ui_df, row_col_label, user_sample):
    """Random sample of users
    
    filter sourse dataframe rows to select random subsample of users
    """
    print("Rows in source df {}".format(ui_df.shape[0]))
    num_rows = ui_df.shape[0]

    random_index = random_index_sample(num_rows, user_sample)
    # preserve order of rows after sampling
    ui_df = ui_df.iloc[random_index]
    
    print("Rows in df after user sampling {}".format(ui_df.shape[0]))
    return ui_df


select = user_sampling_from_df(raw_data, 'userId',0.2)
traindata = raw_data[~raw_data.isin(select)].dropna()

select.sort_values(by=['userId']).to_csv('test.csv',sep=',',index=False)
traindata.to_csv('train.csv', sep=',',index=False)


