'''
@author: Ying
'''
import pandas as pd
import numpy as np


ratings = pd.read_csv("filter-ratings.csv")

movies = ratings["movieId"].unique()

movie_genre = pd.read_csv("movies.csv")

movie_kept = movie_genre.loc[movie_genre["movieId"].isin(movies)]

movie_kept.to_csv("movie-left.csv", index = False)
