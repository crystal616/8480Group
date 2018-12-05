'''
Created on Dec 5, 2018

@author: Ying
'''
import json

movie_user_train_dict = {}
  
user_movie_train_dict = {}
       
with open("train-25.csv") as f:
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
f = open("movie_user_train_dict_25.json","w")
f.write(output)
f.close()
  
output = json.dumps(user_movie_train_dict)
f = open("user_movie_train_dict_25.json","w")
f.write(output)
f.close()


# movie_user_train_dict = {}
 
user_movie_test_dict = {}
      
with open("test-25.csv") as f:
    next(f)
    for line in f:
        data = line.split(",")
        user = str(int(float(data[0])))
        movie = str(int(float(data[1])))      
        rating = float(data[2])   
        if user_movie_test_dict.get(user, 0) == 0:
            user_movie_test_dict[user] = {}     
        user_movie_test_dict[user].update({movie:rating})
        
#         if movie_user_train_dict.get(movie, 0) == 0:
#             movie_user_train_dict[movie] = {}
#         movie_user_train_dict[movie].update({user:rating})
f.close()
  
# print(len(movie_user_train_dict))
#movie = 16655
print(len(user_movie_test_dict))
#user = 153490
 
# output = json.dumps(movie_user_train_dict)
# f = open("movie_user_train_dict_25.json","w")
# f.write(output)
# f.close()
 
output = json.dumps(user_movie_test_dict)
f = open("user_movie_test_dict_25.json","w")
f.write(output)
f.close()
