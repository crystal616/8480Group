'''
Created on Dec 4, 2018

@author: Ying
'''
from Cosine import similarity_matrix
import pandas as pd



def recall_precision (pred_list, real_list):
    count = 0
    real_count = real_list.shape[0] # or len(real_list)
    pred_count = pred_list.shape[0]
    
    for user in pred_list:
        if user in real_list:
            count = count + 1
    
    recall = count / real_count
    precision = count / pred_count
    return recall, precision
    
    
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

def selected_watched_list(userId, user_movie_dict, movie_user_dict, movieId_index_trans, similarity_matrix):
    rec_list=[]
    select_movie = []
    watched_list = user_movie_dict.get(str(userId))
    mean = sum(watched_list.values()) / float(len(watched_list))
    for key in watched_list:
        if watched_list.get(key) >= mean:            
            select_movie.extend(select_movie_basedon_similarity(similarity_matrix, key))
    select_movie = list(set(select_movie))
    
    if len(select_movie) > 50: #recommend 50 movies or 100
        temp_df = pd.DataFrame(columns=['movieId', 'count'])
        for movie in select_movie:
            temp_df.append({movie: len(movie_user_dict.get(movie))})
        temp_df = temp_df.sor
        
    

    
    