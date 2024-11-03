<template>
  <div class="chat-container">
    <h1>与 {{ friend.name }} 聊天</h1>
    <div class="chat-window">
      <div class="message" v-for="message in messages" :key="message.id">
        <strong>{{ message.sender }}:</strong> {{ message.content }}
      </div>
    </div>
    <div class="chat-input">
      <input type="text" v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息...">
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatComponent',
  data() {
    return {
      friend: {
        name: "李四"
      },
      messages: [
        { id: 1, sender: '我', content: '你好！' },
        { id: 2, sender: '李四', content: '你好，有什么可以帮忙的吗？' }
      ],
      newMessage: ''
    };
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() !== '') {
        try {
          const response = await fetch('http://23.184.88.52:8000/api/messages/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              sender: '我',
              content: this.newMessage,
              friendId: new URLSearchParams(window.location.search).get('friend_id')
            })
          });
          const message = await response.json();
          this.messages.push(message);
          this.newMessage = '';
        } catch (error) {
          console.error('发送消息失败:', error);
        }
      }
    }
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    const friendId = urlParams.get('friend_id');
    // 获取好友信息（假设从服务器获取）
    // this.fetchFriendInfo(friendId);
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
.chat-container {
  max-width: 500px;
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
.chat-window {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
}
.message {
  margin: 10px 0;
}
.chat-input {
  display: flex;
}
.chat-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}
.chat-input button {
  padding: 10px 20px;
  background-color: #007BFF;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
}
.chat-input button:hover {
  background-color: #0056b3;
}
</style>