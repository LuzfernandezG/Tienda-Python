import { createRouter, createWebHistory } from 'vue-router';
import Login from './src/pages/inicio/InicialPage.vue';


import Dashboard from './src/pages/principal/DashboardPage.vue';
import Principal from './src/pages/principal/PrincipalPage.vue';
import Pago from './src/pages/principal/PagoPage.vue';



const routes = [
  { path: '/', component: Login },


  { path: '/dashboard', component: Dashboard ,
    children:[
      { path: 'principal', component:Principal},
      { path: 'pago', component:Pago},
   
    ]},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;