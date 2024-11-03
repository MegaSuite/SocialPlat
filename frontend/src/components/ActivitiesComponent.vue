<template>
  <div class="container">
    <h1>举办的活动</h1>
    <div class="activities-list">
      <div class="activity-card">
        <h3>编程马拉松</h3>
        <p><strong>时间:</strong> 2024年10月20日</p>
        <p><strong>地点:</strong> 图书馆</p>
        <p>一场为期24小时的编程挑战赛。</p>
      </div>
      <div class="activity-card">
        <h3>音乐节</h3>
        <p><strong>时间:</strong> 2024年11月15日</p>
        <p><strong>地点:</strong> 学生活动中心</p>
        <p>来享受一场视听盛宴，尽情放松吧。</p>
      </div>
      <!-- 添加更多活动 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivitiesComponent',
  // 可以在这里添加数据和方法
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
.activities-list {
  margin-top: 30px;
}
.activity-card {
  padding: 20px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
.activity-card h3 {
  margin-top: 0;
  color: #007BFF;
}
.activity-card p {
  margin: 5px 0;
  color: #555;
}
</style>
