import numpy as np
from scipy.sparse import csr_matrix

class AlternatingLeastSquares:
    def __init__(self, factors=10, iterations=15, regularization=0.1):
        self.factors = factors
        self.iterations = iterations
        self.regularization = regularization
        self.user_factors = None
        self.item_factors = None

    def fit(self, interaction_matrix):
        num_users, num_items = interaction_matrix.shape
        self.user_factors = np.random.normal(scale=1./self.factors, size=(num_users, self.factors))
        self.item_factors = np.random.normal(scale=1./self.factors, size=(num_items, self.factors))
        # 进行迭代
        for iteration in range(self.iterations):
            # 更新用户因子
            for u in range(num_users):
                interaction_row = interaction_matrix[u, :].toarray().flatten()
                self.user_factors[u] = self._update_user_factors(u, interaction_row)
            # 更新物品因子
            for i in range(num_items):
                interaction_col = interaction_matrix[:, i].toarray().flatten()
                self.item_factors[i] = self._update_item_factors(i, interaction_col)

    def _update_user_factors(self, user, interaction_row):
        item_indices = np.where(interaction_row > 0)[0]
        if len(item_indices) == 0:
            return self.user_factors[user]  # 没有互动的用户，返回原因子

        item_matrix = self.item_factors[item_indices, :]
        interaction_values = interaction_row[item_indices]
        A = item_matrix.T @ item_matrix + self.regularization * np.eye(self.factors)
        b = item_matrix.T @ interaction_values
        return np.linalg.solve(A, b)

    def _update_item_factors(self, item, interaction_col):
        user_indices = np.where(interaction_col > 0)[0]
        if len(user_indices) == 0:
            return self.item_factors[item]  # 没有互动的物品，返回原因子

        user_matrix = self.user_factors[user_indices, :]
        interaction_values = interaction_col[user_indices]
        A = user_matrix.T @ user_matrix + self.regularization * np.eye(self.factors)
        b = user_matrix.T @ interaction_values
        return np.linalg.solve(A, b)

    def recommend(self, user_index, interaction_row, N=10):
        scores = self.item_factors @ self.user_factors[user_index]
        item_indices = np.argsort(scores)[::-1]  # 降序排列
        recommended_items = item_indices[:N]
        return recommended_items, scores[recommended_items]