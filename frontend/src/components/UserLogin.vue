<template>
  <div class="container">
    <h3>
      用户登录
      <div class="login">没有账号？<a href="register.html">去注册</a></div>
    </h3>
    <div class="login-form">
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">邮箱:</label>
          <input type="email" v-model="formData.email" id="email" required />
        </div>
        <div class="form-group">
          <label for="password">密码:</label>
          <input type="password" v-model="formData.password" id="password" required />
        </div>
        <input type="submit" value="登录" class="submit-btn">
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        email: '',
        password: ''
      }
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://23.184.88.52:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        const data = await response.json();
        localStorage.setItem('token', data.token);
        alert('登录成功');
        window.location.href = 'profile.html'; // 跳转到个人资料页面
      } catch (error) {
        alert(`登录失败: ${error.message}`);
      }
    }
  }
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
  max-width: 90%;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  height: 400px;
}
h3 {
  text-align: center;
  color: #333;
}
.login {
  font-size: 14px;
  text-align: right;
  margin-top: -20px;
}
.login a {
  color: #007BFF;
  text-decoration: none;
}
.login-form {
  width: 100%;
  margin-top: 30px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.form-group input[type="email"],
.form-group input[type="password"] {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}
.submit-btn {
  margin-top: 20px;
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}
.submit-btn:hover {
  background-color: #218838;
}
</style>
