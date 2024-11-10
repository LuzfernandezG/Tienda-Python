<template>
  <div class="fondo">

    <div class="catalogo">
      
    <h1 style="margin-top: 1rem;color:orange">Catálogo {{ nombre }}</h1>

    <div class="barra-busqueda">
      <label for="categoria" class="label-categoria">Selecciona una categoría:</label>
      <select @change.prevent="seleccion($event.target.value)" class="select-categoria">
        <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
          
          {{ categoria.nombre }}
        </option>
      </select>
    </div>

    <!-- Muestra el nombre de la categoría seleccionada -->
    <div class="productos">
  <CardProductos 
    v-for="producto in productos" 
    :key="producto.id" 
    :titulo="producto.nombre"
    :descripcion="producto.descripcion" 
    :precio="producto.precio" 
    :existencia="producto.existencia" 
    :id="producto.id"
    :ruta="producto.imagen"
    :carrito="carrito"

  
    />
</div>

<!-- Mensaje cuando no hay productos -->
<p v-if="productos.length === 0" class="mensaje-sin-productos">
  No hay productos.
</p>
  
  </div>
    </div>
  

 



</template>

<script>
import { Categorias, Productos } from '../../../api';
import { onMounted, ref } from 'vue';
import CardProductos from '../../components/CardProductos.vue';

export default {
  components: {
    CardProductos
  },
  setup() {
    const categorias = ref([]);
    const productos = ref([]);
    const nombre = ref("");
    const pedido = ref([]);
   

    async function ListarCategorias() {
      try {
        const response = await Categorias();
        console.log(response);
        categorias.value = response.Categorias;
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
        console.log(productos.value);
  
  
        const categoriaSeleccionada = categorias.value.find(c => c.id == id);
        nombre.value = categoriaSeleccionada ? categoriaSeleccionada.nombre : "";
      } catch (error) {
        console.error("Error fetching productos:", error);
      }
    }
  
    async function carrito(data) {
      console.log("dato ingresado", data);
      pedido.value = [...pedido.value,data]; // Modificar la asignación para usar pedido.value
      console.log(pedido.value); 
      localStorage.setItem("pedidos", JSON.stringify(pedido.value));
     // Mostrar el contenido actualizado de pedido
      
    }
    console.log(pedido)
    onMounted(async () => {
      await ListarCategorias();
    });

    return {
      categorias,
      seleccion,
      productos,
      nombre,
      carrito,
      pedido,
    
      
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
  margin-bottom: 1rem; /* Espacio debajo de la barra de búsqueda */
}

.label-categoria {
  margin-bottom: 0.5rem; /* Espacio debajo de la etiqueta */
  font-weight: bold; /* Estilo para la etiqueta */
  color:white
}

.select-categoria {
  padding: 10px; /* Espacio dentro del select */
  border: 1px solid #ccc; /* Borde del select */
  border-radius: 5px; /* Bordes redondeados */
  font-size: 16px; /* Tamaño de la fuente */
  transition: border-color 0.3s; /* Transición para el borde */
}

.select-categoria:hover {
  border-color: #007bff; /* Color del borde al pasar el mouse */
}

.select-categoria:focus {
  outline: none; /* Quitar el borde de enfoque por defecto */
  border-color: #007bff; /* Color del borde al enfocar */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* Sombra al enfocar */
}

.productos {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem; /* Espaciado entre productos */
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

.mensaje-sin-productos {
  color: white; /* Color del mensaje */
  text-align: center;
  margin-top: 1rem;
  font-size: 1.5rem; /* Espacio por encima del mensaje */
}
</style>
