'''
Created on Dec 4, 2018

@author: Ying
'''
# from Cosine import similarity_matrix
import pandas as pd
from LensKitTest import user_movie_dict



def recall_precision (pred_list, real_watch_dict):
    count = 0
    real_count = len(real_watch_dict)
    pred_count = pred_list.shape[0]
      
    for user in pred_list:
        if real_watch_dict.get(user,0) != 0:
            count = count + 1
      
    recall = count / float(real_count)
    precision = count / float(pred_count)
    return recall, precision
      
def user_realwatch_list (movie_user_dict, movieId):
    m_dict = movie_user_dict.get(str(movieId))
#     r_list = m_dict.keys()
    return m_dict

# def recall_precision (pred_list, movieId, movie_user_dict):
#     count = 0
#     real_watch_dict = movie_user_dict.get(str(movieId))
#     real_count = len(real_watch_dict)
#     pred_count = pred_list.shape[0]
#      
#     for user in pred_list:
#         if real_watch_dict.get(user,0) != 0:
#             count = count + 1
#      
#     recall = count / float(real_count)
#     precision = count / float(pred_count)
#     return recall, precision
    
def select_movie_basedon_similarity (similarity_matrix, movieId):
    movieIndex = #translate here
    IDs = []
    similarity_list = similarity_matrix[movieIndex,:] ##??correct
    size = similarity_list.shape[0]
    limit = 1.09
     
    while len(indices) < 10:
        limit = limit - 0.1
        for i in range (0, size):
            if similarity_list[i] >= limit and i != movieIndex:
                m_ID = #translate back here
                IDs.append(m_ID)
     
    return IDs

def pred_list (movieId_list, movie_user_dict): ##Here must user movieId not index
    user_list = []
#     for movie in movieId_list:
#         for i in range (0, movie_user_df.shape[0]):
#             if movie_user_df.at[i, "movieId"] == movie:
#                 user_list.append(movie_user_df.at[i, "userId"])
    for movieId in movieId_list:
        user_list.extend(list(movie_user_dict.get(str(movieId)).keys()))
    user_list = list(set(user_list))
    return user_list

def rec_movie_list(userId, user_movie_train_dict, movie_user_train_dict, movieId_index_trans, similarity_matrix):
#     rec_list=[]
    select_movie = []
    watched_list = user_movie_train_dict.get(str(userId))
    mean = sum(watched_list.values()) / float(len(watched_list))
    maxRating = max(watched_list.values())
    for key in watched_list:
        if watched_list.get(key) >= mean:            
            select_movie.extend(select_movie_basedon_similarity(similarity_matrix, key))
    select_movie = list(set(select_movie))
    
    if len(select_movie) > 50: #recommend 50 movies or 100
        temp_list = []
        for movie in select_movie:
            temp_list.append((movie, len(movie_user_train_dict.get(str(movie)))))
        temp_list.sort(key=sortSecond, reverse=True)
        list_50 = temp_list[:50]
        select_movie = []
        for i in range (0, 50):
            select_movie.append(list_50[i][0])
        
    return select_movie

        
def sortSecond(val): 
    return val[1]

def movie_realwatch_list (user_movie_test_dict, userId):
    return user_movie_test_dict.get(userId)
    

    