<template>
    <div class="payment">
        <div style="display: flex; flex-direction: column; align-items: center;
        justify-content: center;">
            <h1>Consulta estado de clientes</h1>
      <label for="cedula">Ingresa el número de documento del cliente:</label>
      <input class="input_busqueda" type="number" v-model="cedula" id="cedula" placeholder="Ej. 12345678" style="margin: 10px;"/>
      <button class="boton_buscar"@click.prevent="consultar">Buscar</button>
  


        </div>
      
  
      <!-- Mostrar información del cliente si existe -->
      <div v-if="informacion.Cliente" class="client-info">
        <h2><strong>información del Cliente</strong></h2>
        <p><strong>Cod.Cliente:</strong> {{ informacion.Cliente.id }}</p>
        <p><strong>Nombre:</strong> {{ informacion.Cliente.nombre }}</p>
        <p><strong>Cédula:</strong> {{ informacion.Cliente.cedula }}</p>
        <p><strong>Teléfono:</strong> {{ informacion.Cliente.telefono }}</p>
        <p><strong>Correo:</strong> {{ informacion.Cliente.correo }}</p>
    
      </div>
      <button class="boton_buscar" style="width: 5%;">Abonar</button>
  </div>


  <div style="display: flex; align-items: center;justify-content: center;" >
    <div v-if="informacion.Deudas && informacion.Deudas.length > 0" class="debt-table">
        <h2 style="padding-top: 5px;">Deudas del Cliente</h2>
        <table>
          <thead>
            <tr>
              <th>Cod.venta</th>
              <th>Cod.cliente</th>
              <th>Metodo de venta</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deuda in informacion.Deudas" :key="deuda.id">
              <td>{{ deuda.id }}</td>
              <td>{{ deuda.id_cliente_id }}</td>
              <td>{{ deuda.metodo_de_venta }}</td>
              <td>{{ deuda.total }}</td>
              <td>{{ deuda.estado }}</td>
              <td>{{ deuda.fecha }}</td>
            </tr>
          </tbody>
        </table>
        
      </div>


</div>

  <div style="display: flex; justify-content: center;">
    <div v-if="informacion['Total deuda'] !== undefined" class="total-debt">
        <h2>Total deuda: <span>{{ informacion['Total deuda'] }}</span></h2>
       
      </div>
      
  
      <!-- Mensaje si no se encontraron deudas -->
      <p v-else-if="informacion.Cliente && informacion.Deudas.length === 0" class="no-debt">No tiene deudas registradas.</p>
  
      <!-- Mensaje si no hay cliente encontrado -->
      <p v-else class="no-client">Por favor, ingresa una cédula para buscar las cuentas pendientes.</p>
    
  </div>
      <!-- Mostrar el total de la deuda -->
     
    
      <!-- Tabla de deudas -->
     
  </template>
  
  <script>
  import { ref } from 'vue';
  import { ConsultarDeuda } from '../../../api'; // Importar la función de la API
  
  export default {
    setup() {
      const cedula = ref(null); // Cédula del cliente
      const informacion = ref({ Cliente: null, Deudas: [] }); // Información del cliente y sus deudas
   // Indicador de carga
  
      // Función para consultar deudas del cliente
      async function consultar() {
        if (!cedula.value) {
          return; // Verifica si se ingresó una cédula
        }
  
     
  
        try {
          const response = await ConsultarDeuda(cedula.value);
          informacion.value = response; // Asigna la respuesta a informacion
        } catch (error) {
          console.error("Error al consultar deuda:", error);
        } finally {
    
        }
      }
  
      return {
        cedula,
        informacion,
        consultar,
      
      };
    }
  };
  </script>
  
  <style>
  /* Estilos generales */
  .payment {
 width: auto;
 height: 20vh;
    margin: 0 auto;
    padding: 20px;
    border-radius: 10px;
   
    display: flex;
    justify-content: space-evenly;
    align-items: center
  }
  
  h1, h2 {
    text-align: center;
    font-family: 'Arial', sans-serif;
  }
  
  label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
  }
  
  .input_busqueda {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
  }
  .boton_buscar {
    width: 70%;
    padding: 10px;
    background-color: orange;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;

   
  }
  
  button:hover {
    background-color: rgb(224, 146, 3);
  }
  
  .loading {
    text-align: center;
    font-size: 18px;
    color: #888;
    margin-top: 20px;
  }
  
  .client-info{
    background-color: white;
    padding: 1rem 4rem;
    border-radius: 1rem;
    font-size: 15px;
  }

  .client-info, .debt-table, .total-debt, .no-debt, .no-client {
    margin-top: 20px;

  }
  
  .client-info p {
    font-size: 16px;
    line-height: 1.6;
  }
  .debt-table{
    background-color: white;
    width: 90%;
    height: 45vh;
    padding: 1rem;
    border-radius: 1rem;
  }
  
  .debt-table table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .debt-table th {
    padding: 10px;
    text-align: center;
    border: 1px solid #ddd;
  }
   .debt-table td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  .debt-table th {
    background-color: #f4f4f4;
    font-weight: bold;
  }
  
  .debt-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .total-debt {
    text-align: center;
    font-size: 18px;
    background-color: orange;
    width: 20%;
    padding: 1rem;
    border-radius: 1rem;
  }
  
  .total-debt span {
    color: red;
    font-weight: bold;
  }
  
  .no-debt, .no-client {
    text-align: center;
    font-size: 18px;
    color: #888;
  }
  
  .no-debt {
    color: #4CAF50;
  }
  
  .no-client {
    color: white;
  }
  </style>
  