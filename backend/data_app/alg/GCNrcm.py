import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from typing import List
from dataclasses import dataclass

@dataclass
class User:
    UserID: str
    Interests: List[str]
    Friends: List[str]
    Recommended_posts: List[str]

@dataclass
class Post:
    PostID: str
    Tags: List[str]

class GCN(nn.Module):
    def __init__(self, num_features, hidden_channels, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, num_classes)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return x

class GCNRecommender:
    def __init__(self, users: List[User], posts: List[Post]):
        self.users = users
        self.posts = posts
        self.user_id_map = {user.UserID: idx for idx, user in enumerate(users)}
        self.interest_set = set()
        for user in users:
            self.interest_set.update(user.Interests)
        self.interest_map = {interest: idx for idx, interest in enumerate(self.interest_set)}
        self.model = None

    def prepare_data(self):
        num_users = len(self.users)
        num_interests = len(self.interest_set)

        # 准备节点特征
        x = torch.zeros((num_users, num_interests))
        for user in self.users:
            user_idx = self.user_id_map[user.UserID]
            for interest in user.Interests:
                interest_idx = self.interest_map[interest]
                x[user_idx, interest_idx] = 1

        # 准备边索引
        edge_index = []
        for user in self.users:
            user_idx = self.user_id_map[user.UserID]
            for friend_id in user.friends:
                if friend_id in self.user_id_map:
                    friend_idx = self.user_id_map[friend_id]
                    edge_index.append([user_idx, friend_idx])
                    edge_index.append([friend_idx, user_idx])

        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

        return Data(x=x, edge_index=edge_index)

    def train(self):
        data = self.prepare_data()
        self.model = GCN(num_features=data.num_features, hidden_channels=64, num_classes=data.num_features)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)

        self.model.train()
        for epoch in range(200):
            optimizer.zero_grad()
            out = self.model(data.x, data.edge_index)
            loss = F.mse_loss(out, data.x)
            loss.backward()
            optimizer.step()

    def recommend_with_gcn(self, user: User):
        self.model.eval()
        data = self.prepare_data()
        with torch.no_grad():
            out = self.model(data.x, data.edge_index)

        user_idx = self.user_id_map[user.UserID]
        user_interests = out[user_idx].numpy()
        
        # 获取推荐的兴趣
        recommended_interests = [interest for interest, idx in self.interest_map.items() if user_interests[idx] > 0.5 and interest not in user.Interests]

        # 根据推荐的兴趣对帖子进行评分
        post_scores = {}
        for post in self.posts:
            score = sum(user_interests[self.interest_map[tag]] for tag in post.Tag if tag in self.interest_map)
            post_scores[post.PostID] = score

        # 返回评分最高的10个帖子
        recommended_posts = sorted(post_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        return [post_id for post_id, _ in recommended_posts]
