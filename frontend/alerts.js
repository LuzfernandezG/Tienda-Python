import Swal from 'sweetalert2';

export const swallTrue = (mensaje) => {
  return Swal.fire({
    title: '¡Éxito!',
    text: mensaje,
    icon: 'success',
    confirmButtonText: 'Aceptar',
  });
};

export const swallError = (mensaje) => {
  return Swal.fire({
    title: '¡Error!',
    text: mensaje,
    icon: 'error',
    confirmButtonText: 'Aceptar',
  });
};

export const swallConfirmation = (mensaje) => {
    return Swal.fire({
      title: 'Información',
      text: mensaje,
      icon: 'info',
      showCancelButton: true, 
      confirmButtonText: 'Aceptar',
      cancelButtonText: 'Cancelar', 
    }).then((result) => {
      return result.isConfirmed; 
    });
  };

  export const swallInput = async (options = {}) => {
   
    const {
      title = "¿Qué opinas sobre el Post?",
      inputLabel = "Ingresa tu comentario aquí",
      inputValue = "",
      errorMessage = "¡Mal ingreso!",
      showCancelButton = true,
      customClass = {}, 
      inputType = "text", 
    } = options;
  
    // Llamada a SweetAlert2
    const { value } = await Swal.fire({
      title,
      input: inputType,
      inputLabel,
      inputValue,
      showCancelButton,
      inputValidator: (value) => {
        if (!value) {
          return errorMessage;
        }
      },
   
    });
    return value || null;
  };



  export const swallForm = async () => {
    const { value: formValues } = await Swal.fire({
      title: "Agregar Cliente",
      html: `
        <input id="nombre" placeholder="Nombre" type="text" class="swal2-input">
        <input id="cedula" placeholder="Cédula" type="number" class="swal2-input">
        <input id="correo" placeholder="Correo" type="email" class="swal2-input">
        <input id="telefono" placeholder="Teléfono" type="number" class="swal2-input">
      `,
      focusConfirm: false,
      preConfirm: () => {
        return {
          nombre: document.getElementById("nombre").value,
          cedula: document.getElementById("cedula").value,
          correo: document.getElementById("correo").value,
          telefono: document.getElementById("telefono").value,
        };
      }
    });
  
    if (formValues) {
      return formValues; 
    }
    return null;
  };


  export const swallAbono = async () => {
    const { value: formValues } = await Swal.fire({
      title: "Agregar Abono",
      html: `
        <label>Valor a ingresar:</label>
        <input id="valor" placeholder="Valor $" type="number" min="1" class="swal2-input">
      `,
      focusConfirm: false,
      preConfirm: () => {
        return {
          valor: document.getElementById("valor").value,
        };
      }
    });
  
    if (formValues) {
      return formValues; 
    }
    return null;
  };

  export const swallToast = async (texto) => {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    }
  });
  Toast.fire({
    icon: "success",
    title: texto
  });
}