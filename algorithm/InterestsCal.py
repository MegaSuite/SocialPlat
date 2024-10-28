import numpy as np
import math
from scipy.spatial.distance import pdist, squareform
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    UserID: int
    Name: str
    Gender: str
    DOB: str  # Date of Birth
    City: str  # City
    Country: str  # Country
    Interests: List[str]
    Seen_post: List[List[str]]
    Post_post: List[List[str]]
    friends: List[int]
    character: List[float]

class FriendRecommender:
    def __init__(self, users: List[User]):
        self.user_interests = {}
        self.user_profiles = {}

        # Initialize users
        for user in users:
            self.user_profiles[user.UserID] = user
            self.user_interests[user.UserID] = user.Interests

    def compute_tfidf(self):
        tags_list = []
        for interests in self.user_interests.values():
            for interest in interests:
                if interest not in tags_list:
                    tags_list.append(interest)
        user_count = len(self.user_interests)
        interest_count = len(tags_list)
        tf_matrix = np.zeros([interest_count, user_count])
        idf_values = np.zeros(interest_count)
        tf_idf = np.zeros([interest_count, user_count])
        interest_to_index = {interest: idx for idx, interest in enumerate(tags_list)}

        # for user_id, interests in self.user_interests.items():
        #     user_index = list(self.user_interests.keys()).index(user_id)
        #     for interest in interests:
        #         if interest in interest_to_index:  # Check if interest exists
        #             tf_matrix[interest_to_index[interest], user_index] += 1

        for user_id, interests in self.user_interests.items():
            user_index = list(self.user_interests.keys()).index(user_id)
            
            # 权重分配：兴趣词汇权重使用上凸函数（平方根函数）衰减
            for pos, interest in enumerate(interests):
                if interest in interest_to_index:
                    weight = 1 / math.sqrt(pos + 1)  # 使用平方根函数
                    tf_matrix[interest_to_index[interest], user_index] += weight

        max_tf_per_user = np.max(tf_matrix, axis=0)
        for i in range(tf_matrix.shape[0]):
            for j in range(tf_matrix.shape[1]):
                tf_matrix[i, j] = tf_matrix[i, j] / max_tf_per_user[j] if max_tf_per_user[j] > 0 else 0
                
        interest_presence_counts = np.count_nonzero(tf_matrix, axis=1)
        for j, interest in enumerate(tags_list):
            idf_values[j] = math.log(user_count / (1 + interest_presence_counts[j]))
        
        for i in range(interest_count):
            for j in range(user_count):
                if tf_matrix[i, j] != 0:
                    tf_idf[i, j] = tf_matrix[i, j] * idf_values[i]
        return tf_idf

    def binarize_tfidf(self, tf_idf_matrix, threshold=0.1):
        binary_matrix = np.where(tf_idf_matrix > threshold, 1, 0)
        return binary_matrix

    def create_hash_functions(self, num_hashes, max_val):
        hash_functions = []
        for i in range(1, num_hashes + 1):
            def hash_fn(x, a=i, b=i + 1, max_val=max_val):
                return (a * x + b) % max_val
            hash_functions.append(hash_fn)
        return hash_functions

    def compute_signature_matrix(self, binary_matrix, num_hashes):
        num_users, num_interests = binary_matrix.shape
        signature_matrix = np.full((num_hashes, num_users), np.inf)
        hash_functions = self.create_hash_functions(num_hashes, num_interests)
        for interest_idx in range(num_interests):
            for user_idx in range(num_users):
                if binary_matrix[user_idx, interest_idx] == 1:
                    for hash_idx, hash_fn in enumerate(hash_functions):
                        hash_val = hash_fn(interest_idx)
                        signature_matrix[hash_idx, user_idx] = min(signature_matrix[hash_idx, user_idx], hash_val)
        return signature_matrix
    
    # def compute_jaccard_similarity(self, signature_matrix):
    #     num_hashes, num_animes = signature_matrix.shape
    #     similarity_matrix = np.zeros((num_animes, num_animes))
    #     for i in range(num_animes):
    #         for j in range(i, num_animes):
    #             sim = np.sum(signature_matrix[:, i] == signature_matrix[:, j]) / num_hashes
    #             similarity_matrix[i, j] = sim
    #             similarity_matrix[j, i] = sim
    #     return similarity_matrix

    def compute_jaccard_similarity(self, signature_matrix):
        jaccard_distances = pdist(signature_matrix.T, metric='jaccard')
        similarity_matrix = 1 - squareform(jaccard_distances)
        return similarity_matrix

    def recommend_friends(self, user_id, n):
        recommend_list = []
        recommend_dict = {}
        user_index = list(self.user_interests.keys()).index(user_id)
        
        for other_user_id in self.user_interests:
            if other_user_id == user_id:
                continue
            other_user_index = list(self.user_interests.keys()).index(other_user_id)
            sim = self.minhash_similarity[user_index, other_user_index]
            if sim > 0:
                recommend_list.append((sim, other_user_id))
                recommend_dict[other_user_id] = sim
        
        recommend_list.sort(reverse=True, key=lambda x: x[0])
        return recommend_list[:n], recommend_dict