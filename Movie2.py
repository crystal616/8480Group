'''
Created on Dec 4, 2018

@author: Ying
''' 
import pandas as pd
import numpy as np

movie_genre = pd.read_csv("ratings.csv")

movie_genre = movie_genre.drop(columns="timestamp")

print(movie_genre.head())

def filter_by_threshold(df, group_col, filter_col, threshold):
        entry_count = df.groupby(group_col)[filter_col].apply(np.array).apply(np.unique).apply(len)
        entry_count.sort_values(ascending = True, inplace=True)
        # determine which items to drop
        drop_entries = entry_count[entry_count > threshold]
        drop_entries = drop_entries.to_frame(name='entry_count').reset_index().drop('entry_count', axis=1)
        row_number_before = df.shape[0]
        df = df.merge(drop_entries, how='inner', on=group_col)
        print("Filter {}: shape before {}, shape after {}".format(filter_col, row_number_before, df.shape[0]))
        return df
        

filter_data = filter_by_threshold(movie_genre, 'userId', 'movieId', 25)

filter_data = filter_by_threshold(filter_data, "movieId", "userId", 10)

len(filter_data)

filter_data.to_csv("filter-ratings.csv", index = False)


