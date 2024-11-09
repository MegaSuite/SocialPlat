<template>
  <div id="app" class="container">
    <h1>校园论坛</h1>
    <div class="new-post">
      <h3>发新帖</h3>
      <form @submit.prevent="createPost">
        <div class="form-group">
          <label for="title">标题:</label>
          <input type="text" v-model="newPost.post_title" id="title" required />
        </div>
        <div class="form-group">
          <label for="content">内容:</label>
          <textarea v-model="newPost.post_content" id="content" required></textarea>
        </div>
        <input type="submit" value="发帖" class="submit-btn">
      </form>
    </div>
    <div class="posts">
      <h3>帖子列表</h3>
      <div class="post" v-for="post in posts" :key="post.post_id">
        <h4>{{ post.post_title }}</h4>
        <p>{{ post.post_content }}</p>
        <p class="author">作者: {{ post.post_author }}</p>
        <div class="comments">
          <h5>评论</h5>
          <div v-for="comment in post.post_comments" :key="comment.comment_id" class="comment">
            <p>{{ comment.comment_content }}</p>
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
                    try {
                        const response = await fetch('https://api.caay.ru/avatar/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            body: JSON.stringify({
                                user_id: userId,
                                method: 'request'
                            })
                        });
                        const data = await response.json();
                        if (data.message === 'Success') {
                            return data.avatar; // 返回头像URL
                        } else {
                            throw new Error('获取头像失败');
                        }
                    } catch (error) {
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
</style>