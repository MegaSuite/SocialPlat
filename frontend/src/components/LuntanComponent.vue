<template>
  <div id="app" class="container">
    <h1>校园论坛</h1>
    <div class="new-post">
  <h3>发新帖</h3>
  <form @submit.prevent="createPost">
    <div class="form-group">
      <label for="title">标题:</label>
      <input type="text" v-model="newPost.title" id="title" required />
    </div>
    <div class="form-group">
      <label for="content">内容:</label>
      <textarea v-model="newPost.content" id="content" required></textarea>
    </div>
    <input type="submit" value="发帖" class="submit-btn">
  </form>
</div>
    <div class="posts">
      <h3>帖子列表</h3>
      <div class="post" v-for="post in posts" :key="post.post_id">
        <h4>
            <img :src="post.avatar_url" alt="用户头像" class="avatar">
            {{ post.post_title }}
        </h4>
        <button class="button">
        <div class="hand">
            <div class="thumb"></div>
        </div>
        <span>Like<span>d</span></span>
    </button>
        <p>{{ post.post_content }}</p>
        <p class="author">作者: {{ post.post_author }}</p>
        <div class="comments">
          <h5>评论</h5>
          <div v-for="comment in post.post_comments" :key="comment.comment_id" class="comment">
            <p>
                <img :src="comment.avatar_url" alt="评论者头像" class="avatar">
                {{ comment.comment_content }}
            </p>
            <p class="author">评论者: {{ comment.comment_author }}</p>
          </div>
          <form @submit.prevent="addComment(post.post_id)">
            <div class="form-group">
              <label for="comment">添加评论:</label>
              <textarea v-model="newComment[post.post_id]" id="comment" required></textarea>
            </div>
            <input type="submit" value="评论" class="comment-btn">
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
            data() {
                return {
                    newPost: {
                        title: '',
                        content: '',
                        author: ''
                    },
                    posts: [],
                    newComment: {} // 用于存储每个帖子的新增评论
                };
            },
            methods: {

  async likePost(postId) {
    const userId = localStorage.getItem('id');

    try {
      const response = await fetch('https://api.caay.ru/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          post_id: postId,
          method: 'like'
        })
      });
      const data = await response.json();
      if (data.message === 'Success') {
        ;
      } else {
        alert('点赞失败');
      }
    } catch (error) {
      console.error('点赞失败:', error);
    }
  },

                async fetchPosts() {
                    // const token = localStorage.getItem('token');
                    const userId = localStorage.getItem('id');
                    try {
                        const response = await fetch('https://api.caay.ru/posts/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                user_id: userId,
                                method: 'all'
                            })
                        });
                        const data = await response.json();
                        if (data.message === 'Success') {
                            // 为每个帖子和评论获取头像
                            for (const post of data.posts) {
                                post.avatar_url = await this.fetchAvatar(post.post_author_id);
                                 for (const comment of post.post_comments) {
                                     comment.avatar_url = await this.fetchAvatar(comment.comment_author_id);
                                }
                            }
                            this.posts = data.posts;
                        } else {
                            alert('获取帖子失败');
                        }
                    } catch (error) {
                        console.error('获取帖子失败:', error);
                    }
                },
async fetchAvatar(userId) {
  const formData = new FormData();
  formData.append('user_id', userId);
  formData.append('method', 'request');

  try {
    const response = await fetch('https://api.caay.ru/avatar/', {
      method: 'POST',
      headers: {
      },
      body: formData
    });
    const data = await response.json();
    if (data.message === 'Success') {
        if (!data.avatar) {
          return "https://api.caay.ru/media/avatars/user-head_VKwZd0B.png";
        } else {
          return data.avatar; // 返回头像URL
        }
    } else {
      if (!data.avatar) return "https://api.caay.ru/media/avatars/user-head_VKwZd0B.png";
    }
  } 
  catch (error) {
    console.error('获取头像失败:', error);
  }
},
                async createPost() {
                    const token = localStorage.getItem('token');
                    const userId = localStorage.getItem('id');
                    if (!token) {
                        alert('请先登录');
                        window.location.href = 'login.html';
                        return;
                    }
                    this.newPost.author = userId; // 设置当前用户为作者
                    try {
                        const response = await fetch('https://api.caay.ru/posts/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                user_id: userId,
                                post_title: this.newPost.title,
                                post_content: this.newPost.content,
                                method: 'add'
                            })
                        });
                        const data = await response.json();
                        if (data.message === 'Success') {
                            this.posts.push({
                                post_id: data.post_id,
                                post_author: data.post_author,
                                post_title: this.newPost.title,
                                post_content: this.newPost.content,
                                post_comments: []
                            });
                            this.newPost.title = '';
                            this.newPost.content = '';
                        } else {
                            alert('发帖失败');
                        }
                    } catch (error) {
                        console.error('发帖失败:', error);
                    }
                },
                async addComment(postId) {
                    const token = localStorage.getItem('token');
                    const userId = localStorage.getItem('id');
                    if (!token) {
                        alert('请先登录');
                        window.location.href = 'login.html';
                        return;
                    }
                    try {
                        const newComment = {
                            comment_content: this.newComment[postId],
                            user_id: userId,
                            post_id: postId,
                            method: 'comment'
                        };
                        const response = await fetch(`https://api.caay.ru/posts/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(newComment)
                        });
                        const data = await response.json();
                        if (data.message === 'Success') {
                            const post = this.posts.find(post => post.post_id === postId);
                            post.post_comments.push({
                                comment_id: data.comment_id,
                                comment_content: newComment.comment_content,
                                comment_author: data.comment_author
                            });
                            this.newComment[postId] = ''; // 清空输入框
                        } else {
                            alert('评论失败');
                        }
                    } catch (error) {
                        console.error('评论失败:', error);
                    }
                }
            },
mounted() {
  this.fetchPosts();

  document.querySelectorAll('.button').forEach((button, index) => {
    button.addEventListener('click', () => {
      const postId = this.posts[index].post_id;
      if (!button.classList.contains('liked')) { // 如果按钮没有 'liked' 类，则执行
        button.classList.add('liked'); // 添加 'liked' 类
        this.likePost(postId); // 调用 likePost 方法
      }
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
            margin: 0;
            padding: 0;
        }

        .container {
            background: #FFFFFF;
            width: 800px;
            margin: 50px auto;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 2px 5px 20px rgba(0, 0, 0, .5);
        }

        h1 {
            font-family: 'Montserrat', sans-serif;
            color: #7ED386;
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
        }

        .new-post,
        .posts {
            margin-bottom: 30px;
        }

        textarea {
            resize: none;
        }

        .new-post h3,
        .posts h3 {
            font-family: 'Roboto', sans-serif;
            color: #3FB6A8;
            font-size: 1.5em;
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 1.1em;
            color: #777777;
        }

        input[type="text"],
        textarea {
            width: calc(100% - 20px);
            margin-bottom: 0.5em;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            outline: none;
            font-size: 1.1em;
        }

        textarea {
            height: 50px;
        }

        .submit-btn,
        .comment-btn {
            background-color: #7ED386;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1.1em;
            cursor: pointer;
            font-weight: bold;
            width: 100px;
            display: block;
            margin: 10px auto;
        }

        .post {
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, .1);
            position: relative;
        }

        .post h4 {
            font-family: 'Roboto', sans-serif;
            color: #3FB6A8;
            font-size: 1.5em;
            margin-bottom: 10px;
        }

        .post p {
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            color: #070707;
            margin-bottom: 10px;
        }

        .post .author {
            font-size: 0.9em;
            color: #aaa;
        }

        .comments {
            margin-top: 20px;
        }

        .comments h5 {
            font-family: 'Roboto', sans-serif;
            color: #3FB6A8;
            font-size: 1.2em;
            margin-bottom: 10px;
        }

        .comment {
            margin-bottom: 10px;
        }

        .comment p {
            font-family: 'Montserrat', sans-serif;
            font-size: 1em;
            color: #070707;
            margin-bottom: 5px;
        }

        .comment .author {
            font-size: 0.9em;
            color: #aaa;
        }

        .comment .comment-btn {
            margin-top: 10px;
            width: 100px;
        }

        /* 用户头像样式 */
        .avatar {
            width: 40px;
            /* 设定头像的宽度 */
            height: 40px;
            /* 设定头像的高度 */
            border-radius: 50%;
            /* 将头像设置为圆形 */
            margin-right: 10px;
            /* 添加右边距，防止文字与头像紧贴 */
            vertical-align: middle;
            /* 使头像与文字垂直对齐 */
        }

        /* 让头像图片在相应位置显示 */
        .post h4 .avatar,
        .post .author .avatar,
        .comment p .avatar,
        .comment .author .avatar {
            display: inline-block;
        }

        .avatar {
            width: 40px;
            /* 设定头像的宽度 */
            height: 40px;
            /* 设定头像的高度 */
            border-radius: 50%;
            /* 将头像设置为圆形 */
            margin-right: 10px;
            /* 添加右边距，防止文字与头像紧贴 */
            vertical-align: middle;
            /* 使头像与文字垂直对齐 */
        }

        /* 让头像图片在相应位置显示 */
        .post h4 .avatar,
        .post .author .avatar,
        .comment p .avatar,
        .comment .author .avatar {
            display: inline-block;
        }

        .button {
            top: 45px;
            left: 80%;
            --color: #3FB6A8;
            /* 改为与背景渐变颜色一致 */
            --color-hover: #3FB6A8;
            /* 改为与背景渐变颜色一致 */
            --color-active: #fff;
            --icon: #7ED386;
            /* 改为与背景渐变颜色一致 */
            --icon-hover: #5ba373;
            /* 改为与背景渐变颜色一致 */
            --icon-active: #fff;
            --background: #FFFFFF;
            /* 保持白色背景 */
            --background-hover: #FFFFFF;
            /* 保持白色背景 */
            --background-active: #22543D;
            /* 深绿色背景 */
            --border: #9AE6B4;
            /* 边框绿色 */
            --border-active: #22543D;
            /* 深绿色边框 */
            --shadow: rgba(56, 161, 105, .025);
            /* 绿色阴影 */
            display: block;
            outline: none;
            cursor: pointer;
            position: absolute;
            border: 0;
            background: none;
            padding: 8px 20px 8px 24px;
            border-radius: 9px;
            line-height: 27px;
            font-family: inherit;
            font-weight: 600;
            font-size: 14px;
            color: var(--color);
            -webkit-appearance: none;
            -webkit-tap-highlight-color: transparent;
            transition: color .2s linear;

            &.dark {
                --color: #F6F8FF;
                --color-hover: #F6F8FF;
                --color-active: #fff;
                --icon: #8A91B4;
                --icon-hover: #BBC1E1;
                --icon-active: #fff;
                --background: #1E2235;
                --background-hover: #171827;
                --background-active: #275EFE;
                --border: transparent;
                --border-active: transparent;
                --shadow: #{rgba(#001177, .16)};
            }

            &:hover {
                --icon: var(--icon-hover);
                --color: var(--color-hover);
                --background: var(--background-hover);
                --border-width: 2px;
            }

            &:active {
                --scale: .95;
            }

            &:not(.liked) {
                &:hover {
                    --hand-rotate: 8;
                    --hand-thumb-1: -12deg;
                    --hand-thumb-2: 36deg;
                }
            }

            &.liked {
                --span-x: 2px;
                --span-d-o: 1;
                --span-d-x: 0;
                --icon: var(--icon-active);
                --color: var(--color-active);
                --border: var(--border-active);
                --background: var(--background-active);
            }

            &:before {
                content: '';
                min-width: 103px;
                position: absolute;
                left: 0;
                top: 0;
                right: 0;
                bottom: 0;
                border-radius: inherit;
                transition: background .2s linear, transform .2s, box-shadow .2s linear;
                transform: scale(var(--scale, 1)) translateZ(0);
                background: var(--background);
                box-shadow: inset 0 0 0 var(--border-width, 1px) var(--border), 0 4px 8px var(--shadow), 0 8px 20px var(--shadow);
            }

            .hand {
                width: 11px;
                height: 11px;
                border-radius: 2px 0 0 0;
                background: var(--icon);
                position: relative;
                margin: 10px 8px 0 0;
                transform-origin: -5px -1px;
                transition: transform .25s, background .2s linear;
                transform: rotate(calc(var(--hand-rotate, 0) * 1deg)) translateZ(0);

                &:before,
                &:after {
                    content: '';
                    background: var(--icon);
                    position: absolute;
                    transition: background .2s linear, box-shadow .2s linear;
                }

                &:before {
                    left: -5px;
                    bottom: 0;
                    height: 12px;
                    width: 4px;
                    border-radius: 1px 1px 0 1px;
                }

                &:after {
                    right: -3px;
                    top: 0;
                    width: 4px;
                    height: 4px;
                    border-radius: 0 2px 2px 0;
                    background: var(--icon);
                    box-shadow: -.5px 4px 0 var(--icon), -1px 8px 0 var(--icon), -1.5px 12px 0 var(--icon);
                    transform: scaleY(.6825);
                    transform-origin: 0 0;
                }

                .thumb {
                    background: var(--icon);
                    width: 10px;
                    height: 4px;
                    border-radius: 2px;
                    transform-origin: 2px 2px;
                    position: absolute;
                    left: 0;
                    top: 0;
                    transition: transform .25s, background .2s linear;
                    transform: scale(.85) translateY(-.5px) rotate(var(--hand-thumb-1, -45deg)) translateZ(0);

                    &:before {
                        content: '';
                        height: 4px;
                        width: 7px;
                        border-radius: 2px;
                        transform-origin: 2px 2px;
                        background: var(--icon);
                        position: absolute;
                        left: 7px;
                        top: 0;
                        transition: transform .25s, background .2s linear;
                        transform: rotate(var(--hand-thumb-2, -45deg)) translateZ(0);
                    }
                }
            }

            .hand,
            span {
                display: inline-block;
                vertical-align: top;

                span {
                    opacity: var(--span-d-o, 0);
                    transition: transform .25s, opacity .2s linear;
                    transform: translateX(var(--span-d-x, 4px)) translateZ(0);
                }
            }

            &>span {
                transition: transform .25s;
                transform: translateX(var(--span-x, 4px)) translateZ(0);
            }
        }

        html {
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
        }

        * {
            box-sizing: inherit;

            &:before,
            &:after {
                box-sizing: inherit;
            }
        }

        @keyframes handRotate {
            0% {
                --hand-rotate: 8deg;
            }

            33% {
                --hand-rotate: -45deg;
            }

            66% {
                --hand-rotate: 15deg;
            }

            100% {
                --hand-rotate: 0;
            }
        }

        .button.liked {
            animation: handRotate 0.5s ease forwards;
        }
</style>