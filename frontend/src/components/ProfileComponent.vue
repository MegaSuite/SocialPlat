<template>
    <div class="container">
        <div id="logo">
            <h1 class="logo">森林友约</h1>
            <a class="CTA" href="index.html">
                <h1>返回主页</h1>
            </a>
        </div>
        <div class="leftbox">
            <nav>
                <a id="profiles" class="active"><span class="iconfont">&#xe636;</span></a>
                <a id="editing"><span class="iconfont">&#xe63b;</span></a>
                <a id="myImage"><span class="iconfont">&#xe623;</span></a>
                <a id="friends"><span class="iconfont">&#xe644;</span></a>
                <a id="message"><span class="iconfont">&#xe61f;</span></a>
            </nav>
        </div>
        <div class="rightbox" id="app">
            <div class="profiles">
                <h1>个人资料</h1>
                <h2>姓名</h2>
                <p>{{ user.name }}</p>
                <h2>生日</h2>
                <p>{{ user.dobYear }}-{{ user.dobMonth }}-{{ user.dobDay }}</p>
                <h2>性别</h2>
                <p>{{ user.gender }} {{ user.customGender }}</p>
                <h2>专业</h2>
                <p>{{ user.job }}</p>
                <h2>联系方式</h2>
                <p>{{ user.contact }}</p>
                <h2>兴趣</h2>
                <p>
                    <span v-for="(hobby, index) in user.hobbies" :key="hobby">
                        {{ hobby }}<span v-if="index < user.hobbies.length - 1">， </span>
                    </span>
                </p>
            </div>
            <div class="editing noshow">
                <h1>编辑资料</h1>
                <form @submit.prevent="updateProfile" class="a11">
                    <label for="name" class="a1">姓名:</label>
                    <input type="text" v-model="formData.name" id="name" required />
                    <label for="contact" class="a1">联系方式:</label>
                    <input type="text" v-model="formData.contact" id="contact" required />
                    <label for="job" class="a1">专业:</label>
                    <input type="text" v-model="formData.job" id="job" required />
                    <label for="hobbies" class="a1">兴趣:</label>
                    <div id="tags">
                        <label v-for="tag in allHobbyTags" :key="tag">
                            <input type="checkbox" v-model="formData.hobbies" :value="tag"> {{ tag }}
                        </label>
                    </div>
                    <input type="submit" value="保存" class="btn">
                </form>
            </div>
            <div class="myImage noshow">
                <h1>上传头像</h1>
                <form @submit.prevent="uploadImage">
                    <label for="file-upload">选择文件</label>
                    <input type="file" id="file-upload" @change="onFileChange">
                    <input type="submit" value="上传" class="btn">
                </form>
                <div v-if="imageUrl">
                    <h2>预览头像</h2>
                    <img :src="imageUrl" alt="用户头像" style="width: 200px; height: 200px; border-radius: 50%;">
                </div>
            </div>
            <div class="friends noshow" v-if="friends.length">
                <h1>我的朋友</h1>
                <div v-for="friend in filteredFriends" :key="friend.id" class="friend-card">
                    <h2>{{ friend.name }}</h2>
                    <h2>专业</h2>
                    <p class="fjob">{{ friend.job }}</p>
                    <h2>兴趣</h2>
                    <p class="fhobby">
                        <span v-for="(hobby, index) in friend.hobbies" :key="index">
                            {{ hobby }}<span v-if="index < friend.hobbies.length - 1">， </span>
                        </span>
                    </p>
                    <button class="chat-btn" @click="openChat(friend.id)">聊天</button>
                </div>
                <div class="pagination">
                    <button @click="prevFriendsPage" :disabled="friendsCurrentPage === 1">上一页</button>
                    <button @click="nextFriendsPage" :disabled="friendsCurrentPage === totalFriendsPages">下一页</button>
                </div>
            </div>
            <div class="message noshow" v-if="friendRequests && friendRequests.length">
                <h1>好友请求</h1>
                <div v-for="request in filteredRequests" :key="request.id" class="friend-card">
                    <p><strong>{{ request.name }}</strong> 发来了好友请求</p>
                    <button class="accept-btn" @click="acceptFriendRequest(request)">接受</button>
                    <button class="decline-btn" @click="declineFriendRequest(request)">拒绝</button>
                </div>
                <div class="pagination">
                    <button @click="prevRequestsPage" :disabled="requestsCurrentPage === 1">上一页</button>
                    <button @click="nextRequestsPage"
                        :disabled="requestsCurrentPage === totalRequestsPages">下一页</button>
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
        id: '',
        name: '',
        job: '',
        contact: '',
        password: '',
        dobYear: '',
        dobMonth: '',
        dobDay: '',
        gender: '',
        customGender: '',
        hobbies: [],
        avatar: ''
      },
      friends: [],
      friendRequests: [],
      formData: { hobbies: [] },
      allHobbyTags: [
        '编程', '阅读', '旅行', '摄影', '音乐',
        '运动', '电影', '美食', '手工艺', '游戏',
        '瑜伽', '健身', '园艺', '宠物', '绘画',
        '写作', '舞蹈', '戏剧', '志愿服务', '烹饪',
        '钓鱼', '露营', '滑雪', '冲浪', '攀岩',
        '桌游', '卡牌游戏', '模型制作', '收藏', '天文'
      ],
      imageFile: null,
      imageUrl: '',
      friendsCurrentPage: 1,
      requestsCurrentPage: 1,
      itemsPerPage: 3,
      userToken: localStorage.getItem('token'),
      userId: localStorage.getItem('id')
    };
  },
  computed: {
    totalFriendsPages() {
      return Math.ceil(this.friends.length / this.itemsPerPage);
    },
    totalRequestsPages() {
      return Math.ceil(this.friendRequests.length / this.itemsPerPage);
    },
    filteredFriends() {
      const start = (this.friendsCurrentPage - 1) * this.itemsPerPage;
      const end = this.friendsCurrentPage * this.itemsPerPage;
      return this.friends.slice(start, end);
    },
    filteredRequests() {
      const start = (this.requestsCurrentPage - 1) * this.itemsPerPage;
      const end = this.requestsCurrentPage * this.itemsPerPage;
      return this.friendRequests.slice(start, end);
    }
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await fetch('http://social.caay.ru/api/users/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.userId,
            method: 'request'
          })
        });
        const data = await response.json();
        this.user = {
          id: data.user_id,
          name: data.user_name,
          job: data.user_job,
          contact: data.user_contact,
          password: data.user_password,
          dobYear: data.user_dob_year,
          dobMonth: data.user_dob_month,
          dobDay: data.user_dob_day,
          gender: data.user_gender,
          customGender: data.user_custom_gender,
          hobbies: data.user_hobbies,
          avatar: data.avatar
        };
        this.formData = {
          name: data.user_name,
          job: data.user_job,
          contact: data.user_contact,
          password: data.user_password,
          dobYear: data.user_dob_year,
          dobMonth: data.user_dob_month,
          dobDay: data.user_dob_day,
          gender: data.user_gender,
          customGender: data.user_custom_gender,
          hobbies: data.user_hobbies
        };
      } catch (error) {
        alert(`获取用户资料失败: ${error.message}`);
      }
    },
    async fetchFriends() {
      try {
        const response = await fetch('http://social.caay.ru/api/relation/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.userId,
            method: 'request'
          })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.friends = data.friends;
          this.friendRequests = data.friendRequests;
          this.user.avatar = data.avatar;
        } else {
          alert('获取好友关系失败');
        }
      } catch (error) {
        alert(`获取好友关系失败: ${error.message}`);
      }
    },
    async updateProfile() {
      if (!/^.{1,4}$/.test(this.formData.name)) {
        alert('姓名不能为空，且最多 4 个字符');
        return;
      }
      if (!/^\d{11}$|^\w+@\w+\.com$/.test(this.formData.contact)) {
        alert('联系方式应为 11 位手机号或有效邮箱地址');
        return;
      }
      if (!/^.{1,10}$/.test(this.formData.job)) {
        alert('专业不能为空，且最多 10 个字符');
        return;
      }
      if (this.formData.hobbies.length < 3 || this.formData.hobbies.length > 10) {
        alert('请至少选择三个兴趣标签，最多选择十个');
        return;
      }

      try {
        const response = await fetch('http://social.caay.ru/api/users/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.user.id,
            user_name: this.formData.name,
            user_job: this.formData.job,
            user_contact: this.formData.contact,
            user_password: this.formData.password,
            user_dob_year: this.formData.dobYear,
            user_dob_month: this.formData.dobMonth,
            user_dob_day: this.formData.dobDay,
            user_gender: this.formData.gender,
            user_custom_gender: this.formData.customGender,
            user_hobbies: this.formData.hobbies,
            method: 'renew'
          })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.user.name = this.formData.name;
          this.user.job = this.formData.job;
          this.user.contact = this.formData.contact;
          this.user.password = this.formData.password;
          this.user.dobYear = this.formData.dobYear;
          this.user.dobMonth = this.formData.dobMonth;
          this.user.dobDay = this.formData.dobDay;
          this.user.gender = this.formData.gender;
          this.user.customGender = this.formData.customGender;
          this.user.hobbies = this.formData.hobbies;
          alert('资料更新成功');
        } else {
          alert('更新资料失败');
        }
      } catch (error) {
        alert(`更新资料失败: ${error.message}`);
      }
    },
    async uploadImage() {
      if (!this.imageFile) {
        alert('请先选择一张图片');
        return;
      }
      const formData = new FormData();
      formData.append('avatar', this.imageFile);
      formData.append('user_id', this.user.id);
      formData.append('method', 'avatar');
      try {
        const response = await fetch('http://social.caay.ru/api/users/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
          },
          body: formData
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.user.avatar = data.avatar;
          alert('头像上传成功');
        } else {
          alert('头像上传失败');
        }
      } catch (error) {
        alert(`头像上传失败: ${error.message}`);
      }
    },
    async acceptFriendRequest(request) {
      try {
        const response = await fetch('http://social.caay.ru/api/relation/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.user.id,
            friend_request_id: request.id,
            method: 'Accept'
          })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.friends = data.friends;
          this.friendRequests = this.friendRequests.filter(req => req.id !== request.id);
          alert('好友请求已接受');
        } else {
          alert('接受好友请求失败');
        }
      } catch (error) {
        alert(`接受好友请求失败: ${error.message}`);
      }
    },
    async declineFriendRequest(request) {
      try {
        const response = await fetch('http://social.caay.ru/api/relation/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.userToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.user.id,
            friend_request_id: request.id,
            method: 'Refuse'
          })
        });
        const data = await response.json();
        if (data.message === 'Success') {
          this.friendRequests = this.friendRequests.filter(req => req.id !== request.id);
          alert('好友请求已拒绝');
        } else {
          alert('拒绝好友请求失败');
        }
      } catch (error) {
        alert(`拒绝好友请求失败: ${error.message}`);
      }
    },
    onFileChange(e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        this.imageFile = file;
        this.imageUrl = URL.createObjectURL(file);
      } else {
        alert('请选择一个有效的图片文件');
      }
    },
    openChat(friendId) {
      const userId = this.user.id;
      window.open(`chat.html?friendId=${friendId}&userId=${userId}`, '_blank');
    },
    nextFriendsPage() {
      if (this.friendsCurrentPage < this.totalFriendsPages) {
        this.friendsCurrentPage++;
      }
    },
    prevFriendsPage() {
      if (this.friendsCurrentPage > 1) {
        this.friendsCurrentPage--;
      }
    },
    nextRequestsPage() {
      if (this.requestsCurrentPage < this.totalRequestsPages) {
        this.requestsCurrentPage++;
      }
    },
    prevRequestsPage() {
      if (this.requestsCurrentPage > 1) {
        this.requestsCurrentPage--;
      }
    },
    checkLogin() {
      if (!this.userToken) {
        alert('请先登录');
        window.location.href = 'login.html';
      } else {
        this.fetchUserProfile();
        this.fetchFriends();
      }
    }
  },
  mounted() {
    this.checkLogin();

    // 重写导航事件
    document.querySelectorAll('nav a').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        document.querySelectorAll('nav a').forEach(navLink => {
          navLink.classList.remove('active');
        });
        e.currentTarget.classList.add('active');
        document.querySelectorAll('.rightbox > div').forEach(box => {
          box.classList.add('noshow');
        });
        document.querySelector(`.${e.currentTarget.id}`).classList.remove('noshow');
      });
    });
  }
};
</script>

<style>
        @import url('iconfont.css');
        @import url('https://fonts.googleapis.com/css?family=Nunito:400,900|Montserrat|Roboto');

        body {
            background: linear-gradient(to right, #3FB6A8, #7ED386);
            font-family: 'Nunito', sans-serif;
        }

        .container {
            background: #FFFFFF;
            width: 800px;
            height: 750px;
            margin: 80px auto;
            position: relative;
            box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
        }

        .logo {
            float: right;
            margin-right: 12px;
            margin-top: 12px;
            font-family: 'Nunito', sans-serif;
            color: #3DBB3D;
            font-weight: 900;
            font-size: 1.5em;
            letter-spacing: 1px;
        }

        .CTA {
            width: 80px;
            height: 40px;
            right: -20px;
            bottom: 250px;
            text-decoration: none;
            margin-bottom: 90px;
            position: absolute;
            z-index: 1;
            background: #7ED386;
            font-size: 1em;
            transform: rotate(-90deg);
            transition: all .5s ease-in-out;
            cursor: pointer;
        }

        .CTA h1 {
            color: #FFFFFF;
            font-size: 1em;
            margin-top: 10px;
            margin-left: 9px;
        }

        .active {
            color: #3FB6A8;
        }

        .CTA:hover {
            background: #3FB6A8;
            transform: scale(1.1);
        }

        .leftbox {
            float: left;
            top: -5%;
            left: 5%;
            position: absolute;
            width: 15%;
            height: 110%;
            background: #7ED386;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, .5);
        }

        .rightbox {
            float: right;
            width: 60%;
            height: 100%;
        }

        h1 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-top: 40px;
            margin-bottom: 35px;
        }

        h2 {
            color: #777777;
            font-family: 'Roboto', sans-serif;
            width: 80%;
            text-transform: uppercase;
            font-size: 16px;
            letter-spacing: 1px;
            margin-left: 2px;
        }

        p {
            border-width: 1px;
            border-style: solid;
            border-image: linear-gradient(to right, #3FB6A8, #7ED386) 10%;
            border-top: 0;
            border-left: 0;
            border-right: 0;
            width: 80%;
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            padding: 7px 0;
            color: #070707;
        }

        .btn {
            width: 80px;
            height: 40px;
            right: 50px;
            bottom: -140px;
            text-decoration: none;
            margin-bottom: 90px;
            position: absolute;
            background: #7ED386;
            font-size: 1em;
            transition: all .5s ease-in-out;
            cursor: pointer;
            color: #FFFFFF;
            font-size: 1em;
            margin-top: 10px;
            margin-left: 9px;
            outline: none;
            font-weight: bold;
        }

        nav a {
            list-style: none;
            padding: 35px;
            color: #FFFFFF;
            font-size: 1.1em;
            display: block;
            transition: all .3s ease-in-out;

            &:hover {
                color: #3FB6A8;
                transform: scale(1.2);
                cursor: pointer;
            }

            &:first-child {
                margin-top: 60px;
            }
        }

        nav a .iconfont {
            font-size: 48px;
        }

        .profiles,
        .friends,
        .editing,
        .myImage,
        .message {
            position: absolute;
            width: 70%;
            left: 30%;
            transition: opacity .5s ease-in;
            position: absolute;
            width: 70%;
        }

        @font-face {
            font-family: 'iconfont';
            src: url('iconfont.woff2?t=1730007293898') format('woff2'),
                url('iconfont.woff?t=1730007293898') format('woff'),
                url('iconfont.ttf?t=1730007293898') format('truetype');
        }

        .iconfont {
            font-family: "iconfont" !important;
            font-size: 64px;
            font-style: normal;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .noshow {
            display: none;
        }

        .editing .a1 {
            display: block;
            font-weight: bold;
            margin-block-start: 0.83em;
            margin-block-end: 0.83em;
            color: #777777;
            font-family: 'Roboto', sans-serif;
            width: 80%;
            text-transform: uppercase;
            font-size: 16px;
            letter-spacing: 1px;
            margin-left: 2px;
        }

        .editing #tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .editing #tags label {
            background-color: #e9ecef;
            padding: 5px 10px;
            border-radius: 4px;
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

        .editing input[type=text] {
            outline: none;
            border-width: 1px;
            border-style: solid;
            border-image: linear-gradient(to right, #3FB6A8, #7ED386) 10%;
            width: 80%;
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            padding: 7px 0;
            color: #070707;
        }

        .friends h1 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-bottom: 35px;
        }

        .friend-card {
            position: relative;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 30px;
            width: 80%;
            height: 100px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, .1);
        }

        .friend-card h2 {
            color: #3FB6A8;
            width: 80px;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            margin-top: 0;
        }

        .friend-card p {
            position: absolute;
            border-width: 1px;
            border-style: solid;
            border-image: linear-gradient(to right, #3FB6A8, #7ED386) 10%;
            border-top: 0;
            border-left: 0;
            border-right: 0;
            width: 400px;
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            padding: 5px 0;
            color: #070707;
        }

        .friend-card .fhobby {
            top: 63px;
            left: 60px;
        }

        .friend-card .fjob {
            top: 28px;
            left: 60px;
        }

        .friends .friend-card:last-child {
            margin-bottom: 0;
        }

        .myImage {
            width: 70%;
            left: 30%;
            transition: opacity .5s ease-in;
            position: absolute;
        }

        .myImage h1 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-top: 40px;
            margin-bottom: 35px;
        }

        .myImage form {
            font-family: 'Roboto', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .myImage form input[type="file"] {
            margin: 20px 0;
        }

        .btn:hover {
            background: #3FB6A8;
            transform: scale(1.1);
        }

        .myImage img {
            margin-right: 50%;
            translate: 70%;
            margin-top: 20px;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
        }

        .myImage form input[type="file"] {
            width: 200px;
            height: 40px;
            opacity: 0;
            position: relative;
            cursor: pointer;
        }

        .myImage form label {
            margin-left: -10%;
            margin-top: 30px;
            background: #7ED386;
            color: #FFFFFF;
            display: inline-block;
            padding: 10px 20px;
            font-size: 1em;
            text-align: center;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }

        .myImage .btn {
            bottom: -180px;
            right: 50%;
        }

        .myImage form label:hover {
            background: #3FB6A8;
            transform: scale(1.1);
        }

        .message h2 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-bottom: 35px;
        }

        .friend-card {
            position: relative;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 30px;
            width: 80%;
            height: 100px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, .1);
        }

        .friend-card p {
            position: absolute;
            border-width: 1px;
            border-style: solid;
            border-image: linear-gradient(to right, #3FB6A8, #7ED386) 10%;
            border-top: 0;
            border-left: 0;
            border-right: 0;
            width: 400px;
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            padding: 5px 0;
            color: #070707;
        }

        .message .friend-card:last-child {
            margin-bottom: 0;
        }

        .accept-btn,
        .decline-btn {
            border-radius: 5px;
            position: absolute;
            top: 65px;
            width: 100px;
            height: 40px;
            background: #7ED386;
            font-size: 1em;
            transition: all .3s ease-in-out;
            cursor: pointer;
            color: #FFFFFF;
            font-weight: bold;
            border: none;
            margin: 10px 5px;
        }

        .accept-btn {
            left: 90px;
        }

        .decline-btn {
            left: 250px;
        }

        .accept-btn:hover,
        .decline-btn:hover {
            background: #3FB6A8;
            transform: scale(1.05);
        }

        .pagination {
            position: absolute;
            left: 25%;
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .pagination button {
            background: #7ED386;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 10px;
            cursor: pointer;
            font-size: 1em;
            font-family: 'Montserrat', sans-serif;
            transition: all .3s ease-in-out;
            border-radius: 5px;
        }

        .pagination button:disabled {
            background: #e9ecef;
            cursor: not-allowed;
        }

        .pagination button:hover:not(:disabled) {
            background: #3FB6A8;
        }

        .chat-btn {
            position: absolute;
            top: 5px;
            left: 390px;
            background: #7ED386;
            color: #FFFFFF;
            border: none;
            padding: 10px 20px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 1em;
            font-family: 'Montserrat', sans-serif;
            transition: all .3s ease-in-out;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }

        .chat-btn:hover {
            background: #3FB6A8;
            transform: scale(1.05);
        }
</style>