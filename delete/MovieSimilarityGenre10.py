'''
Created on Dec 2, 2018

@author: Ying
'''
import json
import math

with open("movie_genre_dict.json") as f:
    dict = json.load(f)
f.close()

genre_names = ["Adventure","Animation","Children","Comedy", "Fantasy","Romance","Drama","Action","Crime","Thriller","Horror","Mystery","Sci-Fi","IMAX","Documentary","War","Musical","Western","Film-Noir","(no genres listed)"]

size = len(genre_names)

movie_genre_similarity10 = {}
 
for i in range (140000, 193887):
    if dict.get(str(i), -1) != -1:
        print(i)
        movie_genre_similarity10[str(i)] = {}
        for k in range (i+1, 193887):
            if dict.get(str(k), -1) != -1:
                score = 0
                for genre in range (0, size):
                    score = score + dict[str(i)].get(genre_names[genre], 0) * dict[str(k)].get(genre_names[genre], 0)
                if score != 0:
                    score = score / math.sqrt(len(dict[str(i)]) * len(dict[str(k)]))
                    movie_genre_similarity10[str(i)].update({str(k):score})
                    if movie_genre_similarity10.get(str(k), -1) == -1:
                        movie_genre_similarity10[str(k)] = {}
                    movie_genre_similarity10[str(k)].update({str(k):score})
    


print(movie_genre_similarity10['1'])


output = json.dumps(movie_genre_similarity10)
f = open("movie_genre_similarity10.json","w")
f.write(output)
f.close()