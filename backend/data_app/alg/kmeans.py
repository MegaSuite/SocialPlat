import numpy as np
import matplotlib.pyplot as plt


# 定义KMeans类
class KMeans:
    def __init__(self, k=5, max_iter=300, tol=0.0000001):
        self.k = k  # 聚类的数量
        self.max_iter = max_iter  # 最大迭代次数
        self.tol = tol  # 收敛容忍度

    def fit(self, X):
        X = np.array(X)
        
        # 随机初始化聚类中心
        num_rows = X.shape[0]  
        indices = np.random.choice(num_rows, self.k, replace=False) 
        self.centroids = X[indices]

        # 迭代聚类过程
        for i in range(self.max_iter):
            X_without_labels = X[:, 1:]
            centroids_without_labels = self.centroids[:, 1:]
            distances = np.sqrt(((X_without_labels - centroids_without_labels[:, np.newaxis])**2).sum(axis=2))

            # 分配每个点到距离最近的聚类中心
            labels = distances.argmin(axis=0)

            new_centroids = np.array(self.centroids)
            for j in range(self.k):
                points = X[labels == j]
                if points.shape[0] > 0:
                    new_centroids[j, :] = points.mean(axis=0)

            # 计算收敛误差
            delta = np.abs(self.centroids - new_centroids).max()

            # 如果收敛误差小于容忍度，退出迭代
            if delta < self.tol:
                print('迭代次数：', i)
                break

            # 更新聚类中心
            self.centroids = new_centroids
        
        return labels

    def predict(self, X):
        X = np.array(X)
        X_without_labels = X[:, 1:]
        centroids_without_labels = self.centroids[:, 1:]
        distances = np.sqrt(((X_without_labels - centroids_without_labels[:, np.newaxis])**2).sum(axis=2))
        labels = distances.argmin(axis=0)
        return labels
    
    def SSE(self, X):
        X = np.array(X)
        X_without_labels = X[:, 1:]
        centroids_without_labels = self.centroids[:, 1:]
        distances = ((X_without_labels - centroids_without_labels[:, np.newaxis])**2).sum(axis=2)
        labels = distances.argmin(axis=0)

        sse_num = [0] * self.k
        for i in range(len(X)):
            sse_num[int(labels[i])] += distances[int(labels[i])][i]
        print('三个聚类的SSE依次为：', sse_num)
        sse = sum(sse_num)
        print('SSE总和为:', sse)
        self.sse = sse
        return sse

    def get_points(self, m, data, j, data_min):
        point = []
        for i in range(m):
            if data_min[i, 0] == j + 1:
                point.append(data[i])
        return point

    def plot_clusters(self, data):
        data = np.array(data)
        X_without_labels = data[:, 1:]
        centroids_without_labels = self.centroids[:, 1:]
        distances = np.sqrt(((X_without_labels - centroids_without_labels[:, np.newaxis])**2).sum(axis=2))
        labels = distances.argmin(axis=0)

        data_min = np.mat(np.zeros((len(data), 2)))
        for j in range(len(data)):
            data_min[j, :] = labels[j] + 1, distances[int(labels[j])][j]

        colors = ['r', 'g', 'b', 'y', 'm']
        x = int(input("请输入x轴对应的属性: ")) - 1
        y = int(input("请输入y轴对应的属性: ")) - 1

        for j in range(self.k):
            cluster_points = self.get_points(len(data), data, j, data_min)
            cluster_points = np.array(cluster_points)
            plt.scatter(cluster_points[:, x], cluster_points[:, y], c=colors[j], label=f'Cluster {j+1}')
        
        centers_array = np.array(self.centroids)
        plt.scatter(centers_array[:, x], centers_array[:, y], marker='*', s=200, c='black', label='Centroids')
        plt.xlabel(f'Attribute {x+1}')
        plt.ylabel(f'Attribute {y+1}')
        plt.legend()
        # 在图表上方添加SSE和ACC
        plt.title(f'SSE={self.sse:.3f}', fontsize=12, loc='center')
        plt.savefig('fig_no_sign.png')
        plt.show()