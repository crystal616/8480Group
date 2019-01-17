import pandas as pd
import numpy as np
import scipy as sp
import math

movie_genre = pd.read_csv("movie_left.csv")

movieId2title = {}
index2movieId={}
movieId2index={}

for i in range(0,len(movie_genre)):
    movieId=movie_genre.at[i, 'movieId']
    title =movie_genre.at[i,'title']
    movieId2title[movieId] = title
    index2movieId[i]=movieId
    movieId2index[movieId]=i
movie_genre.drop(columns="title")


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
    strs = movie_genre.at[i, "genres"].split("|")
    for g in strs:
        loc = names.index(g)+1
        genre_matrix[i][loc] = 1
        

genre_matrix = genre_matrix[:,1:21]


genre_matrix_T = genre_matrix.transpose()
 
similarity_matrix = np.dot(genre_matrix, genre_matrix_T)
cosine_sim = similarity_matrix
cosine_sim=cosine_sim.astype(float)
sqrt=[]
for i in range(0,len(cosine_sim[0])):
    sqrt.append(math.sqrt(cosine_sim[i][i]))

for r in range (0, row):
    for l in range (r, row):
        if (cosine_sim[r,l] != 0):            
            cosine_sim[r,l] = cosine_sim[r,l] / (sqrt[r]*sqrt[l])
            cosine_sim[l,r] = cosine_sim[r,l]


def recall_precision (pred_list, real_dict):
    count = 0
    real_count = len(real_dict)# or len(real_list)
    pred_count = len(pred_list)
    if real_count == 0:
        return 0.0,0.0 
    for user in pred_list:
        user = str(user)
        if real_dict.get(user,0) != 0:
            count = count + 1
        
    
    recall = count / real_count
    precision = count / pred_count
    return recall, precision
    
def select_movie_basedon_similarity (similarity_matrix, movieIndex,nn,step):
    IDs = []
    similarity_list = similarity_matrix[movieIndex,:] ##??correct
    size = similarity_list.shape[0]
    limit = 0.99+step
    
    while len(IDs) < nn:
        limit = limit - step
        for i in range (0, size):
            if similarity_list[i] >= limit and i != movieIndex:
                m_ID = index2movieId[i]
                IDs.append(m_ID)
    
    return IDs

def pred_list (movieId_list, movie_user_dict): ##Here must user movieId not index
    user_list = []
    for movieId in movieId_list:
        user_list.extend(list(movie_user_dict[str(movieId)].keys()))
    user_list = list(set(user_list))
    return user_list


def real_list (movie_user_dict, movieId):
    m_dict = movie_user_dict.get(str(movieId))
    return m_dict

def rec_movie_list(userId, user_movie_train_dict, movie_user_train_dict, similarity_matrix,cutOff, listLength, nn, step):
    select_movie = []
    watched_list = user_movie_train_dict.get(str(userId))
    mean = sum(watched_list.values()) / float(len(watched_list))
    if cutOff != 0:
        maxRating=max(watched_list.values())
        mean = mean + (maxRating-mean)/2
    for key in watched_list:
        if watched_list.get(key) >= mean:
            index=movieId2index[int(key)]
            select_movie.extend(select_movie_basedon_similarity(similarity_matrix, index, nn, step))
    select_movie = list(set(select_movie))
    
    if len(select_movie) > listLength: #recommend 50 movies or 100
        temp_list = []
        for movie in select_movie:
            temp_list.append((movie, len(movie_user_train_dict.get(str(movie)))))
        temp_list.sort(key=sortSecond, reverse=True)
        list_50 = temp_list[:listLength]
        select_movie = []
        for i in range (0, listLength):
            select_movie.append(list_50[i][0])
    return select_movie

        
def sortSecond(val): 
    return val[1]

def movie_realwatch_list (user_movie_test_dict, userId):
    userId = str(userId)
    return user_movie_test_dict.get(userId,{})

import json
with open("user_movie_train_dict.json") as f:
    user_movie_train_dict = json.load(f)
f.close


import json
with open("movie_user_train_dict.json") as f:
    movie_user_train_dict = json.load(f)
f.close


import json
with open("user_movie_test_dict.json") as f:
    user_movie_test_dict = json.load(f)
f.close

rating=pd.read_csv('rating_left.csv')
userlist = np.random.choice(rating.userId.unique(), 1000)
recall = []
precision = []

# threshold for choosing neighbor
steps = [0.02,0.1]
# number of nearest neighbor
nn = [1,3,5,10]
# use mean for threshold of eating?
cutOffs = [0,1]
# length of recommendation list
listLengths = [50, 100, 150]

for step in steps:
    for k in nn:
        for cutOff in cutOffs:
            for listLength in listLengths:
                for userId in userlist:
                    select_movies=rec_movie_list(userId, user_movie_train_dict, movie_user_train_dict,cosine_sim,cutOff,listLength, k, step)
                    real_watch=movie_realwatch_list(user_movie_test_dict, userId)
                    a, b = recall_precision (select_movies, real_watch)
                    recall.append(a)
                    precision.append(b)
                    print('recall: ',a, ' precision: ', b)	
                    with open('recall-movie2user-cutOff'+str(cutOff)+'-L'+str(listLength)+'-k'+str(k)+'-step'+str(step)+'.json', 'w') as outfile:
                        json.dump(recall, outfile)
                    with open('precision-movie2user-cutOff'+str(cutOff)+'-L'+str(listLength)+'-k'+str(k)+'-step'+str(step)+'.json', 'w') as outfile:
                        json.dump(precision,outfile)    

with open("movie_user_dict.json") as f:
    movie_user_dict = json.load(f)
f.close()

recall=[]
precision=[]

for step in steps:
    for k in nn:
        for i in range(row):
            recom_movies=select_movie_basedon_similarity(cosine_sim,i, k, step)
            pred=pred_list(recom_movies,movie_user_dict)
            real=real_list(movie_user_dict, index2movieId[i])
            a, b = recall_precision (pred, real)
            recall.append(a)
            precision.append(b)
            print('recall: ',a, ' precision: ', b)	
            with open('recall-user2movie-step'+str(step)+'-k'+str(k)+'.json', 'w') as outfile:
                json.dump(recall, outfile)
            with open('precision-user2movie-step'+str(step)+'-k'+str(k)+'.json', 'w') as outfile:
                json.dump(precision,outfile)
