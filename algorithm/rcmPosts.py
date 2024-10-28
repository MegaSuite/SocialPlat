import json
from typing import List
from dataclasses import asdict
from dataclasses import dataclass, field
from celery import shared_task
from collections import Counter
from InterestsProbe import ProbeSystem
from scipy.sparse import csr_matrix
# from implicit.als import AlternatingLeastSquares
from ALSrcm import AlternatingLeastSquares
from torch_geometric.nn import GCNConv
import torch
import torch.nn.functional as F
from GCNrcm import GCNRecommender
import warnings

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
    Recommended_posts: List[int]

@dataclass
class Post:
    PostID: int         # 帖子ID
    SourceID: int       # 来源ID或用户ID
    Tag: List[str] = field(default_factory=list)  # 标签列表，默认为空列表

# 读取用户和帖子数据的函数
def load_data(user_file: str, post_file: str):
    with open(user_file, 'r') as f:
        user_data_list = json.load(f)
    # 假设 user_data_list 是 User 对象的 JSON 表示形式
    users = []
    user_ids = []
    for user_data in user_data_list:
        user = User(
            UserID=user_data.get('UserID'),
            Name=user_data.get('Name'),
            Gender=user_data.get('Gender'),
            DOB=user_data.get('DOB'),
            City=user_data.get('City'),
            Country=user_data.get('Country'),
            Interests=user_data.get('Interests', []),
            Seen_post=user_data.get('Seen_post', []),
            Post_post=user_data.get('Post_post', []),
            friends=user_data.get('friends', []),
            character=user_data.get('character', []),
            Recommended_posts=[]
        )
        users.append(user)
        user_ids.append(user.UserID)
    with open(post_file, 'r') as f:
        post_data_list = json.load(f)
    posts = []
    for post_data in post_data_list:
        post = Post(
            PostID=post_data.get('PostID'),
            SourceID=post_data.get('SourceID'),
            Tag=post_data.get('Tag', [])
        )
        posts.append(post)
    return users, posts

# 更新单个用户的 Interests
def update_user_interests(user: User):
    # 处理 Seen_post 标签
    seen_tags = [tag for post in user.Seen_post for tag in post]  # 将所有 seen_post 中的标签展开成一个列表
    seen_tag_counts = Counter(seen_tags)  # 统计每个标签的出现次数
    seen_frequent_tags = [tag for tag, count in seen_tag_counts.items() if count > 1]  # 获取出现次数大于1的标签
    seen_frequent_tags.sort(key=lambda tag: seen_tag_counts[tag])  # 按出现次数从小到大排序
    # 将 Seen_post 中的高频标签更新
    for tag in user.Interests:
        if tag in seen_frequent_tags:
            # 将找到的标签移到 Interests 列表的头部
            user.Interests.remove(tag)
            user.Interests.insert(0, tag)
    seen_frequent_tags = [tag for tag, count in seen_tag_counts.items() if count > 3]  # 获取出现次数大于3的标签
    # 将 Seen_post 中的高频标签插入 Interests 头部
    for tag in seen_frequent_tags:
        if tag not in user.Interests:  # 防止重复添加已有的标签
            user.Interests.insert(0, tag)
        if len(user.Interests) > 10:  # 保持 Interests 长度不超过10
            user.Interests.pop()

    # 处理 Post_post 标签
    post_tags = [tag for post in user.Post_post for tag in post]  # 将所有 post_post 中的标签展开成一个列表
    post_tag_counts = Counter(post_tags)  # 统计每个标签的出现次数
    post_frequent_tags = [tag for tag, count in post_tag_counts.items() if count > 0]  # 获取出现次数大于0的标签
    post_frequent_tags.sort(key=lambda tag: post_tag_counts[tag])  # 按出现次数从小到大排序
    # 将 Post_post 中的高频标签更新
    for tag in user.Interests:
        if tag in post_frequent_tags:
            # 将找到的标签移到 Interests 列表的头部
            user.Interests.remove(tag)
            user.Interests.insert(0, tag)
    post_frequent_tags = [tag for tag, count in post_tag_counts.items() if count > 2]  # 获取出现次数大于2的标签
    # 将 Post_post 中的高频标签插入 Interests 头部
    for tag in post_frequent_tags:
        if tag not in user.Interests:  # 防止重复添加已有的标签
            user.Interests.insert(0, tag)
        if len(user.Interests) > 10:  # 保持 Interests 长度不超过10
            user.Interests.pop()

# 更新所有用户的 Interests
def update_all_users_interests(users: List[User]):
    for user in users:
        update_user_interests(user)

# 隐式反馈ALS推荐
def implicit_feedback_recommend_als(user: User, users: List[User], posts: List[Post], factors=10, iterations=15, regularization=0.1):
    # 创建隐式评分矩阵
    user_ids = {u.UserID: idx for idx, u in enumerate(users)}
    post_ids = {p.PostID: idx for idx, p in enumerate(posts)}
    # 构建CSR稀疏矩阵
    rows, cols, data = [], [], []
    for u in users:
        for seen_post in u.Seen_post:
            for post_id in seen_post:
                if post_id in post_ids:
                    rows.append(user_ids[u.UserID])
                    cols.append(post_ids[post_id])
                    data.append(1)  # 看过的互动 +1
        for post_post in u.Post_post:
            for post_id in post_post:
                if post_id in post_ids:
                    rows.append(user_ids[u.UserID])
                    cols.append(post_ids[post_id])
                    data.append(2)  # 自己发布过的 +2
    # 转换为CSR稀疏矩阵
    interaction_matrix = csr_matrix((data, (rows, cols)), shape=(len(users), len(posts)))
    # 使用隐式ALS模型进行推荐
    model = AlternatingLeastSquares(factors=factors, iterations=iterations, regularization=regularization)
    model.fit(interaction_matrix)  # 矩阵进行训练
    # 为当前用户进行推荐
    user_index = user_ids[user.UserID]
    recommendations = model.recommend(user_index, interaction_matrix[user_index], N=10)
    # 提取推荐结果的帖子ID
    recommended_post_ids = [posts[i].PostID for i in recommendations[0]]  # 从第一个数组中提取索引
    return recommended_post_ids

# 根据用户兴趣推荐帖子
def recommend_posts(users: List[User], posts: List[Post], max_recommendations=10, implicit_weight=0.2, original_weight=0.6):
    # 实例化推荐系统
    recommender = ProbeSystem(users)
    # 训练模型
    recommender.train()
    # 保存生成的关联规则到 CSV 文件
    recommender.save_rules_to_csv('./rules.csv')
    # 使用GCN进行推荐
    gcn_recommender = GCNRecommender(users, posts)
    gcn_recommender.train()
    # 遍历每个用户，进行推荐
    for user in users:
        user_id = user.UserID
        # 获取原始推荐结果
        original_recommended_posts = recommender.recommend_posts(user_id, posts)
        # 获取隐式反馈ALS推荐结果
        implicit_recommended_posts = implicit_feedback_recommend_als(user, users, posts)
        # 获取GCN推荐结果
        gcn_recommended_posts = gcn_recommender.recommend_with_gcn(user)
        # print(gcn_recommended_posts)
        # 组合推荐结果
        combined_recommendations = {}
        # 处理原始推荐结果
        for i, post_id in enumerate(original_recommended_posts):
            combined_recommendations[post_id] = original_weight * (len(original_recommended_posts) - i)
        # 处理隐式反馈推荐结果
        for i, post_id in enumerate(implicit_recommended_posts):
            if post_id in combined_recommendations:
                combined_recommendations[post_id] += implicit_weight * (len(implicit_recommended_posts) - i)
            else:
                combined_recommendations[post_id] = implicit_weight * (len(implicit_recommended_posts) - i)
        # 处理GCN推荐结果
        for i, post_id in enumerate(gcn_recommended_posts):
            if post_id in combined_recommendations:
                combined_recommendations[post_id] += implicit_weight * (len(gcn_recommended_posts) - i)
            else:
                combined_recommendations[post_id] = implicit_weight * (len(gcn_recommended_posts) - i)
        # 根据组合得分排序推荐结果
        sorted_recommendations = sorted(combined_recommendations.items(), key=lambda x: x[1], reverse=True)
        # 更新用户的推荐帖子列表
        user.Recommended_posts = [post_id for post_id, score in sorted_recommendations[:max_recommendations]]
    return users

# 将处理后的用户数据写入新文件
def save_recommendations(users: List[User], output_file: str):
    # 将 User 对象列表转换为字典列表
    users_dict = [asdict(user) for user in users]
    # 将用户信息保存到 JSON 文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

# 主函数：读取数据、推荐帖子、输出结果
def process_user_post_recommendations(user_file: str, post_file: str, output_file: str):
    # 读取数据
    users, posts = load_data(user_file, post_file)
    # 更新所有用户的兴趣
    update_all_users_interests(users)
    # 进行推荐
    updated_users = recommend_posts(users, posts)
    # 保存推荐结果
    save_recommendations(updated_users, output_file)

# 调用主函数处理users.json和posts.json
if __name__ == "__main__":
    process_user_post_recommendations("users.json", "posts.json", "users_with_recommendations.json")
    # process_user_data.delay(user_data_list,user_post_content)
