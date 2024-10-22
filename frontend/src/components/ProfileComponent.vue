<template>
  <div class="container">
    <h1>个人资料</h1>
    <div class="profile">
      <div class="profile-info">
        <h3>基本信息</h3>
        <p><strong>名字:</strong> {{ user.name }}</p>
        <p><strong>生日:</strong> {{ user.birth_date }}</p>
        <p><strong>性别:</strong> {{ user.gender }}</p>
        <p><strong>专业:</strong> {{ user.job }}</p>
        <p><strong>兴趣:</strong> {{ user.hobbies.join(', ') }}</p>
        <button @click="editProfile">编辑资料</button>
      </div>
      <div v-if="isEditing" class="edit-profile">
        <h3>编辑资料</h3>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="name">名字:</label>
            <input type="text" v-model="formData.name" id="name" required />
          </div>
          <div class="form-group">
            <label for="birth-date">生日:</label>
            <input type="date" v-model="formData.birth_date" id="birth-date" required />
          </div>
          <div class="form-group">
            <label for="gender">性别:</label>
            <input type="text" v-model="formData.gender" id="gender" required />
          </div>
          <div class="form-group">
            <label for="job">专业:</label>
            <input type="text" v-model="formData.job" id="job" required />
          </div>
          <div class="form-group">
            <label for="hobbies">兴趣:</label>
            <textarea v-model="formData.hobbies" id="hobbies" required></textarea>
          </div>
          <input type="submit" value="保存" class="submit-btn">
          <button @click="cancelEdit">取消</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      user: {},
      isEditing: false,
      formData: {}
    };
  },
  methods: {
    async fetchUser() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://23.184.88.52:8000/api/users/1', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.user = response.data;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        alert('请先登录');
        this.$router.push('/login'); // 使用 Vue Router 导航
      }
    },
    editProfile() {
      this.isEditing = true;
      this.formData = { ...this.user };
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.put('http://23.184.88.52:8000/api/users/1', this.formData, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.user = response.data;
        this.isEditing = false;
      } catch (error) {
        console.error('更新资料失败:', error);
      }
    },
    cancelEdit() {
      this.isEditing = false;
    }
  },
  mounted() {
    this.fetchUser();
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

.profile {
  margin-top: 30px;
}

.profile-info {
  text-align: left;
}

.profile-info h3 {
  color: #333;
}

.profile-info p {
  color: #555;
  margin: 10px 0;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.edit-profile {
  margin-top: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group textarea {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.submit-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #218838;
}
</style>
