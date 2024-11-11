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
      recommendations: [],
      allHobbyTags: [
                    '环保生活方式', '漫画', '网络漫画', '编程', '演唱会粉丝',
                    '金融素养', '辩论俱乐部', '爵士音乐', '化装舞会', '科幻电影',
                    '跑酷', '虚拟现实体验', '龙与地下城', '主题公园', '奇幻书籍',
                    '网购', '日本流行音乐', '真实犯罪', '古典音乐', '宠物爱好者',
                    '摄影', '角色扮演', '怪物电影', '真人秀', '迷因',
                    '单口喜剧', '国际学生', '动漫粉丝', '鬼屋', '侦探故事',
                    '滑雪', '浪漫电影', '预算管理', '学术研究', '社交媒体',
                    '主题夜', '社会活动', '直播', '卡牌游戏', '创意写作',
                    '烹饪节目', '街头食品', '魔术表演', '心理健康意识', '水上运动',
                    '用户体验设计', '单板滑雪', '漫画', '嘻哈', '体育赛事',
                    '卡拉OK', '手机游戏', '志愿工作', '暑假', '科幻奇幻',
                    '海滩日', '正念', '健身目标', '滑板', '文化交流',
                    '超自然惊悚片', '节日', '独立游戏', '名人八卦', '社会正义',
                    '极限运动', '剧集狂看', '摇滚音乐', '恐怖故事', '人工智能开发',
                    '多人在线战术竞技游戏', '电影原声', '领导技能', '悬疑小说', '个人理财',
                    '美食博客', '社区服务', '实习搜索', '露营旅行', '旅行视频博客',
                    '独立音乐', '同人小说', '科幻书籍', '冥想练习', '电影马拉松',
                    '压力管理', '时间管理', '自然摄影', '平面设计', '职业规划',
                    '第一人称射击游戏', '角色扮演游戏', '机器学习', '公众演讲', '角色扮演',
                    '犯罪惊悚片', '喜剧电影', '生产力技巧', '简历制作', '电子竞技',
                    '数据科学', '奇幻电影', '批判性思维', '数字艺术', '恐怖电影',
                    '健康饮食', '项目管理', '城市探索', '自我提升', '戏剧电影',
                    '慈善活动', '密室逃脱', '桌游', '语言交换', '科学创新',
                    '学习小组', '流行音乐', '外国电影', '解谜游戏', '动作电影',
                    '韩国流行音乐', '解谜', '复古游戏', '哲学讨论', '网络活动',
                    '可持续发展', '复古电影', 'YouTube狂看'
                ]
    };
  },
  methods: {
    goHome() {
      window.location.href = 'index.html'; // 跳转到主页
    },
    async fetchRecommendations() {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('id');
      if (token && userId) {
        try {
          const response = await fetch('https://api.caay.ru/recommend/', { // 更新API端点URL
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: userId
            })
          });
          const data = await response.json();
          if (data.message === 'Success') {
            // 将推荐好友的 user_hobbies 数字转换为标签
            data.recommendations.forEach(recommendation => {
              recommendation.user_hobbies = recommendation.user_hobbies.map(hobbyNum => this.allHobbyTags[hobbyNum - 1]);
            });
            this.recommendations = data.recommendations;
          } else {
            alert('获取推荐好友失败1');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('获取推荐好友失败2');
        }
      } else {
        alert('请先登录');
        window.location.href = 'login.html'; // 跳转到登录页面
      }
    },
    async addFriend(friendId) {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('id');
      if (token && userId) {
        try {
          const response = await fetch('https://api.caay.ru/relation/', { // 更新API端点URL
            method: 'POST',
            headers: {
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
        window.location.href = 'login.html'; // 跳转到登录页面
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