<template>
    <div class="contenedor_grafico" v-if="visible">
      <div class="grafico">
        <h2>{{ nombre }}</h2>
        <canvas v-if="data.length" ref="productsChart"></canvas>
        <button @click="cerrar" class="boton-grafico">Cerrar</button>
      </div>
    </div>
  </template>
  
  <script>
  import { watch, onMounted, ref } from 'vue';
  import { Chart } from 'chart.js/auto';
  export default {
    name: 'Grafico',
    props: {
      nombre: String,
      mostrarGrafico: {
        type: Boolean,
        default: false
      },
      data: Array
    },
    setup(props, { emit }) {
      const productsChart = ref(null);
      const visible = ref(props.mostrarGrafico);
  
      watch(() => props.mostrarGrafico, (newValue) => {
        visible.value = newValue;
      });
  
  
  
      async function crearGraficoProductos(data) {
        console.log(data)
        if (!productsChart.value) return;
         
        const ctx = productsChart.value.getContext("2d");
        const labels = data.map((producto) => producto.fecha);
        const datos = data.map((producto) => producto.total);
  
        new Chart(ctx, {
          type: "line",
          data: {
            labels,
            datasets: [
              {
                label: "Resultado peticion",
                data: datos,
                backgroundColor: ["#FFD700", "#C0C0C0", "#CD7F32"],
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: (context) => `${context.raw} venta`,
                },
              },
            },
          },
        });
      }
  
      function cerrar() {
        emit('cerrar-modal');
      }
      watch(async () => {
        await crearGraficoProductos(props.data);
      });
  
      return {
        visible,
        productsChart,
        cerrar
      };
      
    }
  };
  </script>
  
  <style>
  .contenedor_grafico {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    display: flex;
    width: 100%;
    height: 100vh;
    align-items: center;
    justify-content: center;
  }
  
  .grafico {
    padding: 15px;
    background-color: #ffffff;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    z-index: 30;
    border: 1px solid #ff8c00;
    width: 1000px;
  }
  
  .boton-grafico{
    color: white;
    background-color: orange;
    border: none;
    padding: 1rem 2rem;
    border-radius: 1rem;
    font-size: 1rem;
  }
  </style>