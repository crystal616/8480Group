'''
Created on Dec 4, 2018

@author: Ying
'''




def recall_precision (pred_list, real_list, recall, precision):
    count = 0
    real_count = real_list.shape[0] # or len(real_list)
    pred_count = pred_list.shape[0]
    
    for user in pred_list:
        if user in real_list:
            count = count + 1
    
    recall = count / real_count
    precision = count / pred_count
    
    
def order_list (similarity_list, movieIndex):
    indices = []
    size = similarity_list.shape[0]
    limit = 1.09
    
    while len(indices) < 10:
        limit = limit - 0.1
        for i in range (0, size):
            if similarity_list[i] >= limit and i != movieIndex:
                indices.append(i)
    
    return indices

def pred_list (movieId_list, movie_user_dict): ##Here must user movieId not index
    user_list = []
#     for movie in movieId_list:
#         for i in range (0, movie_user_df.shape[0]):
#             if movie_user_df.at[i, "movieId"] == movie:
#                 user_list.append(movie_user_df.at[i, "userId"])
    for movieId in movieId_list:
        user_list.extend(list(movie_user_dict[movieId].keys()))
    user_list = list(set(user_list))
    return user_list

def selected_watched_list(userId, user_movie_dict):
    watched_list = user_movie_dict.get(str(userId))
    mean = sum(watched_list.values()) / float(len(watched_list))


    
    