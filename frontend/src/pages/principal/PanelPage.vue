<template>
    <div class="contenedor_panel">
      <h1>Panel de control de ventas</h1>
  
      <!-- Filtro por fecha -->
      <div class="filtro_fecha">
        <label for="fecha">Filtrar por fecha:</label>
        <input type="date" v-model="fechaFiltro" @change="filtrarVentas" />
        <button @click="mostrarTodas">Mostrar todas</button>
      </div>
  
      <div v-if="ventasFiltradas.length > 0" class="contenedor_infopanel">
        <table class="tabla_ventas">
          <thead>
            <tr>
              <th>id_Cliente</th>
              <th>metodo de pago</th>
              <th>Metodo de venta</th>
              <th>fecha</th>
              <th>total</th>
              <th>estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="datos in ventasFiltradas" :key="datos.id_cliente">
              <td>{{ datos.id_cliente }}</td>
              <td>{{ datos.metodo_de_pago }}</td>
              <td>{{ datos.metodo_de_venta }}</td>
              <td>{{ datos.fecha }}</td>
              <td>{{ datos.total }}</td>
              <td>{{ datos.estado }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="4" class="total_label">Total de venta:</td>
              <td>{{ calcularTotalVentas() }}</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { PanelVentas } from '../../../api';
  
  export default {
    setup() {
      const ventas = ref([]); // Almacena todas las ventas
      const ventasFiltradas = ref([]); // Almacena las ventas filtradas
      const fechaFiltro = ref(""); // Fecha de filtro seleccionada
  
      // Cargar ventas y aplicar el filtro de la fecha actual al montar el componente
      async function cargarVentas() {
        try {
          const response = await PanelVentas();
          ventas.value = response;
  
          // Filtrar ventas de acuerdo a la fecha actual por defecto
          const fechaActual = new Date().toISOString().split("T")[0];
          fechaFiltro.value = fechaActual;
          filtrarVentas();
        } catch (error) {
          console.error("Error al cargar las ventas:", error);
        }
      }
  
      // Función para filtrar las ventas según la fecha seleccionada
      function filtrarVentas() {
        if (fechaFiltro.value) {
          ventasFiltradas.value = ventas.value.filter(
            (venta) => venta.fecha === fechaFiltro.value
          );
        }
      }
  
      // Función para mostrar todas las ventas sin filtrar
      function mostrarTodas() {
        ventasFiltradas.value = [...ventas.value];
        fechaFiltro.value = ""; // Limpiar el filtro de fecha
      }
  
      // Función para calcular el total de ventas en la tabla filtrada
      function calcularTotalVentas() {
        return ventasFiltradas.value.reduce((total, venta) => total + venta.total, 0);
      }
  
      onMounted(async () => {
        await cargarVentas();
      });
  
      return {
        ventasFiltradas,
        fechaFiltro,
        filtrarVentas,
        mostrarTodas,
        calcularTotalVentas,
      };
    },
  };
  </script>
  
  <style>
  .contenedor_panel {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 90vh;
    gap: 1rem;
color: #f5f5f5;
   
  }
  
  .contenedor_panel h1 {
    font-size: 2rem;
    color: #ffa500;
    margin-top: 1rem;
  }
  
  .filtro_fecha {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .filtro_fecha label {
    color: #f5f5f5;
  }
  
  .filtro_fecha input,
  .filtro_fecha button {
    padding: 8px 12px;
    border: 1px solid #ffa500;
    border-radius: 5px;
    background-color: #333;
    color: #f5f5f5;
    cursor: pointer;
  }
  
  .filtro_fecha button:hover {
    background-color: #ffa500;
    color: #1a1a1a;
  }
  
  .contenedor_infopanel {
    width: 90%;
    background-color: #333;
    padding: 2rem;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    overflow-y: auto;
  }
  
  .tabla_ventas {
    width: 100%;
    border-collapse: collapse;
    font-size: 1rem;
    color: #f5f5f5;
  }
  
  .tabla_ventas th,
  .tabla_ventas td {
    padding: 12px;
    text-align: left;
    border: 1px solid #555;
  }
  
  .tabla_ventas th {
    background-color: #ffa500;
    color: #1a1a1a;
    font-weight: bold;
    text-transform: uppercase;
  }
  
  .tabla_ventas tr:nth-child(even) {
    background-color: #2a2a2a;
  }
  
  .tabla_ventas tr:nth-child(odd) {
    background-color: #1e1e1e;
  }
  
  .tabla_ventas tr:hover {
    background-color: #ffa500;
    color: #1a1a1a;
    transition: background-color 0.3s ease;
  }
  
  .total_label {
    font-weight: bold;
    text-align: right;
    padding-right: 12px;
    color: #ffa500;
  }
  </style>
  