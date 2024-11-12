import { createRouter, createWebHistory } from 'vue-router';
import Login from './src/pages/inicio/InicialPage.vue';


import Dashboard from './src/pages/principal/DashboardPage.vue';
import Principal from './src/pages/principal/PrincipalPage.vue';
import Pago from './src/pages/principal/PagoPage.vue';
import Cliente from './src/pages/principal/ClientePage.vue';
import Panel from './src/pages/principal/PanelPage.vue';



const routes = [
  { path: '/', component: Login },


  { path: '/dashboard', component: Dashboard ,
    children:[
      { path: 'principal', component:Principal},
      { path: 'pago', component:Pago},
      { path: 'consultar', component:Cliente},
      { path: 'panel', component:Panel},
   
    ]},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;