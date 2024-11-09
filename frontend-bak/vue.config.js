const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html'
    },
    register: {
      entry: 'src/main.js',
      template: 'public/register.html',
      filename: 'register.html'
    },
    login: {
      entry: 'src/main.js',
      template: 'public/login.html',
      filename: 'login.html'
    },
    recommend: {
      entry: 'src/main.js',
      template: 'public/recommend.html',
      filename: 'recommend.html'
    },
    luntan: {
      entry: 'src/main.js',
      template: 'public/luntan.html',
      filename: 'luntan.html'
    },
    activities: {
      entry: 'src/main.js',
      template: 'public/activities.html',
      filename: 'activities.html'
    },
    profile: {
      entry: 'src/main.js',
      template: 'public/profile.html',
      filename: 'profile.html'
    },
    chat: {
      entry: 'src/main.js',
      template: 'public/chat.html',
      filename: 'chat.html'
    }
  }
})