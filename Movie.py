'''
Created on Dec 2, 2018

@author: Ying
'''

import json

movie_genre_dict = {}
movie_user_dict = {}

with open("movies.txt", encoding = "UTF-8") as f:
    next(f)
    for line in f:
        data = line.split(",")
        movie = data[0]
        index = len(data)
        t = data[index-1]
        genre = t.split("|")
        temp_dict = {}
        for s in genre:
            temp_dict.update({s.rstrip():1})
        movie_genre_dict.update({movie: temp_dict})
        movie_user_dict[movie] = {}
f.close()

print(movie_genre_dict['1'])

output = json.dumps(movie_genre_dict)
f = open("movie_genre_dict.json","w")
f.write(output)
f.close()
 
user_movie_dict = {}
  
for i in range(1, 283229):
    user_movie_dict[str(i)] = {}
       
with open("ratings.txt") as f:
    next(f)
    for line in f:
        data = line.split(",")
        user = data[0]
        movie = data[1]       
        rating = data[2]        
        user_movie_dict[user].update({movie:rating})
        movie_user_dict[movie].update({user:rating})
f.close()
  
print(user_movie_dict['1'])
print(user_movie_dict['283228'])
  
print(movie_user_dict['1'])
print(movie_user_dict['193886'])
 
output = json.dumps(movie_user_dict)
f = open("movie_user_dict.json","w")
f.write(output)
f.close()
 
output = json.dumps(user_movie_dict)
f = open("user_movie_dict.json","w")
f.write(output)
f.close()



