<template>
  <div class="payment-view">
    <h1 style="margin-bottom: 1rem;">VISTA PARA PAGAR</h1>
    <button class="boton" @click.prevent="regresar">Regresar</button>

    <div class="search-container">
      <input type="text" v-model="cedula" placeholder="Número de cédula del cliente" @change.prevent="ValueCedula($event.target.value)" />
      <button @click="addClient" class="add-client-button">
        <i class="icon-plus">
          <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 20 20"><path fill="currentColor" d="M9 2a4 4 0 1 0 0 8a4 4 0 0 0 0-8M6 6a3 3 0 1 1 6 0a3 3 0 0 1-6 0m-1.991 5A2 2 0 0 0 2 13c0 1.691.833 2.966 2.135 3.797C5.417 17.614 7.145 18 9 18q.617 0 1.21-.057a5.5 5.5 0 0 1-.618-.958Q9.301 17 9 17c-1.735 0-3.257-.364-4.327-1.047C3.623 15.283 3 14.31 3 13c0-.553.448-1 1.009-1h5.59q.277-.538.658-1zM14.5 19a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9m0-7a.5.5 0 0 1 .5.5V14h1.5a.5.5 0 0 1 0 1H15v1.5a.5.5 0 0 1-1 0V15h-1.5a.5.5 0 0 1 0-1H14v-1.5a.5.5 0 0 1 .5-.5"/></svg>
        </i>
      </button>
    </div>

    <div class="select-container" >
      <select v-model="datosVenta.metodo_de_pago">
        <option value="" disabled selected>Método de Pago</option>
        <option :value="1">Tarjeta</option>
        <option :value="2">Efectivo</option>
        <option :value="3">Fiar</option>
      </select>

      <select v-model="datosVenta.metodo_de_venta">
        <option value="" disabled selected>Método de Venta</option>
        <option :value="2">Domicilio</option>
        <option :value="1">Presencial</option>
        <option :value="3">Para llevar</option>
      </select>
    </div>

    <table class="products-table">
      <thead>
        <tr>
        
          <th>Img</th>
          <th>id_producto</th>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Cantidad</th>
          <th>Subtotal</th>
          <th>Eliminar</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(producto, index) in productos" :key="index">
        
          <td><img :src="producto.imagen" alt="Imagen del producto" /></td>
          <td>{{ producto.id_producto }}</td>
          <td>{{ producto.nombre }}</td>
          <td>{{ producto.precio }}</td>
          <td><input type="number" v-model="producto.cantidad" min="1" /></td>
          <td>{{ producto.precio * producto.cantidad }}</td>
          <td>
            <button @click="eliminarProducto(producto.id_producto,index)">Eliminar</button>
          </td>
        </tr>
        <tr><td>   <p>Total a pagar: ${{ totalPagar }}</p></td> </tr>
      </tbody>
    </table>

    <div v-if="filtro.length > 0" class="contenedor_cliente">
      <svg xmlns="http://www.w3.org/2000/svg" width="6em" height="6em" viewBox="0 0 12 12">
	<path fill="currentColor" d="M1 3a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2zm4 1.25a1 1 0 1 0 0-2a1 1 0 0 0 0 2m0 3c1.5 0 2-.75 2-1.5A.75.75 0 0 0 6.25 5h-2.5a.75.75 0 0 0-.75.75c0 .75.5 1.5 2 1.5M3.268 10A2 2 0 0 0 5 11h2a4 4 0 0 0 4-4V5a2 2 0 0 0-1-1.732V7a3 3 0 0 1-3 3z" />
</svg>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center">
        <h2>Cliente:</h2>
  <p >Cod.cliente: {{ filtro[0].id }}</p>
  <p>Nombre: {{ filtro[0].nombre }}</p>
  <p>Cédula: {{ filtro[0].cedula }}</p>
  <p>Correo: {{ filtro[0].correo }}</p>
  <p>Teléfono: {{ filtro[0].telefono }}</p>
        </div>

</div>
<p v-else>No hay informacion del cliente</p>
<select v-model="datosVenta.estado">
        <option value="" disabled selected>Método de Pago</option>
        <option :value="1">Finalizado</option>
        <option :value="2">En proceso</option>
       
      </select>

  

    <button @click="guardar" class="save-button">Guardar</button>
  </div>
</template>

<script>
import { Clientes } from '../../../api';
import { onMounted, ref ,computed} from 'vue';
import { swallError ,swallConfirmation} from '../../../alerts';
import { agregarVenta } from '../../../api';
import { useRouter } from 'vue-router';
const router=useRouter()
export default {
  setup() {
    const clientes = ref([]);
    const filtro = ref([]);
    const encontrado = ref(false);
    const productos = ref(JSON.parse(localStorage.getItem('pedidos')));
   console.log(productos);
    const items ={
      "id_producto":null,
      "cantidad":null,
      "total":null /**VALOR UNITARIO DLEPRODUCTO */
    }
    const datosVenta ={
      "metodo_de_pago":null,
      "metodo_de_venta":null,
      "estado":null,
      "id_cliente":null,
      "items":items
    }

    async function ListarClientes() {
      try {
        const response = await Clientes();
        console.log(response);
        clientes.value = response;
      } catch (error) {
        console.error("Error fetching clientes:", error);
      }
    }

    function ValueCedula(cedula)  {
      console.log("Número de cédula ingresado:", cedula);
      const resultado = clientes.value.filter((cliente) => cliente.cedula == cedula);
      const id_usuario=resultado[0].id;
      datosVenta.id_cliente=id_usuario;
       filtro.value=resultado;
       console.log(filtro)
        encontrado.value = true;
   
    };

    
    console.log(filtro);


   async function guardar()  {
   
      datosVenta.items = productos.value.map(producto => ({
    id_producto: producto.id_producto,
    cantidad: producto.cantidad,
    total: producto.precio
  }));
  console.log("DATOS:", datosVenta);
  const reponse = await agregarVenta(datosVenta);
  console.log(response);
  localStorage.removeItem("pedidos")
  router.push("/dashboard/principal")

   
    };

    const totalPagar = computed(() => {
      return productos.value.reduce((total, producto) => {
        return total + producto.precio * producto.cantidad;
      }, 0);
    });

    async function eliminarProducto(index,posicion) {
      console.log("id del producto",index);
      console.log("posicion en tabla",posicion);
      productos.value.splice(posicion, 1);
      localStorage.setItem("pedidos", JSON.stringify(productos.value))
     

    
    }

    async function regresar() {
     
     const confirmacion = await swallConfirmation("¿Desea seguir agregando productos?");
     if (confirmacion) {
    
         router.push("/dashboard/principal");
     
         

   
       }
      
      
     }

    onMounted(async () => {
      await ListarClientes();
  
    });

    return {
      clientes,
      productos,
      datosVenta,
      ListarClientes,
      ValueCedula,
      filtro,
      encontrado,
      items,
      guardar,
      totalPagar,
      eliminarProducto,
      regresar
    
      
      
    };
  },
};
</script>

<style scoped>
.payment-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px;
  background-color: white;
  border-radius: 1rem;
  height: 100vh;

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
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  margin: 0 auto;
}
.boton{
  background-color: orange;
  padding: 8px;
  border: 1px solid orange;
  margin: 1rem;
  border-radius: 5px;

}
.contenedor_cliente{
  border: 1px solid gray;
  border-radius: 1rem;
  padding: 1rem;
  width: 50%;
  display: flex
}
</style>
