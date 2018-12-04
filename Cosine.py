'''
Created on Dec 4, 2018

@author: Ying
'''

import pandas as pd
import numpy as np
import scipy as sp
import math

movie_genre = pd.read_csv("movie-left.csv")



movie_genre.drop(columns="title")

print(movie_genre.head())

row = movie_genre.shape[0]

print(row)

genre_matrix = np.zeros((row, 20 + 1), dtype = int)

names = ["Action","Adventure","Animation","Children","Comedy","Crime","Documentary","Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western","IMAX","(no genres listed)"]

print(len(names))

genres = movie_genre["genres"]
print(genres.shape)
 
for i in range (0, row):
    id = int(movie_genre.iloc[[i]]["movieId"])
    genre_matrix[i][0] = id
    str = movie_genre.at[i, "genres"].split("|")
    for g in str:
        loc = names.index(g)+1
        genre_matrix[i][loc] = 1
        
# np.savetxt("genre matrix.csv", genre_matrix, delimiter=",", fmt="%d")

genre_matrix = genre_matrix[:,1:21]
# np.savetxt("genre matrix without movieId.csv", genre_matrix, delimiter=",", fmt="%d")


genre_matrix_T = genre_matrix.transpose()
# np.savetxt("genre matrix without movieId Transpose.csv", genre_matrix_T, delimiter=",", fmt="%d")
 
similarity_matrix = np.dot(genre_matrix, genre_matrix_T)

cosine_sim = similarity_matrix

for r in range (0, 22714):
    for l in range (r, 22714):
        if (cosine_sim[r][l] != 0):            
            cosine_sim[r][l] = cosine_sim[r][l] / math.sqrt(similarity_matrix[r][r]*similarity_matrix[l][l])
            cosine_sim[l][r] = cosine_sim[r][l]

print(cosine_sim[0,:])

