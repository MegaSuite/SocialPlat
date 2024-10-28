import pandas as pd
import numpy as np
import random
from typing import List
from dataclasses import dataclass, field
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

@dataclass
class Post:
    PostID: int
    SourceID: int
    Tag: List[str] = field(default_factory=list)

class ProbeSystem:
    def __init__(self, users):
        self.users = users
        self.support_data = {}
        self.minsupport = 0.02
        self.minconfidence = 0.04
        self.rule_list = []

    def Create_C1(self, c1):
        """创建 C1 集合"""
        C1 = set()
        for item in c1:
            item_set = frozenset([item])
            C1.add(item_set)
        return C1

    def is_apriori(self, ck_item, Lk):
        """检查 k-1 项集是否为 k 项集的子集"""
        for item in ck_item:
            sub_item = ck_item - frozenset([item])
            if sub_item not in Lk:
                return False
        return True

    def Create_Ck(self, Lk, k):
        """生成候选 k 项集 Ck"""
        Ck = set()
        len_Lk = len(Lk)
        list_Lk = list(Lk)
        for i in range(len_Lk):
            for j in range(i + 1, len_Lk):
                l1 = list(list_Lk[i])
                l2 = list(list_Lk[j])
                l1.sort()
                l2.sort()
                l1 = l1[0:k - 2]
                l2 = l2[0:k - 2]
                if l1 == l2:
                    Ck_item = list_Lk[i] | list_Lk[j]
                    if self.is_apriori(Ck_item, Lk):
                        Ck.add(Ck_item)
        return Ck

    def get_Lk(self, baskets, Ck):
        """计算频繁项集 Lk"""
        Lk = set()
        item_count = {}
        for t in baskets:
            for item in Ck:
                if item.issubset(t):
                    if item not in item_count:
                        item_count[item] = 1
                    else:
                        item_count[item] += 1
        data_num = float(len(baskets))
        for item in item_count:
            if (item_count[item] / data_num) >= self.minsupport:
                Lk.add(item)
                self.support_data[item] = item_count[item] / data_num
        return Lk

    def multihash(self, L1, baskets):
        """多重哈希处理候选 2 项集"""
        C2 = list(self.Create_Ck(L1, 2))
        bucket1 = [[] for _ in range(1500)]
        bucket2 = [[] for _ in range(1500)]
        itemset_to_index = {itemset: idx for idx, itemset in enumerate(L1)}

        hash1 = []
        hash2 = []
        for itemset in C2:
            indices = [itemset_to_index[frozenset([item])] for item in itemset]
            if len(indices) == 2:
                product_mod_1500 = (indices[0] * indices[1]) % 1500
                hash1.append(product_mod_1500)

        for itemset in C2:
            indices = [itemset_to_index[frozenset([item])] for item in itemset]
            if len(indices) == 2:
                product_mod_1500 = (indices[0] + indices[1]) % 1500
                hash2.append(product_mod_1500)

        for hashnum, itemset in zip(hash1, C2):
            index = hashnum % 1500
            bucket1[index].append(itemset)

        for hashnum, itemset in zip(hash2, C2):
            index = hashnum % 1500
            bucket2[index].append(itemset)

        # 计算每个候选 2 项集的 support 值
        support_values = {itemset: 0 for itemset in C2}
        for basket in baskets:
            for itemset in C2:
                if itemset.issubset(basket):
                    support_values[itemset] += 1

        for index, bucket_items in enumerate(bucket1):
            bucket_support_sum = sum(support_values[itemset] for itemset in bucket_items)
            if bucket_support_sum / float(len(baskets)) < self.minsupport:
                bucket1[index] = []

        for index, bucket_items in enumerate(bucket2):
            bucket_support_sum = sum(support_values[itemset] for itemset in bucket_items)
            if bucket_support_sum / float(len(baskets)) < self.minsupport:
                bucket2[index] = []

        filtered_C2 = []
        temp1 = []
        temp2 = []
        for index, bucket_items in enumerate(bucket1):
            if bucket_items:
                temp1.extend(bucket_items)
        temp1 = set(temp1)
        for index, bucket_items in enumerate(bucket2):
            if bucket_items:
                temp2.extend(bucket_items)
        temp2 = set(temp2)
        filtered_C2 = list(temp1 & temp2)

        return filtered_C2

    def train(self):
        """训练模型并生成频繁项集"""
        baskets = []
        for user in self.users:
            baskets.append(user.Interests)

        c1 = [item for user in self.users for item in user.Interests]
        C1 = self.Create_C1(c1)
        L1 = self.get_Lk(baskets, C1)
        Lk = L1.copy()
        L = [Lk]
        filtered_C2 = self.multihash(Lk, baskets)
        L2 = self.get_Lk(baskets, filtered_C2)
        Lk = L2.copy()
        L.append(Lk)

        for k in range(3, 5):
            Ck = self.Create_Ck(Lk, k)
            Lk = self.get_Lk(baskets, Ck)
            Lk = Lk.copy()
            L.append(Lk)

        return L

    def save_rules_to_csv(self, filename):
        """保存生成的关联规则到 CSV 文件"""
        rule_list = self.get_Rule()
        with open(filename, 'w') as f:
            for item in rule_list:
                f.write('{}\t{}\t{}\t: {}\n'.format(list(item[0]), "of", list(item[1]), item[2]))

    def get_Rule(self):
        """获取关联规则"""
        rule_list = []
        sub_set_list = []
        L = self.train()  # 重新训练以获取频繁项集
        for i in range(len(L)):
            for frequent_set in L[i]:
                for sub_set in sub_set_list:
                    if sub_set.issubset(frequent_set):
                        conf = self.support_data[frequent_set] / self.support_data[sub_set]
                        rule = (sub_set, frequent_set - sub_set, conf)
                        if conf >= self.minconfidence and rule not in rule_list:
                            rule_list.append(rule)
                sub_set_list.append(frequent_set)
        # 生成关联规则并存储到 `self.rule_list` 中
        self.rule_list = rule_list
        return rule_list

    def recommend(self, user_id):
        # 为指定用户生成推荐
        user = next((u for u in self.users if u.UserID == user_id), None)
        if not user:
            print(f"User ID {user_id} not found.")  # 如果找不到用户，输出提示
            return
        current_interests = set(user.Interests)  # 获取当前用户的兴趣
        recommended_tags = []  # 用于存储推荐的标签
        # 根据关联规则查找推荐标签
        for antecedent, consequent, confidence in self.rule_list:
            if antecedent.issubset(current_interests) and not consequent.issubset(current_interests):
                for tag in consequent:
                    if tag not in current_interests:
                        recommended_tags.append((tag, confidence))  # 记录推荐标签及其置信度
        # 按置信度排序推荐标签
        recommended_tags = sorted(recommended_tags, key=lambda x: x[1], reverse=True)
        # 输出推荐度最高的前5个标签及其推荐度
        print("Top 5 Recommended Tags and Confidence Scores:")
        for tag, confidence in recommended_tags[:5]:
            print(f"Tag: {tag}, Confidence: {confidence}")
        # 更新用户的兴趣列表
        for tag, _ in recommended_tags:
            if tag not in user.Interests:
                if len(user.Interests) >= 10:
                    user.Interests.pop()  # 如果兴趣列表长度超过 10，删除最后一个标签
                    user.Interests.append(tag)  # 将推荐标签插入到兴趣列表尾部
                    break
                elif len(user.Interests) == 9:
                    user.Interests.append(tag)  # 将推荐标签插入到兴趣列表尾部
                    break
                else:
                    user.Interests.append(tag)  # 将推荐标签插入到兴趣列表尾部
        print(f"Updated interests for user {user_id}: {user.Interests}")  # 输出更新后的兴趣列表

    def recommend_posts(self, user_id: int, posts: List[Post]) -> List[int]:
        # 根据用户ID查找用户
        user = next((u for u in self.users if u.UserID == user_id), None)
        if not user:
            print(f"User ID {user_id} not found.")
            return []

        interests = user.Interests  # 获取用户的兴趣列表
        scored_posts = []

        # 计算每个 post 的得分
        for post in reversed(posts):  # 从尾部开始遍历帖子列表
            score = 0
            for tag in post.Tag:
                if tag in interests:
                    index = interests.index(tag)
                    score += 20 - index
                else:
                    score -= 5

            # 如果得分超过 40，加入候选列表
            if score > 10:
                scored_posts.append((post.PostID, score))
                if len(scored_posts) > 100:
                    break
        # 按分数和位置进行加权随机选择，生成推荐帖子列表
        if scored_posts:
            # 计算权重：post_id 越大且得分越高，权重越大
            weighted_posts = [
                (post_id, score * post_id)  # 使用 post_id 和 score 的乘积作为权重
                for post_id, score in scored_posts
            ]
            selected_posts = []
            attempts = 0
            # 重抽直到获得10个不重复的推荐帖子或达到最大抽取次数
            while len(selected_posts) < 20 and attempts < 200:
                selected_post = random.choices(
                    weighted_posts,
                    weights=[weight for _, weight in weighted_posts],
                    k=1
                )[0][0]  # 获取抽取的post_id
                # 若抽取的帖子未出现在selected_posts中，则添加
                if selected_post not in selected_posts:
                    selected_posts.append(selected_post)
                attempts += 1
            # print(f"Recommended posts for user {user_id}: {selected_posts}")
            return selected_posts
        else:
            print(f"No suitable posts found for user {user_id}.")
            return []
