<template>
  <div class="contenedor_panel">
    <h1>Panel de control de ventas</h1>

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
            <th>Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="datos in ventasFiltradas" :key="datos.id_cliente">
            <td>{{ datos.id_cliente }}</td>
            <td>{{ datos.metodo_de_pago == 1 ? '💳 Tarjeta' : datos.metodo_de_pago == 2 ? '💲 Efectivo​' : datos.metodo_de_pago == 3 ? '🗳️Fiado':'Contra Entrega'
              }}</td>
            <td>{{ datos.metodo_de_venta == 1 ? '​🛒​ Presencial' : datos.metodo_de_venta == 2 ? '🛵 Domicilio' : '​➡️​Para Llevar' }}</td>
            <td>{{ datos.fecha }}</td>
            <td>{{ datos.total }}</td>
            <td :style="{ color: datos.estado == 1 ? 'green' : 'red' }">{{ datos.estado == 1 ? '✔️​ Finalizado' : '​⭕​ En proceso' }}</td>
            <td style="text-align:center; display: flex; gap: 1rem;  justify-content: center; border: none; align-items: center;" >
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"
                @click="actualizarEstado(datos.id)">
                <path fill="none" stroke="currentColor" stroke-width="2"
                  d="M1.75 16.002C3.353 20.098 7.338 23 12 23c6.075 0 11-4.925 11-11m-.75-4.002C20.649 3.901 16.663 1 12 1C5.925 1 1 5.925 1 12m8 4H1v8M23 0v8h-8" />
              </svg>
              <svg v-if="datos.metodo_de_venta == 2" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
                viewBox="0 0 20 20" @click="enviarSoporteDomicilio(datos.id_cliente)">
                <path fill="currentColor"
                  d="M10 0c5.342 0 10 4.41 10 9.5c0 5.004-4.553 8.942-10 8.942a11 11 0 0 1-3.43-.546c-.464.45-.623.603-1.608 1.553c-.71.536-1.378.718-1.975.38c-.602-.34-.783-1.002-.66-1.874l.4-2.319C.99 14.002 0 11.842 0 9.5C0 4.41 4.657 0 10 0m0 1.4c-4.586 0-8.6 3.8-8.6 8.1c0 2.045.912 3.928 2.52 5.33l.02.017l.297.258l-.067.39l-.138.804l-.037.214l-.285 1.658a3 3 0 0 0-.03.337v.095q0 .007-.002.008c.007-.01.143-.053.376-.223l2.17-2.106l.414.156a9.6 9.6 0 0 0 3.362.605c4.716 0 8.6-3.36 8.6-7.543c0-4.299-4.014-8.1-8.6-8.1M5.227 7.813a1.5 1.5 0 1 1 0 2.998a1.5 1.5 0 0 1 0-2.998m4.998 0a1.5 1.5 0 1 1 0 2.998a1.5 1.5 0 0 1 0-2.998m4.997 0a1.5 1.5 0 1 1 0 2.998a1.5 1.5 0 0 1 0-2.998" />
              </svg>
              <svg v-if="datos.metodo_de_venta == 3"  xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 32 32" @click="enviarSoportePedido(datos.id_cliente)">
                <path fill="currentColor" d="M16 4a9 9 0 0 0-9 9v4.803l-1.929 4.826A1 1 0 0 0 6 24h6c0 2.217 1.783 4 4 4s4-1.783 4-4h6a1 1 0 0 0 .929-1.371L25 17.803V13a9 9 0 0 0-9-9m2 20c0 1.112-.888 2-2 2s-2-.888-2-2zM9 13a7 7 0 1 1 14 0v4.995a1 1 0 0 0 .071.371L24.523 22H7.477l1.452-3.634a1 1 0 0 0 .071-.37z" />
              </svg>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="5" class="total_label">Total de venta:</td>
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
import { PanelVentas, Actualizar,Clientes,ApiWhatsapp } from '../../../api';
import { swallActualizar,swallConfirmation } from '../../../alerts';

export default {
  setup() {
    const ventas = ref([]);
    const ventasFiltradas = ref([]);
    const fechaFiltro = ref("");


    async function cargarVentas() {
      try {
        const response = await PanelVentas();
        console.log(response);
        ventas.value = response;


        const fechaActual = new Date().toISOString().split("T")[0];
        fechaFiltro.value = fechaActual;
        filtrarVentas();
      } catch (error) {
        console.error("Error al cargar las ventas:", error);
      }
    }


    function filtrarVentas() {
      if (fechaFiltro.value) {
        ventasFiltradas.value = ventas.value.filter(
          (venta) => venta.fecha === fechaFiltro.value
        );
      }
    }


    function mostrarTodas() {
      ventasFiltradas.value = [...ventas.value];
      fechaFiltro.value = "";
    }


    function calcularTotalVentas() {
      return ventasFiltradas.value.reduce((total, venta) => total + venta.total, 0);
    }

    async function actualizarEstado(id) {
    
      const { estado } = await swallActualizar();
      console.log("Nuevo estado:", estado);
      const ventasActualizadas =
      {
        "id": id,
        "estado": estado
      };
      console.log("Ventas actualizadas:", ventasActualizadas);
      await Actualizar(ventasActualizadas)
      await cargarVentas();
    }

    async function enviarSoporteDomicilio(cliente) {
      const confirmacion= await swallConfirmation("¿Desea mandar aviso al cliente?");
      if(!confirmacion){
        return
      }
   
      const clientes = await Clientes();
      console.log(clientes)
      const filtro = clientes.filter((info)=>info.id==cliente)
      console.log(filtro)
      const data={
        "message":`*ESTIMADO CLIENTE 😊:* 
        ${filtro[0].nombre}, 
        su pedido ha salido en camino🛵, 
        Porfavor estar por su pedido.
        *---Muchas gracias---*
        
        *Minimarket Colombia🌍*`,
        "phone":`57${filtro[0].telefono}`
      }
      console.log(data)
      await ApiWhatsapp(data)

    }


    async function enviarSoportePedido(cliente) {
      const confirmacion= await swallConfirmation("¿Desea mandar aviso al cliente?");
      if(!confirmacion){
        return
      }
    
      const clientes = await Clientes();
      console.log(clientes)
      const filtro = clientes.filter((info)=>info.id==cliente)
      console.log(filtro)
      const data={
        "message":`*ESTIMADO CLIENTE 😊:* 
        ${filtro[0].nombre}, 
        su pedido se encuentra listo para ser reclamado, 
        Porfavor reclamar en caja.
        *---Muchas gracias---*
        
        *Minimarket Colombia🌍*`,
        "phone":`57${filtro[0].telefono}`
      }
      console.log(data)
      await ApiWhatsapp(data)

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
      actualizarEstado,
      enviarSoporteDomicilio,
      enviarSoportePedido
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