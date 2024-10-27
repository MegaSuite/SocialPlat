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
        <p><strong>兴趣:</strong> <span v-for="hobby in user.hobbies" :key="hobby">{{ hobby }}</span></p>
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
            <div id="tags">
              <label v-for="tag in allHobbyTags" :key="tag">
                <input type="checkbox" v-model="formData.hobbies" :value="tag"> {{ tag }}
              </label>
            </div>
          </div>
          <input type="submit" value="保存" class="submit-btn">
          <button @click="cancelEdit">取消</button>
        </form>
      </div>
      <div class="friends-list">
        <h3>好友列表</h3>
        <div class="friend-card" v-for="friend in friends" :key="friend.id">
          <div class="friend-info">
            <p><strong>名字:</strong> {{ friend.name }}</p>
            <p><strong>专业:</strong> {{ friend.job }}</p>
            <p><strong>兴趣:</strong> {{ friend.hobbies.join(', ') }}</p>
          </div>
          <button @click="startChat(friend)" class="chat-btn">聊天</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: '',
        birth_date: '',
        gender: '',
        job: '',
        hobbies: []
      },
      friends: [],
      isEditing: false,
      formData: {},
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
    editProfile() {
      this.isEditing = true;
      this.formData = { ...this.user };
    },
    async updateProfile() {
      try {
        const response = await fetch('http://23.184.88.52:8000/api/users/1', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        const data = await response.json();
        this.user = data;
        this.isEditing = false;
      } catch (error) {
        console.error('更新资料失败:', error);
      }
    },
    cancelEdit() {
      this.isEditing = false;
    },
    startChat(friend) {
      window.open(`chat.html?friend_id=${friend.id}`, '_blank', 'width=600,height=400');
    }
  },
  async mounted() {
    try {
      const response = await fetch('http://23.184.88.52:8000/api/users/1', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'fetch_user' })
      });
      this.user = await response.json();

      const friendsResponse = await fetch('http://23.184.88.52:8000/api/users/1/friends', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'fetch_friends' })
      });
      this.friends = await friendsResponse.json();
    } catch (error) {
      console.error('初始化用户数据失败:', error);
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
#tags {
  display: flex;
  flex-wrap: wrap;
}
#tags label {
  margin-right: 10px;
  margin-bottom: 5px;
}
#tags input {
  margin-right: 5px;
}
</style>