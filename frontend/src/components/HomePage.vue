<template>
  <div>
    <header class="header">
      <div class="logo">校园交友平台</div>
      <nav>
        <ul>
          <li><a href="#">首页</a></li>
          <li><a href="#">关于我们</a></li>
          <li><a href="#">活动</a></li>
          <li><a href="#">群组</a></li>
          <li><a href="#">联系我们</a></li>
        </ul>
      </nav>
      <div class="auth-buttons">
        <a href="register.html" class="auth-btn">注册</a>
        <a href="login.html" class="auth-btn">登录</a>
        <a href="profile.html" class="auth-btn">个人中心</a>
      </div>
    </header>
    <section class="section">
      <h2>推荐的朋友</h2>
      <div class="card">
        <img src="user1.jpg" alt="用户1">
        <div class="card-content">
          <p>名字：张三</p>
          <p>专业：计算机科学</p>
          <p>兴趣：编程、阅读</p>
        </div>
      </div>
      <a href="recommend.html" class="more-btn">查看更多</a>
    </section>
    <section class="section">
      <h2>举办的活动</h2>
      <div class="card">
        <div class="card-content">
          <h3>编程马拉松</h3>
          <p>时间：2024年10月20日</p>
          <p>地点：图书馆</p>
          <p>简介：一场为期24小时的编程挑战赛。</p>
        </div>
      </div>
      <a href="activities.html" class="more-btn">查看所有活动</a>
    </section>
    <section class="section">
      <h2>论坛</h2>
      <div class="card">
        <div class="card-content">
          <h3>最新帖子</h3>
          <p>用户A：大家好，有没有人一起组队参加编程马拉松？</p>
          <p>用户B：我有兴趣，怎么联系？</p>
        </div>
      </div>
      <a href="luntan.html" class="more-btn">进入论坛</a>
    </section>
    <footer>
      <div class="quick-links">
        <a href="#">隐私政策</a>
        <a href="#">使用条款</a>
        <a href="#">帮助中心</a>
      </div>
      <div class="social-media">
        <a href="#"><img src="wechat.png" alt="微信"></a>
        <a href="#"><img src="weibo.png" alt="微博"></a>
        <a href="#"><img src="qq.png" alt="QQ"></a>
      </div>
      <div class="copyright">
        <p>© 2024 校园交友平台. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
  // 目前不需要任何数据和方法
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
  color: #333;
}
.header {
  background-color: #28a745;
  color: #fff;
  padding: 20px 0;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header .logo {
  font-size: 24px;
  font-weight: bold;
}
nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  gap: 20px;
}
nav ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 18px;
  padding: 10px 20px;
  transition: background 0.3s;
}
nav ul li a:hover {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}
.auth-buttons {
  display: flex;
  gap: 10px;
}
.auth-btn {
  color: #fff;
  text-decoration: none;
  padding: 10px 20px;
  background-color: #218838;
  border-radius: 4px;
  transition: background 0.3s;
}
.auth-btn:hover {
  background-color: #1e7e34;
}
.section {
  padding: 50px 20px;
  background-color: #fff;
  text-align: center;
  margin-bottom: 20px;
  background: linear-gradient(120deg, #f4f4f4, #ffffff);
}
.section h2 {
  font-size: 32px;
  margin-bottom: 30px;
  color: #333;
}
.card {
  background-color: #fff;
  padding: 20px;
  margin: 10px auto;
  width: 80%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
.card img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
.card-content {
  text-align: left;
}
.more-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #28a745;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  font-size: 18px;
  transition: background 0.3s;
}
.more-btn:hover {
  background-color: #218838;
}
footer {
  background-color: #333;
  color: #fff;
  padding: 20px 0;
  text-align: center;
}
footer .quick-links a, footer .social-media a {
  color: #fff;
  text-decoration: none;
  margin: 0 10px;
}
footer .social-media img {
  width: 24px;
  height: 24px;
  vertical-align: middle;
}
footer .copyright {
  margin-top: 10px;
  font-size: 14px;
}
</style>
