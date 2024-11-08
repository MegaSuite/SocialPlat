import numpy as np
import json
from dataclasses import dataclass
from typing import List
from celery import shared_task
from PersonalityClassification import PersonalityAnalyzer
from kmeans import KMeans
from InterestsCal import FriendRecommender

@dataclass
class User:
    UserID: int
    Name: str
    Gender: str
    DOB: str  # Date of Birth
    Interests: List[str]
    friends: List[int]
    character: List[float]

# @shared_task
def rcm_friends(user_data_list,user_post_content):
    # 假设 user_data_list 是 User 对象的 JSON 表示形式
    users = []
    user_ids = []
    for user_data in user_data_list:
        user = User(
            UserID=user_data.get('id'),
            Name=user_data.get('user_name'),
            Gender=user_data.get('user_gender'),
            DOB=user_data.get('user_dob_year'),
            Interests=user_data.get('user_hobbies', []),
            friends=user_data.get('user_friends', []),
            character=user_data.get('user_character', [])
        )
        users.append(user)
        user_ids.append(user.UserID)
    user_post = [(post['user_id'], post['post_content']) for post in user_post_content]

    analyze_users_personality(users,user_post)
    # # 输出结果
    # for user in users:
    #     print(f"User ID: {user.UserID}, Personality: {user.character}")

    # 将UserID和character合并，形成新的数据集用于KMeans
    X = np.array([user.character for user in users])
    data_with_ids = np.hstack((np.array([user.UserID for user in users]).reshape(-1, 1), X))  # [UserID, character1, character2, ...]
    # print(data_with_ids)
    # 使用KMeans算法进行聚类
    kmeans = KMeans(k=3)  # 假设聚5类
    labels = kmeans.fit(data_with_ids)  # 执行聚类，返回标签
    # 将每个用户的类别号添加到character的头部
    for i, user in enumerate(users):
        user.character.insert(0, labels[i] + 1)  # 类别号从1开始
    # # 计算SSE并打印
    # kmeans.SSE(data_with_ids)
    # # 画出聚类结果
    # kmeans.plot_clusters(data_with_ids)

    # 实例化推荐系统并生成推荐
    recommender = FriendRecommender(users)
    tf_idf_matrix = recommender.compute_tfidf()
    # print(tf_idf_matrix)
    binary_matrix = recommender.binarize_tfidf(tf_idf_matrix.T)
    signature_matrix = recommender.compute_signature_matrix(binary_matrix, num_hashes=100)
    recommender.minhash_similarity = recommender.compute_jaccard_similarity(signature_matrix)

    # 调用函数计算交友概率矩阵
    num_classes = 3
    prob_matrix = compute_prob_matrix(users, num_classes)
    # 调用函数，获取每类用户更容易与其他类用户成为朋友的权重
    friendship_likelihood = compute_friendship_likelihood(prob_matrix, users)
    # # 输出结果
    # for i in range(len(friendship_likelihood)):
    #     print(f"Class {i+1} friendship likelihood with other classes: {friendship_likelihood[i]}")

    n = 10
    results = {}
    for user_id in user_ids:
        recommended_friends = recommend_friends_with_both(user_id, n, recommender, friendship_likelihood, users)
        # 将推荐的朋友ID添加到用户的friends中
        current_user = next(user for user in users if user.UserID == user_id)
        current_user.friends.extend([user_id for _, user_id in recommended_friends])
        # # 存储推荐的朋友
        results[user_id] = [user_id for _, user_id in recommended_friends]
        # store_recommendations(user_id, [user_id for _, user_id in recommended_friends])
        # print(f"Recommended friends for user {user_id}: {[value for key, value in recommended_friends]}")

    # 输出结果为 JSON 文件
    output_filename = 'recommended_friends.json'
    with open(output_filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    # # 输出到新的 updated_users.json 文件
    # output_data = [{
    #     "UserID": int(user.UserID),  # 将 UserID 转换为 int
    #     "Name": user.Name,
    #     "Gender": user.Gender,
    #     "DOB": user.DOB,
    #     "Interests": user.Interests,
    #     "Seen_post": user.Seen_post,
    #     "Post_post": user.Post_post,
    #     "friends": user.friends,
    #     "character": [int(c) for c in user.character]  # 确保 character 中的所有元素都转为 int
    # } for user in users]  # 获取用户数据的字典表示

    # with open('updated_users.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(output_data, json_file, ensure_ascii=False, indent=4)  # 写入新的 JSON 文件

def analyze_users_personality(users: List[User], content_data: List[tuple]):
    analyzer = PersonalityAnalyzer()
    
    # 将内容按照 UserID 分组
    user_posts = {}
    for user_id, content in content_data:
        if user_id not in user_posts:
            user_posts[user_id] = []
        user_posts[user_id].append(content)

    # 分析每个用户的个性
    for user in users:
        posts = user_posts.get(user.UserID, [])
        personality_scores = analyzer.get_personality_traits(posts)
        user.character = [round(score, 2) for score in personality_scores.values()]

def compute_prob_matrix(users, num_classes):
    # 初始化交友统计矩阵和类别计数矩阵
    friend_matrix = [[0] * num_classes for _ in range(num_classes)]
    class_count = [0] * num_classes
    # 统计每类用户与其他类用户成为朋友的次数
    for user in users:
        user_class = user.character[0] - 1  # 类别号从1开始
        class_count[user_class] += 1  # 增加该类用户的计数
        # 遍历用户的朋友
        for friend_id in user.friends:
            # 根据朋友的ID找到对应的朋友对象
            friend = next((u for u in users if u.UserID == friend_id), None)
            if friend:
                friend_class = friend.character[0] - 1
                friend_matrix[user_class][friend_class] += 1  # 增加交友次数
    # 计算概率矩阵
    prob_matrix = [[0] * num_classes for _ in range(num_classes)]
    for i in range(num_classes):
        total_friends = sum(friend_matrix[i])
        if total_friends > 0:
            for j in range(num_classes):
                prob_matrix[i][j] = friend_matrix[i][j] / total_friends  # 归一化为概率
    return prob_matrix

def compute_friendship_likelihood(prob_matrix, users):
    # 获取类别数量
    num_classes = len(prob_matrix)
    # 统计每类用户的数量
    class_counts = [0] * num_classes
    for user in users:
        class_label = user.character[0] - 1  # 类别号从1开始
        class_counts[class_label] += 1
    # 计算所有用户总数
    total_users = len(users)
    # 初始化结果矩阵
    score_matrix = [[0] * num_classes for _ in range(num_classes)]
    # 计算每类用户与其他类用户成为朋友的综合权重
    for i in range(num_classes):
        for j in range(num_classes):
            # 计算类i与类j成为朋友的权重
            if total_users > 0:
                score_matrix[i][j] = prob_matrix[i][j] * (class_counts[j] / total_users)
    return score_matrix

def recommend_friends_with_both(user_id, n, recommender, friendship_likelihood, users):
    # 根据兴趣相似度推荐朋友
    recommended_friends, friend_dict = recommender.recommend_friends(user_id, n)
    # 获取当前用户的类别
    current_user = next(user for user in users if user.UserID == user_id)
    current_user_class = current_user.character[0] - 1  # 类别从1开始，减1转为索引
    # 加入性格的权重进行排序
    weighted_friends = []
    for similarity_score, friend_id in recommended_friends:
        friend_user = next(user for user in users if user.UserID == friend_id)
        friend_class = friend_user.character[0] - 1
        # 获取性格权重（当前用户类 -> 推荐朋友类的交友概率）
        personality_weight = friendship_likelihood[current_user_class][friend_class]
        # 计算加权分数：兴趣相似度 * 性格权重
        weighted_score = similarity_score * (0.1+personality_weight)
        weighted_friends.append((weighted_score, friend_id))
    # 按加权分数降序排序
    weighted_friends.sort(reverse=True, key=lambda x: x[0])
    # 返回前n个推荐的朋友
    return weighted_friends[:n]

def store_recommendations(user_id, recommendations):
    # 假设有一个 Recommendation 模型保存推荐用户
    # from .models import Recommendation
    # 清除旧数据并保存新推荐结果
    # Recommendation.objects.filter(user_id=user_id).delete()
    # for rec_user in recommendations:
    #     Recommendation.objects.create(user_id=user_id, recommended_user=rec_user)
    # print(f"User {user_id} 推荐好友: {recommendations}")
    return

if __name__ == "__main__":
    with open("./users.json", 'r') as f:
        user_data_list = json.load(f)
    with open("./user_post.json", mode='r', encoding='utf-8') as file:
        user_post_content = json.load(file)
    rcm_friends(user_data_list,user_post_content)
    # rcm_friends.delay(user_data_list,user_post_content)

