'''
movie.py
Author: Ying Cai
Date: 11/05/12
Description: 
Generate dicts for cleaned full dataset, train set and test set.
'''

import json

movie_user_dict = {}

with open("movie_left.csv", encoding = "utf-8") as f:
    next(f)
    for line in f:
        data = line.split(",")
        movie = data[0]
        movie_user_dict[movie] = {}
f.close()

user_movie_dict = {}
       
with open("rating_left.csv", encoding = "utf-8") as f:
    next(f)
    for line in f:
        data = line.split(",")
        user = data[0]
        movie = data[1]       
        rating = data[2]    
        if user_movie_dict.get(user, 0) == 0:
            user_movie_dict[user] = {}   
		#add watched history to each user
        user_movie_dict[user].update({movie:rating})
		#add all watchers to each movie
        movie_user_dict[movie].update({user:rating})
f.close()
  

 
output = json.dumps(movie_user_dict)
f = open("movie_user_dict.json","w")
f.write(output)
f.close()
 
output = json.dumps(user_movie_dict)
f = open("user_movie_dict.json","w")
f.write(output)
f.close()


movie_user_train_dict = {}
  
user_movie_train_dict = {}
       
with open("train.csv") as f:
    next(f)
    for line in f:
        data = line.split(",")
        user = str(int(float(data[0])))
        movie = str(int(float(data[1])))      
        rating = float(data[2])   
        if user_movie_train_dict.get(user, 0) == 0:
            user_movie_train_dict[user] = {}     
        user_movie_train_dict[user].update({movie:rating})
         
        if movie_user_train_dict.get(movie, 0) == 0:
            movie_user_train_dict[movie] = {}
        movie_user_train_dict[movie].update({user:rating})
f.close()
   
print(len(movie_user_train_dict))
#movie = 16655
print(len(user_movie_train_dict))
#user = 153524
  
output = json.dumps(movie_user_train_dict)
f = open("movie_user_train_dict.json","w")
f.write(output)
f.close()
  
output = json.dumps(user_movie_train_dict)
f = open("user_movie_train_dict.json","w")
f.write(output)
f.close()
 
user_movie_test_dict = {}
      
with open("test.csv") as f:
    next(f)
    for line in f:
        data = line.split(",")
        user = str(int(float(data[0])))
        movie = str(int(float(data[1])))      
        rating = float(data[2])   
        if user_movie_test_dict.get(user, 0) == 0:
            user_movie_test_dict[user] = {}     
        user_movie_test_dict[user].update({movie:rating})
f.close()

print(len(user_movie_test_dict))
#user = 153490
 
output = json.dumps(user_movie_test_dict)
f = open("user_movie_test_dict.json","w")
f.write(output)
f.close()

