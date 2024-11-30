<template>
  <div class="fondo">

    <div class="catalogo">
      <div style="display: flex; align-items: center; justify-content: space-between">
        <h1 style="margin-top: 1rem;color:orange">Catálogo {{ nombre }}</h1>
        <router-link style="text-decoration: none; color: white;">
          <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24" class="cerrar"
            @click.prevent="DirigirPago">
            <path fill="currentColor"
              d="M6 5h11a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V8a3 3 0 0 1 3-3M4 17a2 2 0 0 0 2 2h5v-3H4zm7-5H4v3h7zm6 7a2 2 0 0 0 2-2v-1h-7v3zm2-7h-7v3h7zM4 11h7V8H4zm8 0h7V8h-7z" />
          </svg>
        </router-link>
      </div>

      <div class="barra-busqueda">
        <label for="categoria" class="label-categoria">Selecciona una categoría:</label>
        <select @change.prevent="seleccion($event.target.value)" class="select-categoria">
          <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">

            {{ categoria.nombre }}
          </option>
        </select>
      </div>

      <div class="productos">
        <CardProductos v-for="producto in productos" :key="producto.id" :titulo="producto.nombre"
          :descripcion="producto.descripcion" :precio="producto.precio" :existencia="producto.existencia"
          :id="producto.id" :ruta="producto.imagen" :carrito="carrito" />
          <CardProductos v-for="producto in total" :key="producto.id" :titulo="producto.nombre"
          :descripcion="producto.descripcion" :precio="producto.precio" :existencia="producto.existencia"
          :id="producto.id" :ruta="producto.imagen" :carrito="carrito" />
    
      </div>
   

      

    </div>
  </div>

</template>

<script>
import { Categorias, Productos,TotalProductos } from '../../../api';
import { onMounted, ref } from 'vue';
import CardProductos from '../../components/CardProductos.vue';
import { swallConfirmation, swallError,swallToast } from '../../../alerts';
import { RouterLink, useRouter } from 'vue-router';

export default {
  components: {
    CardProductos
  },
  setup() {
    const router = useRouter()
    const categorias = ref([]);
    const productos = ref([]);
    const nombre = ref("");
    const pedido = ref([]);
    const total = ref([]);


    async function ListarCategorias() {
      try {
        const response = await Categorias();
        console.log(response);
        categorias.value = response.Categorias;
      } catch (error) {
        console.error("Error fetching categorias:", error);
      }
    }

    async function Producticos() {
      try {
        const response = await TotalProductos();
        console.log(response);
        const direccionBase = 'http://127.0.0.1:8001';
        response.Productos.forEach(producto => {
          producto.imagen = `${direccionBase}${producto.imagen}`;
        });
        total.value = response.Productos;
        console.log(total)
      } catch (error) {
        console.error("Error fetching categorias:", error);
      }
    }

    async function seleccion(id) {
      console.log("dato ingresado", id);
      try {
        const response = await Productos(id);
        console.log(response);

        const direccionBase = 'http://127.0.0.1:8001';
        response.Productos.forEach(producto => {
          producto.imagen = `${direccionBase}${producto.imagen}`;
        });
        productos.value = response.Productos;
        total.value=[];
        console.log(productos.value);


        const categoriaSeleccionada = categorias.value.find(c => c.id == id);
        nombre.value = categoriaSeleccionada ? categoriaSeleccionada.nombre : "";
      } catch (error) {
        console.error("Error fetching productos:", error);
      }
    }

    async function carrito(data) {
      console.log("dato ingresado", data);
      swallToast(`${data.nombre} agregado`)
      pedido.value = [...pedido.value, data];
      console.log(pedido.value);
      localStorage.setItem("pedidos", JSON.stringify(pedido.value));


    }

    async function DirigirPago() {
  const listado = JSON.parse(localStorage.getItem("pedidos") || "[]"); // Asegurarse de que listado sea un array
  console.log(listado);

  const confirmacion = await swallConfirmation("¿Ir a pagar?");
  if (confirmacion) {
    if ((pedido?.value?.length > 0) || (listado.length > 0)) {
      router.push("/dashboard/pago");
    } else {
      swallError("No hay productos seleccionados para la compra");
    }
  }
}

    console.log(pedido)
    onMounted(async () => {
      await ListarCategorias();
      await Producticos();
    });

    return {
      categorias,
      seleccion,
      productos,
      nombre,
      carrito,
      pedido,
      DirigirPago,
      total,


    };
  }
}
</script>

<style>
.catalogo {
  padding: 12px 3rem;
  color: white;
  display: flex;
  flex-direction: column;


}

.barra-busqueda {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1rem;
}

.label-categoria {
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: white
}

.select-categoria {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.select-categoria:hover {
  border-color: #007bff;
}

.select-categoria:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.productos {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1rem 1rem;
  background-color: transparent;
  height: 65vh;
  overflow-y: scroll;


}

.nombre {
  color: white;
  text-align: center;
  margin-top: 10px;
  text-transform: capitalize;
}


</style>
