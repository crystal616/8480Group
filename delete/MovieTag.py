'''
Created on Dec 2, 2018

@author: Ying
'''

import json

movie_tag_dict = {}
tag_value = []

with open("genome-scores.txt", encoding = "UTF-8") as f:
    next(f)
    for line in f:
        data = line.split(",")
        movie = data[0]
        tag = data[1]
        relevance = float(data[2])        
        if movie_tag_dict.get(movie, -1) == -1 :
            movie_tag_dict[movie] = {}         
        movie_tag_dict[movie].update({tag:relevance})
f.close()

print(movie_tag_dict['1'])

output = json.dumps(movie_tag_dict)
f = open("movie_tag_dict.json","w")
f.write(output)
f.close()