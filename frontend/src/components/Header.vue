<template>
  <div class="header">
    <div style="display: flex; gap: 1rem; justify-content: center; align-items: center; padding-top: 10px;">
        <h1 style="font-size: 2rem; color: white;">
          <span style="color: orange">Mini</span>market
        </h1>
        <svg xmlns="http://www.w3.org/2000/svg" width="3em" height="3em" viewBox="0 0 48 48" style="color: orange">
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M39.048 29.602H22.615c-.645 0-1.142-.57-1.054-1.21l2.481-18.048a.613.613 0 0 0-.607-.696h-3.5" />
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M23.752 12.453h17.955c.47 0 .838.408.789.876l-1.002 9.55a2.024 2.024 0 0 1-2.012 1.812H22.07m-4.491-8.185H12.07m4.546 6.438H5.5" />
          <ellipse cx="21.66" cy="35.526" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" rx="3.086" ry="2.588" transform="rotate(-42.481 21.66 35.525)" />
          <ellipse cx="36.295" cy="35.526" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" rx="3.086" ry="2.588" transform="rotate(-42.481 36.295 35.526)" />
        </svg>
      </div>
    
      <div class="contenido">
        
         
          <router-link to="/dashboard/principal" style="text-decoration: none; color: white;">
              <svg xmlns="http://www.w3.org/2000/svg" class="cerrar" width="2em" height="2em" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M6 19h3.692v-5.884h4.616V19H18v-9l-6-4.538L6 10zm-1 1V9.5l7-5.288L19 9.5V20h-5.692v-5.884h-2.616V20zm7-7.77"/>
              </svg>
          </router-link>
          <router-link to="/dashboard/consultar" style="text-decoration: none; color: white;">
              <svg xmlns="http://www.w3.org/2000/svg" class="cerrar" width="2em" height="2em" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M18 20v-3h-3v-2h3v-3h2v3h3v2h-3v3zM3 21q-.825 0-1.412-.587T1 19V5q0-.825.588-1.412T3 3h14q.825 0 1.413.588T19 5v5h-2V8H3v11h13v2z"/>
              </svg>
          </router-link>
          <router-link to="/dashboard/panel" style="text-decoration: none; color: white;">
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24" class="cerrar">
	<path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.557 2.75H4.682A1.93 1.93 0 0 0 2.75 4.682v3.875a1.94 1.94 0 0 0 1.932 1.942h3.875a1.94 1.94 0 0 0 1.942-1.942V4.682A1.94 1.94 0 0 0 8.557 2.75m10.761 0h-3.875a1.94 1.94 0 0 0-1.942 1.932v3.875a1.943 1.943 0 0 0 1.942 1.942h3.875a1.94 1.94 0 0 0 1.932-1.942V4.682a1.93 1.93 0 0 0-1.932-1.932m0 10.75h-3.875a1.94 1.94 0 0 0-1.942 1.933v3.875a1.94 1.94 0 0 0 1.942 1.942h3.875a1.94 1.94 0 0 0 1.932-1.942v-3.875a1.93 1.93 0 0 0-1.932-1.932M8.557 13.5H4.682a1.943 1.943 0 0 0-1.932 1.943v3.875a1.93 1.93 0 0 0 1.932 1.932h3.875a1.94 1.94 0 0 0 1.942-1.932v-3.875a1.94 1.94 0 0 0-1.942-1.942" />
</svg>
          </router-link>
          <svg @click.prevent="logout" xmlns="http://www.w3.org/2000/svg" class="cerrar" width="2em" height="2em" viewBox="0 0 24 24">
              <path fill="currentColor" d="M5.616 20q-.691 0-1.153-.462T4 18.384V15.27h1v3.115q0 .231.192.424t.423.192h12.77q.23 0 .423-.192t.192-.424V5.616q0-.231-.192-.424T18.384 5H5.616q-.231 0-.424.192T5 5.616V8.73H4V5.616q0-.691.463-1.153T5.616 4h12.769q.69 0 1.153.463T20 5.616v12.769q0 .69-.462 1.153T18.384 20zm5.23-4.077l-.707-.72l2.703-2.703H4v-1h8.842L10.14 8.796l.707-.719L14.77 12z"/>
          </svg>
         
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { swallConfirmation, swallTrue, swallError } from "../../alerts.js";
import { useRouter } from 'vue-router'; 

export default {
name: 'Header', 
props: {
  nombre: {
    type: String,
    required: true
  }
},
setup() {
  // const router = useRouter();
  // const nombre = JSON.parse(localStorage.getItem('userData'));

  // const logout = async () => {
  //   const confirmacion = await swallConfirmation("¿Seguro que desea cerrar sesión?");
  //   if (confirmacion) {
  //     try {
  //       const response = await axios.get('/api/logout', { withCredentials: true });
        
  //       if (response && response.data && response.data.message) {
  //         console.log(response.data.message);
  //         swallTrue(response.data.message);
  //         localStorage.removeItem('userData');
  //         router.push("/");
  //       } else {
  //         console.error('Mensaje de respuesta no disponible');
  //         swallError('Error al cerrar sesión'); 
  //       }
  //     } catch (error) {
  //       console.error('Error al cerrar sesión:', error);
  //       swallError('Error al cerrar sesión'); 
  //     }
  //   }
  // };

  // return { logout,nombre};
}
};
</script>

<style>
.header {
  background-color: black; 
  width: 100%;
  padding: 0.5rem 3rem;
  display: flex;
  
}
.contenido {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
  color: white;
  width: 93%;
  position: fixed;
  padding-top: 1rem;
  transition: color 0.3s ease;
}
.cerrar:hover {
  color: orange;
}
.usuario{
  background-color: orange;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
}
.usuario:hover{
  background-color: rgb(134, 88, 3);
}
</style>
