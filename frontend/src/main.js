import { createApp } from 'vue'
import HomeComponent from './components/HomeComponent.vue'
import RegisterComponent from './components/RegisterComponent.vue'
import LoginComponent from './components/LoginComponent.vue'
import RecommendComponent from './components/RecommendComponent.vue'
import LuntanComponent from './components/LuntanComponent.vue'
import ActivitiesComponent from './components/ActivitiesComponent.vue'
import ProfileComponent from './components/ProfileComponent.vue'
import ChatComponent from './components/ChatComponent.vue'

const components = {
    '#home': HomeComponent,
    '#register': RegisterComponent,
    '#login': LoginComponent,
    '#recommend': RecommendComponent,
    '#luntan': LuntanComponent,
    '#activities': ActivitiesComponent,
    '#profile': ProfileComponent,
    '#chat': ChatComponent
};

Object.keys(components).forEach(id => {
    if (document.querySelector(id)) {
        createApp(components[id]).mount(id);
    }
});