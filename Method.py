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
    
    
def order_list (similarity_list):
    indices = []
    size = similarity_list.shape[0]
    limit = 1.09
    
    while len(indices) < 10:
        limit = limit - 0.1
        for i in range (0, size):
            if similarity_list[i] >= limit:
                indices.append(i)
    
    return indices


    
    