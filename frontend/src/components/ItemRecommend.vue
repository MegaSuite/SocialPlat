<template>
  <div class="container">
    <h1>推荐好友</h1>
    <div class="friends-list">
      <div class="friend-card">
        <img src="user1.jpg" alt="用户1" width="80" height="80">
        <div class="friend-info">
          <p><strong>名字:</strong> 张三</p>
          <p><strong>专业:</strong> 计算机科学</p>
          <p><strong>兴趣:</strong> 编程、阅读</p>
        </div>
        <button class="add-friend-btn">添加好友</button>
      </div>
      <div class="friend-card">
        <img src="user2.jpg" alt="用户2" width="80" height="80">
        <div class="friend-info">
          <p><strong>名字:</strong> 李四</p>
          <p><strong>专业:</strong> 信息技术</p>
          <p><strong>兴趣:</strong> 旅行、音乐</p>
        </div>
        <button class="add-friend-btn">添加好友</button>
      </div>
      <!-- 添加更多好友推荐 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemRecommend'
  // 这里可以添加数据和方法
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}
.container {
  max-width: 80%;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
h1 {
  text-align: center;
  color: #333;
}
.friends-list {
  margin-top: 30px;
}
.friend-card {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
.friend-card img {
  border-radius: 50%;
  margin-right: 20px;
}
.friend-info {
  flex-grow: 1;
}
.friend-info p {
  margin: 5px 0;
  color: #555;
}
.add-friend-btn {
  padding: 10px 20px;
  background-color: #007BFF;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
.add-friend-btn:hover {
  background-color: #0056b3;
}
</style>
