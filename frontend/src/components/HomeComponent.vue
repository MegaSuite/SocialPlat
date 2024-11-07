<template>
  <div>
    <header class="header">
      <div class="logo">森林友约</div>
      <div class="auth-buttons">
        <a href="register.html" class="auth-btn">注册</a>
        <a href="login.html" class="auth-btn">登录</a>
        <a href="profile.html" class="auth-btn">个人中心</a>
      </div>
    </header>
    <div class="sections-container">
      <section class="section">
        <h2>推友</h2>
        <a href="recommend.html" class="more-btn">助您交友</a>
      </section>
      <section class="section">
        <h2>活动</h2>
        <a href="activities.html" class="more-btn">查看活动</a>
      </section>
      <section class="section">
        <h2>论坛</h2>
        <a href="luntan.html" class="more-btn" target="_blank">进入论坛</a>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeComponent"
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Nunito:400,900|Montserrat|Roboto');

body {
    background: linear-gradient(to right, #3FB6A8, #7ED386);
    font-family: 'Nunito', sans-serif;
}

.header {
    margin-top: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    height: 42.5px;
    background: #FFFFFF;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
}

.logo {
    font-family: 'Nunito', sans-serif;
    color: #3DBB3D;
    font-weight: 900;
    font-size: 2.5em;
    letter-spacing: 1px;
    position: absolute;
    top: 65px;
    left: 50%;
    transform: translateX(-50%);
}

.auth-buttons {
    display: flex;
    margin-right: 20px;
    position: absolute;
    right: 20px;
}

.auth-btn {
    margin-left: 20px;
    text-decoration: none;
    padding: 10px 20px;
    background: #7ED386;
    color: #fff;
    border-radius: 4px;
    font-size: 1em;
    font-weight: bold;
    transition: all .3s ease-in-out;
}

.auth-btn:hover {
    background: #5ba373;
}

.sections-container {
    display: flex;
    justify-content: center;
    margin-top: 200px;
}

.section {
    width: 250px;
    margin: 20px;
    padding: 20px;
    background: #fff;
    box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
    border-radius: 8px;
    text-align: center;
}

h2 {
    font-family: 'Montserrat', sans-serif;
    color: #7ED386;
    font-size: 2em;
    margin-bottom: 20px;
}

.more-btn {
    display: inline-block;
    margin-top: 20px;
    text-decoration: none;
    padding: 10px 20px;
    background: #7ED386;
    color: #fff;
    border-radius: 4px;
    font-size: 1em;
    font-weight: bold;
    transition: all .3s ease-in-out;
}

.more-btn:hover {
    background: #5ba373;
}
</style>