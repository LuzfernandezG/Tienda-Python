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