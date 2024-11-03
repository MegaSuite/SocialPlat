<template>
  <div class="container">
    <h1>选择你感兴趣的朋友！</h1>
    <div class="carousel-inner">
      <div class="friend-card" v-for="friend in friends" :key="friend.user_id">
        <img :src="friend.avatar_url" :alt="friend.user_name">
        <div class="friend-info">
          <p><strong>名字:</strong> {{ friend.user_name }}</p>
          <p><strong>专业:</strong> {{ friend.user_job }}</p>
          <p><strong>兴趣:</strong> {{ friend.user_hobbies.join(', ') }}</p>
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
      friends: [],
      userToken: localStorage.getItem('token'),
      userId: localStorage.getItem('id')
    };
  },
  methods: {
    async fetchRecommendations() {
      try {
        const response = await fetch('http://23.184.88.52:8000/api/recommendations/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.userToken}`
          },
          body: JSON.stringify({ user_id: this.userId })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.friends = data.recommendations;
        } else {
          alert('Failed to fetch recommendations.');
        }
      } catch (error) {
        alert(`Failed to fetch recommendations: ${error.message}`);
      }
    },
    async addFriend(friendId) {
      try {
        const response = await fetch('http://23.184.88.52:8000/api/relation/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.userToken}`
          },
          body: JSON.stringify({
            user_id: this.userId,
            friend_add: friendId,
            method: 'add'
          })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          alert('好友添加成功');
        } else {
          alert('添加好友失败');
        }
      } catch (error) {
        alert(`添加好友失败: ${error.message}`);
      }
    },
    goHome() {
      window.location.href = 'index.html';
    },
    checkLogin() {
      if (!this.userToken || !this.userId) {
        alert('请先登录');
        window.location.href = 'login.html';
      } else {
        this.fetchRecommendations();
      }
    }
  },
  created() {
    this.checkLogin();
  },
  mounted() {
    let friendcards = document.querySelectorAll(".friend-card");
    let carouselinner = document.querySelector(".carousel-inner");
    // 设置每个卡片的宽度
    carouselinner.style.width = friendcards.length * 430 + 'px';
    carouselinner.style.animationDuration = friendcards.length * 3 + 's';
    // 添加鼠标移入和移出事件监听器
    friendcards.forEach(card => {
      card.addEventListener("mouseover", () => {
        carouselinner.classList.add("paused");
      });
      card.addEventListener("mouseout", () => {
        carouselinner.classList.remove("paused");
      });
    });
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