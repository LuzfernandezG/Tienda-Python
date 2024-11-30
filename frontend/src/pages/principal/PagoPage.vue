<template>
  <div class="payment-view">
    <h1 style="margin-bottom: 1rem;">VISTA PARA PAGAR</h1>
    <button class="boton" @click.prevent="regresar">Regresar</button>
    <button class="boton" @click.prevent="cancelar" style="margin-left: 10px;">Cancelar</button>

    <div class="search-container">
      <input type="text" v-model="cedula" placeholder="Número de cédula del cliente"
        @change.prevent="ValueCedula($event.target.value)" />
      <button @click="addClient" class="add-client-button">
        <i class="icon-plus">
          <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 20 20">
            <path fill="currentColor"
              d="M9 2a4 4 0 1 0 0 8a4 4 0 0 0 0-8M6 6a3 3 0 1 1 6 0a3 3 0 0 1-6 0m-1.991 5A2 2 0 0 0 2 13c0 1.691.833 2.966 2.135 3.797C5.417 17.614 7.145 18 9 18q.617 0 1.21-.057a5.5 5.5 0 0 1-.618-.958Q9.301 17 9 17c-1.735 0-3.257-.364-4.327-1.047C3.623 15.283 3 14.31 3 13c0-.553.448-1 1.009-1h5.59q.277-.538.658-1zM14.5 19a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9m0-7a.5.5 0 0 1 .5.5V14h1.5a.5.5 0 0 1 0 1H15v1.5a.5.5 0 0 1-1 0V15h-1.5a.5.5 0 0 1 0-1H14v-1.5a.5.5 0 0 1 .5-.5" />
          </svg>
        </i>
      </button>
    </div>

    <div class="select-container">
      <select v-model="datosVenta.metodo_de_pago">
        <option value="" disabled selected>Método de Pago</option>
        <option :value="1">Tarjeta</option>
        <option :value="2">Efectivo</option>
        <option :value="3">Fiar</option>
        <option :value="4">Contra Entrega</option>
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
            <button @click="eliminarProducto(producto.id_producto, index)">Eliminar</button>
          </td>
        </tr>
        <tr>
          <td>
            <p >Total a pagar: ${{ totalPagar }}</p>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="filtro.length > 0" class="contenedor_cliente">
      <svg xmlns="http://www.w3.org/2000/svg" width="5em" height="5em" viewBox="0 0 12 12">
        <path fill="currentColor"
          d="M1 3a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2zm4 1.25a1 1 0 1 0 0-2a1 1 0 0 0 0 2m0 3c1.5 0 2-.75 2-1.5A.75.75 0 0 0 6.25 5h-2.5a.75.75 0 0 0-.75.75c0 .75.5 1.5 2 1.5M3.268 10A2 2 0 0 0 5 11h2a4 4 0 0 0 4-4V5a2 2 0 0 0-1-1.732V7a3 3 0 0 1-3 3z" />
      </svg>
      <div
        style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 13px;">
        <h2>Cliente:</h2>
        <p>Cod.cliente: {{ filtro[0].id }}</p>
        <p>Nombre: {{ filtro[0].nombre }}</p>
        <p>Cédula: {{ filtro[0].cedula }}</p>
        <p>Correo: {{ filtro[0].correo }}</p>
        <p>Teléfono: {{ filtro[0].telefono }}</p>
      </div>
    </div>
    <p v-else>No hay informacion del cliente</p>

    <select v-model="datosVenta.estado">
      <option value="" disabled selected>Estado de venta</option>
      <option :value="1">Finalizado</option>
      <option :value="2">En proceso</option>

    </select>



    <button @click="guardar" class="save-button">Guardar</button>
  </div>
</template>

<script>
import { Clientes } from '../../../api';
import { onMounted, ref, computed } from 'vue';
import { swallError, swallConfirmation, swallTrue, swallForm } from '../../../alerts';
import { agregarVenta, AgregarCliente,ApiWhatsapp } from '../../../api';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter()
    const clientes = ref([]);
    const filtro = ref([]);
    const encontrado = ref(false);
    const productos = ref(JSON.parse(localStorage.getItem('pedidos')));
    console.log(productos);
    const items = {
      "id_producto": null,
      "cantidad": null,
      "total": null
    }
    const datosVenta = {
      "metodo_de_pago": null,
      "metodo_de_venta": null,
      "estado": null,
      "id_cliente": null,
      "items": items
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

    function ValueCedula(cedula) {
      console.log("Número de cédula ingresado:", cedula);
      const resultado = clientes.value.filter((cliente) => cliente.cedula == cedula);
      if (resultado.length == 0) {
        swallError("No se encontro cliente con ese cc")
        filtro.value = []
      } else {
        swallTrue("Cliente encontrado")
        const id_usuario = resultado[0].id;
        datosVenta.id_cliente = id_usuario;
        filtro.value = resultado;
        console.log(filtro)
        encontrado.value = true;

      }
    };
    async function addClient() {
      console.log("funcion para agregar cliente")
      const data = await swallForm();
      console.log(data);
      const response = await AgregarCliente(data);
      console.log(response);
      ListarClientes()
    }

    async function guardar() {

      if (!datosVenta.metodo_de_pago || !datosVenta.metodo_de_venta || !datosVenta.estado || !datosVenta.id_cliente) {
        swallError("Todos los campos de venta deben estar completos.");
        return;
      }


      if (!datosVenta.items || datosVenta.items.length === 0) {
        swallError("Debe haber al menos un producto en la venta.");
        return;
      }

      datosVenta.items = productos.value.map(producto => ({
        id_producto: producto.id_producto,
        cantidad: producto.cantidad,
        total: producto.precio
      }));
      console.log("DATOS:", datosVenta);
      const reponse = await agregarVenta(datosVenta);
      console.log(reponse);
      localStorage.removeItem("pedidos")
      
       if (filtro) {
        const productosListados = productos.value
    .map(
      (producto, index) => 
        `${index + 1}. 🛍️ Producto: *${producto.nombre}* | Cantidad: *${producto.cantidad}* | Precio: 💰 $${producto.precio} | Total: 💰 $${producto.precio * producto.cantidad}`
    )
    .join("\n");

  const data = {
    "message": `
      HOLA!\n
      ✨ *Estimado Cliente:* ${filtro.value[0].nombre},\n
      🛒 Realizaste una compra por el valor de: 💰 ${totalPagar.value}\n
      en 🏪 *Minimarket* 😊 -Colombia 🌍\n\n
      📋 *Detalles de tu compra:*\n${productosListados}\n\n
      🎉 *--GRACIAS POR SU COMPRA--* 🙌  
          `,
          "phone": `57${filtro.value[0].telefono}`
        };

      const mensaje = await ApiWhatsapp(data)
      console.log(mensaje)

       }
      router.push("/dashboard/principal")

    };

    const totalPagar = computed(() => {
      return productos.value.reduce((total, producto) => {
        return total + producto.precio * producto.cantidad;
      }, 0);
    });

    async function eliminarProducto(index, posicion) {
      console.log("id del producto", index);
      console.log("posicion en tabla", posicion);
      productos.value.splice(posicion, 1);
      localStorage.setItem("pedidos", JSON.stringify(productos.value))

    }

    async function regresar() {
      const confirmacion = await swallConfirmation("¿Desea seguir agregando productos?");
      if (confirmacion) {
        router.push("/dashboard/principal");
      }
    }

    async function cancelar() {
      const confirmacion = await swallConfirmation("¿Desea cancelar el pedido?");
      if (confirmacion) {
        localStorage.removeItem("pedidos");
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
      regresar,
      addClient,
      cancelar



    };
  },
};
</script>

<style scoped>
.payment-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f9f9f9;
  border-radius: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  height: 80vh;
  overflow-y: scroll;
}

h1 {
  text-align: center;
  color: #333;
  font-weight: bold;
}

.search-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

input[type="text"] {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.3s;
}

input[type="text"]:focus {
  border-color: #ff7043;
}

.add-client-button {
  background-color: orange;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.add-client-button:hover {
  background-color: gray;
}

.select-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  flex: 1;
  background-color: white;
  transition: border-color 0.3s;
}

select:focus {
  border-color: #ff7043;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 0.95rem;
  font-family: Arial, Helvetica, sans-serif
}

.products-table th {
  background-color: orange;
  color: black;
  font-weight: bold;
  padding: 12px;
  border: 1px solid #e0e0e0;
}

.products-table td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: center;
}

.products-table img {
  width: 50px;
  height: auto;
  border-radius: 5px;
}

.save-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  display: block;
  margin: 0 auto;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #388E3C;
}

.boton {
  background-color: #FFA726;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.boton:hover {
  background-color: #FB8C00;
}

.contenedor_cliente {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 0.9rem;
}
</style>
