//FUNCIONES PARA MANEJO DE BACKEND
import { swallTrue,swallError, swallConfirmation } from "./alerts";
import axios from "axios";
import Cookies from 'js-cookie';


  export async function Categorias() {
    try {
      const response = await axios.get(`productos`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }
  export async function Productos(id) {
    try {
      const response = await axios.get(`productos/inventario/?id=${id}`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }
  Productos(2)

  // export function formatearFecha(fecha) {
  //   const fechaObj = new Date(fecha);
  //   const opciones = {
  //     dia: 'numeric',
  //     mes: 'short',
  //     año: 'numeric',
  //     hora: 'numeric',
  //     minuto: 'numeric',
  //   };
  
  //   const fechaFormateada = `${fechaObj.getDate().toString().padStart(2, '0')} ${fechaObj.toLocaleString('es-ES', { month: 'short' })} ${fechaObj.getFullYear()}`;
  
  //   return fechaFormateada;
  // }

  export async function listarProductos(data) {
    try {
      const response = await axios.post('/api/publicacion', data);
      console.log(response.data);
      swallTrue(`Publicacion creada exitosamente`);
      return response; 
    } catch (error) {
      console.log(error);
      swallError(`Error en la creacion de la publicacion: ${error.response?.data?.message || 'Error desconocido'}`);
      throw error; 
    }
  }

  // export async function deletePost(id) {
  //   // Confirmación de eliminación
  //   const confirmed = await swallConfirmation("¿Seguro que desea eliminar la publicación?");
  
  //   if (!confirmed) return; // Salir si no se confirma
  
  //   try {
  //     // Realizar solicitud DELETE
  //     const response = await axios.delete(`/api/publicacion/${id}`);
  //     console.log(response);
  
  //     // Mostrar mensaje de éxito
  //     swallTrue(`${response.data.mensaje}`);
  //     return response;
  //   } catch (error) {
  //     // Manejar error
  //     console.error(error);
  //     swallError(`Error al eliminar la publicación: ${error.response?.data?.message || 'Error desconocido'}`);
  //     throw error;
  //   }
  // }

  // export async function editPost(id,data) {
  //   // Confirmación de eliminación
  //   const confirmed = await swallConfirmation("¿Seguro que desea cambiar la informacion?");
  
  //   if (!confirmed) return; 
  
  //   try {
  //     // Realizar solicitud DELETE
  //     const response = await axios.put(`/api/publicacion/${id}`,data);
  //     console.log(response);
  
  //     // Mostrar mensaje de éxito
  //     swallTrue(`${response.data.mensaje}`);
  
  //     return response;
  //   } catch (error) {
  //     // Manejar error
  //     console.error(error);
  //     swallError(`Error al eliminar la publicación: ${error.response?.data?.mensaje || 'Error desconocido'}`);
  //     throw error;
  //   }
  // }


  
 
