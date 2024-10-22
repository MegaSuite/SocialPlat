import Vue from 'vue';
import VueRouter from 'vue-router';
import IndexComponent from '../components/IndexComponent.vue';
import LoginComponent from '../components/LoginComponent.vue';
import LuntanComponent from '../components/LuntanComponent.vue';
import ProfileComponent from '../components/ProfileComponent.vue';
import RegisterComponent from '../components/RegisterComponent.vue';

Vue.use(VueRouter);

const routes = [
    { path: '/', component: IndexComponent },
    { path: '/register', component: RegisterComponent },
    { path: '/login', component: LoginComponent },
    { path: '/profile', component: ProfileComponent },
    { path: '/forum', component: LuntanComponent }
];

const router = new VueRouter({
    routes
});

export default router;
