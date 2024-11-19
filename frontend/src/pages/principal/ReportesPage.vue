<template>
  <Grafico nombre="Reporte" v-model:mostrarGrafico="mostrarGrafico" @cerrar-modal="mostrarGrafico = false" :data="respuesta"/>
  <div class="report-container">
    <div class="contenedor-reporte">
      <div class="report-selection">
        <h2>Consulta de datos</h2>
        <div class="report-options">
          <label for="report-type">Filtrar por:</label>
          <select v-model="consulta.tipo" id="report-type" class="select_report">
            <option value="day">Día</option>
            <option value="week">Semana</option>
            <option value="month">Mes</option>
          </select>
        </div>
        <div class="date-selection">
          <label for="report-date">Seleccionar Fecha:</label>
          <input type="date" v-model="consulta.fecha" id="report-date"  class="input_date"/>
        </div>
        <button @click="capturarData">Consultar</button>
      </div>
      <div class="report-selection2">
        <div style=" display: flex;gap:1rem; flex-direction: column">
          <h2>Top 3° categorías</h2>
          <canvas ref="categoriesChart" class="diagrama"></canvas>
       
          <!-- <p v-if="rankingData.topProducts.length">{{ rankingData.topProducts[0].name }} con {{ rankingData.topProducts[0].sales }} ventas</p> -->
        </div>
        <div
          style="display: flex; flex-direction: column; text-align: center; justify-content: center ;width: 100%; margin: 0 auto;">
          <svg xmlns="http://www.w3.org/2000/svg" width="9em" height="9em" viewBox="0 0 24 24"
            style="color: orange; text-align: center; width: 100%;">
            <path fill="currentColor"
              d="M7.308 21.116q-.633 0-1.067-.434t-.433-1.066t.433-1.067q.434-.433 1.067-.433t1.066.433t.434 1.067t-.434 1.066t-1.066.434m9.384 0q-.632 0-1.066-.434t-.434-1.066t.434-1.067q.434-.433 1.066-.433t1.067.433q.433.434.433 1.067q0 .632-.433 1.066q-.434.434-1.067.434M3.808 3.5H2.5q-.213 0-.356-.144T2 2.999t.144-.356T2.5 2.5h1.436q.239 0 .435.12t.294.34l3.88 8.156h6.634q.173 0 .308-.087q.134-.087.23-.24l3.356-6.039q.068-.115.18-.183T19.5 4.5q.285 0 .429.247q.143.247.003.497l-3.364 6.09q-.217.366-.565.574t-.762.208H8.1l-1.215 2.23q-.154.231-.01.5t.433.27h10.384q.213 0 .357.143q.143.144.143.357t-.143.356t-.357.144H7.308q-.875 0-1.309-.735t-.018-1.485l1.504-2.68zM12 9.5q-.261 0-.438-.177t-.177-.438t.177-.439T12 8.27t.439.177t.176.439t-.177.438T12 9.5m0-3q-.214 0-.357-.144T11.5 6V2q0-.213.144-.356t.357-.144t.356.144T12.5 2v4q0 .213-.144.356t-.357.144" />
          </svg>
          <h2>Producto menos vendido</h2>
          <p>{{ rankingData.leastProduct.nombre }} con
            <span v-if="rankingData.leastProduct.cantidad_total == null">0</span>
            <span v-else>{{ rankingData.leastProduct.cantidad_total }}</span>
            ventas
          </p>
        </div>
      </div>
    </div>
    <div class="contenedor-graficos">
      <div class="ranking-section">
        <h2>Ranking de Productos</h2>
        <canvas v-if="rankingData.topProducts.length" ref="productsChart"></canvas>

      </div>
      <div class="ranking-section">
        <h2>Ranking de Clientes</h2>
        <canvas v-if="rankingData.topClients.length" ref="clientsChart"></canvas>
        <div v-else>No hay datos disponibles para los clientes</div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';
import { DashboardGraficos } from '../../../api';
import { onMounted, ref, nextTick } from 'vue';
import { Consultar } from '../../../api';
import Grafico from '../../components/Grafico.vue';
import { swallError, swallTrue } from '../../../alerts';
export default {
  components: {
    Grafico
    
  },
  setup() {
    const rankingData = ref({
      topProducts: [],
      leastProduct: {},
      topClients: [],
      topCategories: []
    });
    const productsChart = ref(null);
    const clientsChart = ref(null);
    const categoriesChart = ref(null);
    const mostrarGrafico=ref(false);

    const consulta = ref({
      tipo: "",
      fecha: "",
    });

    const respuesta = ref([])
  

    async function traerInformacion() {
      try {
        const response = await DashboardGraficos();
        console.log(response)
        if (response && Array.isArray(response)) {
          const productos = response.filter((producto) => producto.tipo === "Más vendido");
          console.log(productos)
          const clientes = response.filter((producto) => producto.tipo === "Mejores_clientes");
          console.log(clientes)
          const menos = response.filter((producto) => producto.tipo === "Menos vendido");
          console.log(menos)
          const categories = response.filter((producto) => producto.tipo === "Mejores_categorias");
          console.log(categories)


          rankingData.value = {
            topProducts: productos,
            leastProduct: menos[0],
            topClients: clientes,
            topCategories: categories
          };
        }
      } catch (error) {
        console.error("Error al obtener los datos:", error);
      }
    }

    // Inicializar los gráficos cuando el componente se monta

    async function crearGraficoProductos() {
      // Verifica que haya datos disponibles antes de renderizar el gráfico
      if (!rankingData.value.topProducts.length) return;

      // Espera a que el DOM esté actualizado
      await nextTick();

      const productosVendidos = rankingData.value.topProducts;
      console.log(productosVendidos)
      const labels = productosVendidos.map((producto) => producto.nombre);
      const data = productosVendidos.map((producto) => producto.cantidad_total);

      // Obtiene el contexto del canvas para crear el gráfico
      const ctx = productsChart.value.getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Productos más vendidos",
              data,
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
                label: (context) => `${context.raw} vendidos`,
              },
            },
          },
        },
      });
    }

    async function crearGraficoClientes() {
      // Verifica que haya datos disponibles antes de renderizar el gráfico
      if (!rankingData.value.topClients.length) return;

      // Espera a que el DOM esté actualizado
      await nextTick();

      const clientesRecurrentes = rankingData.value.topClients;
      console.log(clientesRecurrentes)
      const labels = clientesRecurrentes.map((producto) => producto.nombre);
      const data = clientesRecurrentes.map((producto) => producto.cantidad_total);

      // Obtiene el contexto del canvas para crear el gráfico
      const ctx = clientsChart.value.getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Mejores clientes",
              data,
              backgroundColor: ["#b20463", "#b23604", "#ff9e00"],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false, 
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `${context.raw} vendidos`,
              },
            },
          },
        },
      });
    }

    async function crearGraficoCategorias() {
  // Verifica que haya datos disponibles antes de renderizar el gráfico
  if (!rankingData.value.topCategories.length) return;

  // Espera a que el DOM esté actualizado
  await nextTick();

  const categoriasPopulares = rankingData.value.topCategories;
  console.log(categoriasPopulares)
  const labels = categoriasPopulares.map((categoria) => categoria.nombre);
  const data = categoriasPopulares.map((categoria) => categoria.cantidad_total);

  // Obtiene el contexto del canvas para crear el gráfico
  const ctx = categoriesChart.value.getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Categorías más populares",
          data,
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#E7E9ED",
            "#9B59B6",
          ],
          borderColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#E7E9ED",
            "#9B59B6",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: {
          callbacks: {
            label: (context) => `${context.raw} ventas`,
          },
        },
      },
    },
  });
}

async function capturarData() {
  try {
    console.log("DATOS A ENVIAR", consulta.value);
    const response = await Consultar(consulta.value);
    console.log(response);

    if (!response || response.mensaje === 'No se encontraron resultados' || response[0].venta === null) {
      swallError("No existen datos relacionados a lo solicitado");
    } else {
      respuesta.value = response;
      mostrarGrafico.value = true;
    }
  } catch (error) {
    console.error("Error al capturar datos:", error);
    swallError("No existen datos con relacion a la peticion");
  }
}

    onMounted(async () => {
      await traerInformacion();
      await crearGraficoProductos();
      await crearGraficoClientes();
      await crearGraficoCategorias();
    });

    return {
      rankingData,
      productsChart,
      clientsChart,
      categoriesChart,
      consulta,
      capturarData,
      mostrarGrafico,
      respuesta
    };
  },
 
};
</script>

<style scoped>
.report-container {
  display: grid;
  grid-template-columns: 60% 40%;
  gap: 20px;
  padding: 2rem;
  font-family: Arial, sans-serif;
  color: #ffffff;
}

h2 {
  color: orange;
}

.report-selection,
.report-selection2,
.ranking-section,
.report-display {
  padding: 15px;
  border: 1px solid #ff8c00;
  background-color: #333;
  border-radius: 5px;
}

.report-selection {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 3;
  gap: 1rem;
  align-items: center;
 
}

.report-selection2 {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);

}

.report-display {
  min-height: 100px;
  height: 250px;
}

.ranking-section {
  height: 36vh;
}

.ranking-section canvas {
  margin-top: 20px;
  max-height: 220px;
}

.contenedor-graficos {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contenedor-reporte {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.report-selection input,
.report-selection button,
.report-selection select {
  padding: 8px 12px;
  border: 1px solid #ffa500;
  border-radius: 5px;
  background-color: #333;
  color: #f5f5f5;
  cursor: pointer;
}

.report-selection button:hover {
  background-color: #ffa500;
  color: #1a1a1a;
}

@media (max-width: 768px) {
  .report-container {
    grid-template-columns: 1fr;
  }

  .report-selection {
    flex: 1;
  }

  .report-selection2 {
    grid-template-columns: 1fr;
  }
}
.diagrama{
  max-width: 400px; /* ajusta el ancho máximo */
  max-height: 150px;
}
.input_date,
.select_report
{
  width: 20rem;
}
</style>
