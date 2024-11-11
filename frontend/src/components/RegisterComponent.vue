<template>
    <div class="container">
        <h1>创建新用户</h1>
        <p class="subtitle">快速又简便。</p>
        <hr>
        <form id="register" @submit.prevent="handleSubmit">
            <div class="name-fields">
                <div class="input-wrapper">
                    <input type="text" id="name" v-model="formData.user_name" placeholder="姓名">
                    <span class="input-mark"><img src="image.png" alt=""></span>
                </div>
                <div class="input-wrapper">
                    <input type="text" id="job" v-model="formData.user_job" placeholder="专业">
                    <span class="input-mark"><img src="image.png" alt=""></span>
                </div>
            </div>
            <div class="input-wrapper">
                <input type="text" id="contact" v-model="formData.user_contact" placeholder="手机号或邮箱">
                <span class="input-mark"><img src="image.png" alt=""></span>
            </div>
            <div class="input-wrapper">
                <input type="password" id="password" v-model="formData.user_password" placeholder="创建密码">
                <span class="input-mark"><img src="image.png" alt=""></span>
            </div>
            <label class="icon">出生日期
                <div class="icon-box">
                    <img src="image.png" alt="图标">
                </div>
                <div class="tooltip" v-show="showTooltip0">点击查看更多信息</div>
                <div class="messages" v-show="showMessages0"><strong>提供你的出生日期</strong>将确保我们提供与你年龄相符的使用体验。详细信息，请参阅我们的<a href="#"
                        class="messagesLink">隐私权政策</a>。</div>
            </label>
            <div class="dob-fields">
                <select id="dobYear" v-model="formData.user_dob_year" ref="dobYear">
                    <option value="" disabled selected>年</option>
                    <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                </select>
                <select id="dobMonth" v-model="formData.user_dob_month" ref="dobMonth">
                    <option value="" disabled selected>月</option>
                    <option v-for="month in 12" :key="month" :value="month">{{ month }}</option>
                </select>
                <select id="dobDay" v-model="formData.user_dob_day" ref="dobDay">
                    <option value="" disabled selected>日</option>
                    <option v-for="day in daysInMonth" :key="day" :value="day">{{ day }}</option>
                </select>
            </div>
            <label class="icon">性别
                <div class="icon-box">
                    <img src="image.png" alt="图标">
                </div>
                <div class="tooltip" v-show="showTooltip1">点击查看更多信息</div>
                <div class="messages" v-show="showMessages1">如果你希望选择其他信息，或不想透露性别信息，请选择"自定义"。</div>
            </label>
            <div class="gender-fields">
                <label for="female">
                    女
                    <input type="radio" id="female" v-model="formData.user_gender" value="female">
                </label>
                <label for="male">
                    男
                    <input type="radio" id="male" v-model="formData.user_gender" value="male">
                </label>
                <label for="custom">
                    自定义
                    <input type="radio" id="custom" v-model="formData.user_gender" value="custom">
                </label>
            </div>
            <div class="input-wrapper custom-gender" v-show="formData.user_gender === 'custom'">
                <input type="text" id="customGender" v-model="formData.user_custom_gender" placeholder="请输入您的性别">
                <span class="input-mark"><img src="image.png" alt=""></span>
            </div>
            <label class="icon" for="hobby">兴趣:</label>
            <div id="tags">
                <label v-for="tag in allHobbyTags" :key="tag">
                    <input type="checkbox" v-model="formData.user_hobbies" :value="tag"> {{ tag }}
                </label>
            </div>
            <p class="terms">
                点击注册，即表示你同意接受我们的<a href="#">条款</a>、<a href="#">隐私权政策</a>和<a href="#">Cookie政策</a>。你可能会收到我们的短信通知，并可以随时退订。
            </p>
            <button type="submit" :disabled="isSubmitting">注册</button>
        </form>
        <div class="login-link">
            <a href="login.html">有账户了？</a>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        user_name: '',
        user_job: '',
        user_contact: '',
        user_password: '',
        user_dob_year: '',
        user_dob_month: '',
        user_dob_day: '',
        user_gender: 'female',
        user_custom_gender: '',
        user_hobbies: [],
        user_character: []
      },
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
                ],
      years: Array.from({ length: 150 }, (v, i) => new Date().getFullYear() - i),
      daysInMonth: [],
      isSubmitting: false, // 防止重复提交的状态
      showTooltip0: false,
      showTooltip1: false,
      showMessages0: false,
      showMessages1: false
    };
  },
  methods: {
    showTooltip(index) {
      this[`showTooltip${index}`] = true;
    },
    hideTooltip(index) {
      this[`showTooltip${index}`] = false;
    },
    toggleMessages(index) {
      this[`showMessages${index}`] = !this[`showMessages${index}`];
    },
    updateDays() {
      const year = +this.formData.user_dob_year;
      const month = +this.formData.user_dob_month;
      this.daysInMonth = [];
      if (year && month) {
        const daysInMonth = new Date(year, month, 0).getDate();
        this.daysInMonth = Array.from({ length: daysInMonth }, (v, i) => i + 1);
      }
    },
    validateFields() {
      const fields = [
        { field: this.formData.user_name, regex: /^.{1,10}$/, message: "姓名不能为空，且最多 10 个字符" },
        { field: this.formData.user_job, regex: /^.{1,10}$/, message: "专业不能为空，且最多 10 个字符" },
        { field: this.formData.user_contact, regex: /^\d{11}$|^\w+@\w+\.com$/, message: "手机号应为 11 位数字或有效邮箱地址" },
        { field: this.formData.user_password, regex: /^[\w]{6,16}$/, message: "密码应为 6 ~ 16 位数字、字母或下划线" }
      ];
      let allFilled = true;
      fields.forEach(obj => {
        const isValid = obj.regex.test(obj.field);
        if (!isValid || !obj.field) {
          alert(obj.message);
          allFilled = false;
        }
      });

      const customGender = this.formData.user_custom_gender;
      if (this.formData.user_gender === 'custom' && (!customGender || !/^.{1,4}$/.test(customGender))) {
        alert("自定义性别不能为空，且最多 4 个字符");
        allFilled = false;
      }

      return allFilled;
    },
    async handleSubmit() {
  if (!this.validateFields()) return;

  if (this.formData.user_hobbies.length < 3 || this.formData.user_hobbies.length > 10) {
    alert('请至少选择三个兴趣标签，最多选择十个');
    return;
  }

  if (this.formData.user_gender === 'custom' && !this.formData.user_custom_gender) {
    alert('请输入您的自定义性别');
    return;
  }

  // 将兴趣标签转换为数字
  const hobbyNumbers = this.formData.user_hobbies.map(hobby => this.allHobbyTags.indexOf(hobby) + 1);

  this.isSubmitting = true; // 防止重复提交

  try {
    const response = await fetch('https://api.caay.ru/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...this.formData,
        user_hobbies: hobbyNumbers
      })
    });
    const data = await response.json();
    if (data.message === 'Success') {
      alert('注册成功');
      window.location.href = 'login.html'; // 跳转到登录页面
    } else {
      alert(`注册失败: ${data.message}`);
    }
  } catch (error) {
    alert(`注册失败: ${error.message}`);
  } finally {
    this.isSubmitting = false; // 重置提交状态
  }
}

  },
  mounted() {
    const yearSelect = this.$refs.dobYear;
    const currentYear = new Date().getFullYear();
    for (let i = currentYear; i >= currentYear - 150; i--) {
      yearSelect.appendChild(new Option(i, i));
    }

    const monthSelect = this.$refs.dobMonth;
    for (let i = 1; i <= 12; i++) {
      monthSelect.appendChild(new Option(i, i));
    }

    this.$refs.dobYear.addEventListener('change', this.updateDays);
    this.$refs.dobMonth.addEventListener('change', this.updateDays);
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
            background: #FFFFFF;
            width: 600px;
            margin: 50px auto;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
        }

        h1 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-bottom: 5px;
            margin-top: 0;
            text-align: center;
        }

        .subtitle {
            text-align: center;
            font-size: 16px;
            color: #aaa;
            margin-top: 0;
        }

        hr {
            margin: 20px 0;
            border: 0;
            border-top: 1px solid #aaa;
        }

        input[type="text"],
        input[type="password"],
        select {
            width: calc(100% - 20px);
            margin-bottom: 0.5em;
            padding: 0.5em;
            border: 1px solid #ccc;
            border-radius: 0.25em;
            font-size: 1.1em;
            outline: none;
        }

        label,
        .gender-fields label {
            display: block;
            margin-bottom: 0.5em;
            font-family: 'Roboto', sans-serif;
            font-size: 1.1em;
            color: #777777;
        }

        .gender-fields,
        .dob-fields {
            display: flex;
            justify-content: space-between;
            flex-wrap: nowrap;
        }

        .gender-fields label,
        .dob-fields select {
            display: flex;
            align-items: center;
            padding: 0.5em;
            color: #000;
            border: 1px solid #ccc;
            border-radius: 0.25em;
            margin-right: 10px;
            width: 33%;
            justify-content: space-between;
            font-size: 1.1em;
        }

        input[type="text"]::placeholder,
        input[type="password"]::placeholder {
            color: #aaa;
        }

        .custom-gender {
            display: none;
            width: calc(100% - 20px);
            margin-top: 10px;
        }

        .terms {
            font-size: 14px;
            color: #aaa;
            text-align: center;
            margin-top: 0;
        }

        .terms a {
            color: #003366;
            text-decoration: none;
        }

        .login-link {
            text-align: center;
            margin-top: 20px;
        }

        .login-link a {
            color: #007BFF;
            text-decoration: none;
        }

        .messagesLink {
            color: #007BFF;
            text-decoration: none;
        }

        button[type="submit"] {
            display: block;
            margin: 0 auto;
            background-color: #7ED386;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1.1em;
            cursor: pointer;
            font-weight: bold;
            width: 50%;
            margin-top: 20px;
        }

        .input-wrapper .error {
            border: 1px solid red;
        }

        .input-wrapper {
            position: relative;
            display: block;
            margin-bottom: 0.5em;
        }

        .input-wrapper input {
            width: calc(100% - 20px);
        }

        .input-mark {
            display: none;
            position: absolute;
            top: 20px;
            right: 10px;
            transform: translateY(-50%);
            color: white;
            width: 20px;
            height: 20px;
            text-align: center;
            overflow: hidden;
        }

        .input-wrapper img {
            width: 100%;
            height: auto;
            position: absolute;
            top: 170%;
            right: 0px;
            transform: translateY(-50%);
        }

        .icon {
            position: relative;
        }

        .icon-box {
            display: inline-block;
            position: relative;
            top: 5px;
            width: 20px;
            height: 20px;
            overflow: hidden;
        }

        .icon-box img {
            position: absolute;
            top: -50px;
            right: 0px;
            width: 100%;
            height: auto;
        }

        .tooltip {
            display: none;
            position: absolute;
            background-color: black;
            color: white;
            padding: 5px;
            border-radius: 3px;
            top: 136%;
            left: 14%;
            transform: translateX(-50%);
            white-space: nowrap;
            z-index: 10;
        }

        .messages {
            display: none;
            position: absolute;
            background-color: white;
            padding: 10px;
            color: grey;
            box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 0.2);
            width: 373px;
            left: -67%;
            top: 5%;
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
