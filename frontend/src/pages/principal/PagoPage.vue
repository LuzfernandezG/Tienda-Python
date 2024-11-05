<template>
    <div class="payment-view">
      <h1 style="margin-bottom: 1rem;">VISTA PARA PAGAR</h1>
  
      <div class="search-container">
        <input type="text" v-model="cedula" placeholder="Número de cédula del cliente" />
        <button @click="addClient" class="add-client-button">
          <i class="icon-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 20 20"><path fill="currentColor" d="M9 2a4 4 0 1 0 0 8a4 4 0 0 0 0-8M6 6a3 3 0 1 1 6 0a3 3 0 0 1-6 0m-1.991 5A2 2 0 0 0 2 13c0 1.691.833 2.966 2.135 3.797C5.417 17.614 7.145 18 9 18q.617 0 1.21-.057a5.5 5.5 0 0 1-.618-.958Q9.301 17 9 17c-1.735 0-3.257-.364-4.327-1.047C3.623 15.283 3 14.31 3 13c0-.553.448-1 1.009-1h5.59q.277-.538.658-1zM14.5 19a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9m0-7a.5.5 0 0 1 .5.5V14h1.5a.5.5 0 0 1 0 1H15v1.5a.5.5 0 0 1-1 0V15h-1.5a.5.5 0 0 1 0-1H14v-1.5a.5.5 0 0 1 .5-.5"/></svg>

          </i> <!-- Aquí puedes usar un ícono de tu elección -->
        </button>
      </div>
  
      <div class="select-container">
        <select v-model="metodoPago">
          <option value="" disabled selected>Método de Pago</option>
          <option value="tarjeta">Tarjeta</option>
          <option value="efectivo">Efectivo</option>
          <option value="transferencia">Transferencia</option>
        </select>
  
        <select v-model="metodoVenta">
          <option value="" disabled selected>Método de Venta</option>
          <option value="online">Online</option>
          <option value="presencial">Presencial</option>
        </select>
      </div>
  
      <table class="products-table">
        <thead>
          <tr>
            <th>Img</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Cantidad</th>
            <th>Subtotal</th>
            <th>Eliminar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(producto, index) in productos" :key="index">
            <td><img :src="producto.img" alt="Imagen del producto" /></td>
            <td>{{ producto.nombre }}</td>
            <td>{{ producto.precio }}</td>
            <td><input type="number" v-model="producto.cantidad" min="1" /></td>
            <td>{{ producto.total }}</td>
            <td>
              <button @click="eliminarProducto(index)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p>Total a pagar: $</p>
  
      <button @click="guardar" class="save-button">Guardar</button>
    </div>
  </template>
  

<script>

import { Categorias, Productos } from '../../../api';
import { onMounted, ref } from 'vue';


export default {
 
  setup() {
   
    const productos = ref(JSON.parse(localStorage.getItem('pedidos')));
   console.log(productos);
 
    // onMounted(async () => {
    //   await ListarCategorias();
    // });

    return {
 
      productos,
     
    };
  }
}



</script>

<style scoped>
.payment-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
  background-color: white;
  border-radius: 1rem;
  height: 76vh;

}

h1 {
  text-align: center;
}

.search-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

input[type="text"] {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-client-button {
  background-color: #4CAF50; /* Color verde */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.icon-plus {
  margin-right: 5px;
}

.select-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
  flex: 1;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.products-table th,
.products-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

.products-table img {
  width: 50px; /* Ajusta según el tamaño de la imagen */
  height: auto;
}

.save-button {
  background-color: #2196F3; /* Color azul */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  margin: 0 auto;
}
</style>
