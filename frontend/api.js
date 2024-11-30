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

  export async function TotalProductos() {
    try {
      const response = await axios.get(`productos/listar/`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }

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

  export async function Clientes() {
    try {
      const response = await axios.get(`ventas/`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }
 
  export async function agregarVenta(data) {
    try {
      const response = await axios.post('ventas/registro/', data);
      console.log(response.data);
      swallTrue(`Venta creada`);
      return response; 
    } catch (error) {
      console.log(error);
      swallError(`Error en la creacion de la publicacion: ${error.response?.data?.message || 'Error desconocido'}`);
      throw error; 
    }
  }


  export async function ApiWhatsapp(message) {7
    console.log(message)
    if (!message) {
      throw new Error('Mesaje no proporcionado');
    }
    try {
      const req1 = await fetch(`http://127.0.0.1:3001/lead`, {
        method: 'POST',
        mode:"cors",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message), 
      });
  
      if (!req1.ok) {
        return { error: true, statusText: req1.statusText };
      }
   
      const respuesta = await req1.json();
      return respuesta;
  
    } catch (error) {
      console.error('Error en la llamada a la API:', error);
      return { error: true, message: error.message };
    }
  }

  export async function AgregarCliente(data) {
    try {
      const response = await axios.post('ventas/', data);
      console.log(response.data);
      swallTrue(`Cliente agregado`);
      return response; 
    } catch (error) {
      console.log(error);
      swallError(`Error en la creacion del cliente`);
      throw error; 
    }
  }

  export async function ConsultarDeuda(cedula) {
    try {
      const response = await axios.get(`ventas/registro/?cc=${cedula}`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      swallError(`El cliente no existe`);
      console.log(error);
      throw error; 
    }
  }
 

  export async function PanelVentas() {
    try {
      const response = await axios.get(`ventas/administrar`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }

  export async function Actualizar(data) {
    try {
      const response = await axios.put(`ventas/registro/`,data);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }

  
  export async function AbonoDeudas(data) {
    try {
      const response = await axios.post(`ventas/administrar/`,data);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }

  export async function CerrarDeuda(id,cedula) {
  
    try {
      const response = await axios.delete(`ventas/administrar/?id=${id}&cedula=${cedula}`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }


  export async function DashboardGraficos() {
    try {
      const response = await axios.get(`reportes/`);
      const result= response.data;
      console.log(result);
      return result; 
    } catch (error) {
      console.log(error);
      throw error; 
    }
  }

  export async function Consultar(data) {
    try {
      const response = await axios.post(`reportes/`,data);
      const result= response.data;
      console.log(result);
      swallTrue(`Encontrado`);
      return result; 
    } catch (error) {
      console.log(error);
      swallError(`Error de consulta`);
      throw error; 
    }
  }





  
 
