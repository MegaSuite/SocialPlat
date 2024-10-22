<template>
  <div class="container">
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
      <div class="post" v-for="post in posts" :key="post.id">
        <h4>{{ post.title }}</h4>
        <p>{{ post.content }}</p>
        <p class="author">作者: {{ post.author }}</p>
        <div class="comments">
          <h5>评论</h5>
          <div v-for="comment in post.comments" :key="comment.id" class="comment">
            <p>{{ comment.content }}</p>
            <p class="author">评论者: {{ comment.author }}</p>
          </div>
          <form @submit.prevent="addComment(post.id)">
            <div class="form-group">
              <label for="comment">添加评论:</label>
              <textarea v-model="newComment[post.id]" id="comment" required></textarea>
            </div>
            <input type="submit" value="评论" class="comment-btn">
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ForumComponent',
  data() {
    return {
      newPost: {
        title: '',
        content: '',
        author: '当前用户'
      },
      posts: [],
      newComment: {} // 用于存储每个帖子的新增评论
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://23.184.88.52:8000/api/posts/');
        this.posts = response.data;
      } catch (error) {
        console.error('获取帖子失败:', error);
      }
    },
    async createPost() {
      try {
        const response = await axios.post('http://23.184.88.52:8000/api/posts/', this.newPost);
        this.posts.push(response.data);
        this.newPost.title = '';
        this.newPost.content = '';
      } catch (error) {
        console.error('发帖失败:', error);
      }
    },
    async addComment(postId) {
      try {
        const newComment = {
          content: this.newComment[postId],
          author: '当前用户'
        };
        const response = await axios.post(`http://23.184.88.52:8000/api/posts/${postId}/comments`, newComment);
        const post = this.posts.find(post => post.id === postId);
        post.comments.push(response.data);
        this.newComment[postId] = ''; // 清空输入框
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
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 90%;
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

.new-post {
  margin-bottom: 30px;
}

.new-post h3 {
  color: #333;
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
.form-group textarea {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.submit-btn,
.comment-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:hover,
.comment-btn:hover {
  background-color: #218838;
}

.posts {
  margin-top: 30px;
}

.post {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.post h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.post p {
  margin: 0;
  color: #555;
}

.post .author {
  margin-top: 10px;
  font-size: 14px;
  color: #777;
}

.comments {
  margin-top: 20px;
}

.comments h5 {
  margin: 0 0 10px 0;
  color: #444;
}

.comment {
  margin-bottom: 15px;
}

.comment p {
  margin: 0;
  color: #555;
}

.comment .author {
  margin-top: 5px;
  font-size: 14px;
  color: #777;
}
</style>
