<template>
  <div class="w registerarea">
    <h3>注册新用户
      <div class="login">我有账号，去<router-link to="/login">登录</router-link></div>
    </h3>
    <div class="reg-form">
      <form @submit.prevent="handleSubmit">
        <div class="form-left">
          <ul>
            <li>
              <label for="name">名称:</label>
              <input type="text" v-model="formData.name" id="name" required />
            </li>
            <li>
              <label for="email">邮箱:</label>
              <input type="email" v-model="formData.email" id="email" required />
            </li>
            <li>
              <label for="password">密码:</label>
              <input type="password" v-model="formData.password" id="password" required />
            </li>
            <li>
              <label for="job">专业:</label>
              <input type="text" v-model="formData.job" id="job" required />
            </li>
            <li>
              <input type="submit" value="提交注册">
            </li>
          </ul>
        </div>
        <div class="form-right">
          <ul>
            <li>
              <label for="hobby">兴趣:</label>
              <div id="tags">
                <label v-for="tag in allHobbyTags" :key="tag">
                  <input type="checkbox" v-model="formData.hobbies" :value="tag"> {{ tag }}
                </label>
              </div>
            </li>
          </ul>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterComponent',
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        job: '',
        hobbies: []
      },
      allHobbyTags: [
        '编程', '阅读', '旅行', '摄影', '音乐',
        '运动', '电影', '美食', '手工艺', '游戏',
        '瑜伽', '健身', '园艺', '宠物', '绘画',
        '写作', '舞蹈', '戏剧', '志愿服务', '烹饪',
        '钓鱼', '露营', '滑雪', '冲浪', '攀岩',
        '桌游', '卡牌游戏', '模型制作', '收藏', '天文'
      ]
    };
  },
  methods: {
    async handleSubmit() {
      if (this.formData.hobbies.length < 3 || this.formData.hobbies.length > 10) {
        alert('请至少选择三个兴趣标签，最多选择十个');
        return;
      }
      try {
        const response = await axios.post('http://23.184.88.52:8000/api/data/', this.formData);
        if (response.status !== 200) {
          throw new Error('Network response was not ok');
        }
        alert('数据提交成功');
        this.clearForm();
      } catch (error) {
        alert(`表单提交失败: ${error.message}`);
      }
    },
    clearForm() {
      this.formData = {
        name: '',
        email: '',
        password: '',
        job: '',
        hobbies: []
      };
    }
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.w {
  max-width: 90%;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  height: 600px;
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

.reg-form {
  width: 100%;
  position: relative;
}

.form-left,
.form-right {
  width: 40%;
}

.form-left {
  position: absolute;
  left: 7%;
}

.form-right {
  position: absolute;
  right: 7%;
}

.reg-form ul {
  list-style: none;
  padding: 0;
}

.reg-form ul li {
  margin-bottom: 15px;
}

.reg-form ul li label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.reg-form ul li input[type="text"],
.reg-form ul li input[type="email"],
.reg-form ul li input[type="password"],
.reg-form ul li input[type="date"],
.reg-form ul li select {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.reg-form ul li input[type="checkbox"] {
  margin-right: 10px;
}

.reg-form ul li div {
  margin-bottom: 10px;
}

.reg-form ul li input[type="submit"] {
  margin-top: 30px;
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.reg-form ul li input[type="submit"]:hover {
  background-color: #218838;
}

#tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

#tags label {
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 4px;
}
</style>