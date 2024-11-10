import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from '../router.js'; 
import './style.css'

// Correcting the baseURL by removing the extra colon
axios.defaults.baseURL = 'http://127.0.0.1:8001/';
axios.defaults.withCredentials = true;

const app = createApp(App);

// Making Axios globally available in the app
app.config.globalProperties.$axios = axios;

app.use(router);

app.mount('#app');
