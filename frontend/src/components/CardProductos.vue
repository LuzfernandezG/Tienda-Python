<template>
  <div class="contenedor_prueba">
      <h1 class="titulo">{{ titulo }}</h1>
      <p class="descripcion">{{ descripcion }}</p>
      <p class="precio">Precio: ${{ precio.toFixed(2) }}</p>
      <p class="existencia">Existencia: {{ existencia }}</p>
      
      <div class="contador">
          <button @click="decrementar" :disabled="cantidad <= 0">-</button>
          <span class="cantidad">{{ cantidad }}</span>
          <button @click="incrementar" :disabled="cantidad >= existencia">+</button>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24" class="agregar" @click.prevent="()=>capturar()"><path fill="currentColor" d="M0 1h4.764l3 11h10.515l3.089-9.265l1.897.633L19.72 14H7.78l-.5 2H22v2H4.72l1.246-4.989L3.236 3H0zm14 1v3h3v2h-3v3h-2V7H9V5h3V2zM4 21a2 2 0 1 1 4 0a2 2 0 0 1-4 0m14 0a2 2 0 1 1 4 0a2 2 0 0 1-4 0"/></svg>
  </div>
</template>

<script>
export default {
  name: 'CardProductos',
  props: {
      titulo: {
          type: String,
          required: true
      },
      descripcion: {
          type: String,
          required: true,
      },
      precio: {
          type: Number,
          required: true,
      },
      existencia: {
          type: Number,
          required: true,
      },
      id: {
          type: Number,
          required: true,
      },
      carrito: {
            type: Function,
            required: true
        },
  },
  data() {
      return {
          cantidad: 0, // Inicializa el contador en 1
      };
  },
  methods: {
      incrementar() {
          // Corrige 'this.existencias' a 'this.existencia'
          if (this.cantidad < this.existencia) {
              this.cantidad++;
          }
      },
      decrementar() {
          if (this.cantidad > 0) {
              this.cantidad--;
          }
      },
      capturar(){
        console.log(this.cantidad);
        const data ={
          "id_producto": this.id,
          "precio": this.precio, // ID de un producto existente
            "cantidad": this.cantidad,
            "total": this.precio* this.cantidad,
            "nombre":this.titulo
        }
        console.log("dato de la card",data);
        this.carrito(data)

      }
  }
}
</script>

<style>
.contenedor_prueba {
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.contenedor_prueba:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.titulo {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.descripcion {
  font-size: 1rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.precio {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.existencia {
  font-size: 0.875rem;
  color: #777;
  margin-bottom: 1rem;
}

.contador {
  display: flex;
  align-items: center;
}

.contador button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.contador button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.contador button:hover:not(:disabled) {
  background-color: #0056b3;
}

.cantidad {
  margin: 0 1rem;
  font-size: 1.5rem;
  font-weight: bold;
}
.agregar{
  padding-top: 15px;
}
.agregar:hover{
  color: gray;
}
</style>
