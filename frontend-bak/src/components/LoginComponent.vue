<template>
    <div class="container">
        <h1>用户登录</h1>
        <p class="subtitle">快速又简便。</p>
        <hr>
        <div class="login">
            没有账号？<a href="register.html">去注册</a>
        </div>
        <form id="login" @submit.prevent="handleLogin">
            <div>
                <input type="text" v-model="formData.contact" id="contact" placeholder="手机号或邮箱" required />
            </div>
            <div>
                <input type="password" v-model="formData.password" id="password" placeholder="密码" required />
            </div>
            <button type="submit">登录</button>
        </form>
    </div>
</template>

<script>
export default {
        data() {
            return {
                formData: {
                    contact: '',
                    password: ''
                }
            };
        },
        methods: {
            async handleLogin() {
                try {
                    const response = await fetch('http://social.caay.ru/api/login/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            user_contact: this.formData.contact,
                            user_password: this.formData.password
                        })
                    });
                    const data = await response.json();
                    if (data.message === 'Success') {
                        localStorage.setItem('token', data.user_token);
                        localStorage.setItem('name', data.user_name);
                        localStorage.setItem('id', data.user_id);
                        alert('登录成功');
                        window.location.href = 'index.html'; // 跳转到个人资料页面
                    } else {
                        alert(`登录失败: ${data.message}`);
                    }
                } catch (error) {
                    alert(`登录失败: ${error.message}`);
                }
            }
        }
};
</script>

<style scoped>
        @import url('https://fonts.googleapis.com/css?family=Nunito:400,900|Montserrat|Roboto');

        body {
            background: linear-gradient(to right, #3FB6A8, #7ED386);
            font-family: 'Nunito', sans-serif;
            margin: 0;
            padding: 0;
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
            width: calc(100% + 40px);
            margin-left: -20px;
        }

        input[type="text"],
        input[type="password"] {
            outline: none;
            width: calc(100% - 20px);
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1.1em;
        }

        .login {
            text-align: right;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .login a {
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

        .login-link {
            text-align: center;
            margin-top: 20px;
        }

        .login-link a {
            color: #007BFF;
            text-decoration: none;
        }
</style>