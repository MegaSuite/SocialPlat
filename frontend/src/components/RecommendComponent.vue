<template>
  <div class="container">
    <h1>选择你感兴趣的朋友！</h1>
    <div class="carousel-inner">
      <div v-for="friend in recommendations" :key="friend.user_id" class="friend-card">
        <img :src="friend.avatar_url" alt="用户头像">
        <div class="friend-info">
          <p><strong>名字:</strong> {{ friend.user_name }}</p>
          <p><strong>专业:</strong> {{ friend.user_job }}</p>
          <p><strong>兴趣:</strong> {{ friend.user_hobbies.join('、') }}</p>
        </div>
        <button class="add-friend-btn" @click="addFriend(friend.user_id)">添加好友</button>
      </div>
    </div>
    <button class="return-home-btn" @click="goHome">返回主页</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recommendations: []
    };
  },
  methods: {
    goHome() {
      this.$router.push('/'); // 跳转到主页
    },
    async fetchRecommendations() {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('id');
      if (token && userId) {
        try {
          const response = await fetch('http://social.caay.ru/api/recommend/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: userId
            })
          });
          const data = await response.json();
          if (data.message === 'Success') {
            this.recommendations = data.recommendations;
          } else {
            alert('获取推荐好友失败');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('获取推荐好友失败');
        }
      } else {
        alert('请先登录');
        this.$router.push('/login'); // 跳转到登录页面
      }
    },
    async addFriend(friendId) {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('id');
      if (token && userId) {
        try {
          const response = await fetch('http://social.caay.ru/api/relation/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: userId,
              friend_add: friendId,
              method: 'add'
            })
          });
          const data = await response.json();
          if (data.message === 'Success') {
            alert('好友添加成功');
          } else {
            alert('好友添加失败');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('好友添加失败');
        }
      } else {
        alert('请先登录');
        this.$router.push('/login'); // 跳转到登录页面
      }
    }
  },
  mounted() {
    this.fetchRecommendations(); // 获取推荐好友
  }
};
</script>

<style scoped>
        @import url('https://fonts.googleapis.com/css?family=Nunito:400,900|Montserrat|Roboto');

        body {
            background: linear-gradient(to right, #3FB6A8, #7ED386);
            font-family: 'Nunito', sans-serif;
        }

        .container {
            width: 100%;
            height: 100%;
            display: flex;
            flex-wrap: nowrap;
            overflow: hidden;
            flex-direction: column;
            align-items: center;
        }

        .carousel-inner {
            display: flex;
            width: 100%;
            animation: slide linear infinite;
        }

        .friend-card {
            width: 350px;
            height: 500px;
            display: flex;
            align-items: center;
            padding: 10px;
            margin-left: 80px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            flex-shrink: 0;
            flex-direction: column;
            align-items: center;
        }

        .friend-card img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin-bottom: 50px;
            margin-top: 50px;
        }

        .friend-info {
            height: 30%;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .friend-info p {
            margin: 5px 0;
            color: #555;
        }

        .add-friend-btn {
            margin-bottom: 50px;
            padding: 10px 20px;
            background-color: #7ED386;
            border: none;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }

        .add-friend-btn:hover {
            background-color: #5ba373;
        }

        .return-home-btn {
            margin-top: 40px;
            padding: 12px 24px;
            background-color: #7ED386;
            border: none;
            font-size: 1.2em;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }

        .return-home-btn:hover {
            background-color: #319e86;
        }

        /* 定义平移动画 */
        @keyframes slide {
            0% {
                transform: translateX(100%);
            }

            100% {
                transform: translateX(-110%);
            }
        }

        /* 暂停动画的类 */
        .paused {
            animation-play-state: paused;
        }

        h1 {
            color: #fff;
            margin-bottom: 30px;
            margin-top: 30px;
        }
</style>