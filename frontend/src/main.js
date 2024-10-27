import { createApp } from 'vue'
import HomePage from './components/HomePage.vue'
import Register from './components/UserRegister.vue'
import Login from './components/UserLogin.vue'
import ItemRecommend from './components/ItemRecommend.vue'
import Luntan from './components/ForumLuntan.vue'
import UserActivities from './components/UserActivities.vue'
import Profile from './components/UserProfile.vue'
import Chat from './components/UserChat.vue'

const components = {
    '#home': HomePage,
    '#register': Register,
    '#login': Login,
    '#recommend': ItemRecommend,
    '#luntan': Luntan,
    '#activities': UserActivities,
    '#profile': Profile,
    '#chat': Chat
};

Object.keys(components).forEach(id => {
    if (document.querySelector(id)) {
        createApp(components[id]).mount(id);
    }
});
