<template>
  <!-- Se añade la clase animar-contrato solo cuando 'animando' sea true -->
  <div :class="{'animar-contrato': animando}" class="contenedor_inicio">
    <div class="info_inicio">
      <div style="display: flex; gap: 1rem; justify-content: center; align-items: center" class="titulo">
        <h1 style="font-size: 6rem; color: white;">
          <span style="color: orange">Mini</span>market
        </h1>
        <svg xmlns="http://www.w3.org/2000/svg" width="8em" height="8em" viewBox="0 0 48 48" style="color: orange">
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M39.048 29.602H22.615c-.645 0-1.142-.57-1.054-1.21l2.481-18.048a.613.613 0 0 0-.607-.696h-3.5" />
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M23.752 12.453h17.955c.47 0 .838.408.789.876l-1.002 9.55a2.024 2.024 0 0 1-2.012 1.812H22.07m-4.491-8.185H12.07m4.546 6.438H5.5" />
          <ellipse cx="21.66" cy="35.526" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" rx="3.086" ry="2.588" transform="rotate(-42.481 21.66 35.525)" />
          <ellipse cx="36.295" cy="35.526" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" rx="3.086" ry="2.588" transform="rotate(-42.481 36.295 35.526)" />
        </svg>
      </div>
        <button class="boton-inicio" @click.prevent="cambio">Ingresar</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const animando = ref(false);
import { useRouter } from 'vue-router';
const router= useRouter();
const cambio = () => {
  // Activamos la animación
  animando.value = true;

  // Esperamos el tiempo de la animación (700ms) y luego redirigimos
  setTimeout(() => {
    // Si quieres hacer la redirección de forma programática:
    router.push('/dashboard/principal');
  }, 700); // Este es el tiempo que dura la animación de salida
};
</script>

<style scoped>
@keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

@keyframes tracking-out-contract {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 1;
  }
  100% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
}

.titulo {
  animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.610, 0.355, 1.000) both;
}

.contenedor_inicio {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.7s ease;
}

.info_inicio {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
  align-items: center;
}

.boton-inicio {
  animation: tracking-in-expand 0.7s cubic-bezier(0.215, 0.610, 0.355, 1.000) both;
  background-color: orange;
  padding: 1rem 6rem;
  color: white;
  border-radius: 2rem;
  font-size: 1rem;
  border: none;
  transition: background-color 1s ease;
}

.boton-inicio:hover {
  background-color: black;
  color: white;
}

/* Animación de contracción y desvanecimiento */
.animar-contrato {
  animation: tracking-out-contract 0.7s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
  opacity: 0;
}
</style>
