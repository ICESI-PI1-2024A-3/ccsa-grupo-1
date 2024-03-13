document.getElementById('miBoton').addEventListener('click', function() {
  Swal.fire({
    title: 'Selecciona una fecha y hora',
    html: `
      <p><input id="datetime1" type="datetime-local" class="swal-input"></p>
      <p><input id="datetime2" type="datetime-local" class="swal-input"></p>
    `,
    showCancelButton: true,
    confirmButtonText: 'Aceptar',
    cancelButtonText: 'Cancelar',
    input: 'select',
    inputPlaceholder: 'Selecciona tipo de salón',
    inputValue: '',
    inputOptions: {
      'Aula': 'Aula',
      'Laboratorio': 'Laboratorio',
      'Auditorio': 'Auditorio'
    },
    preConfirm: () => {
      const datetime1 = Swal.getPopup().querySelector('#datetime1').value;
      const datetime2 = Swal.getPopup().querySelector('#datetime2').value;
      const salon = Swal.getPopup().querySelector('select').value;
      if (!datetime1 || !datetime2 || !salon) {
        Swal.showValidationMessage('Debes seleccionar ambas fechas, horas y el tipo de salón');
      }
      return { datetime1: datetime1, datetime2: datetime2, salon: salon };
    }
  }).then((result) => {
    if (result.isConfirmed) {
      const datos = {
        datetime1: result.value.datetime1,
        datetime2: result.value.datetime2,
        salon: result.value.salon
      };

      // Envía los datos al backend de Django
      
      fetch('/dataProcessor_lounge/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
      }).then(response => {
        if (response.ok) {
          // Si la solicitud fue exitosa, puedes realizar acciones adicionales aquí
          console.log('Datos enviados correctamente');
        } else {
          console.error('Error al enviar datos al servidor');
        }
      }).catch(error => {
        console.error('Error:', error);
      });
       
    }
  });
});



// Estilos CSS
const styles = `
.swal-input {
  width: 90%;
  padding: .375rem .75rem;
  font-size: 1rem;
  border-radius: .25rem;
  border: 1px solid #ced4da;
}

.swal-input:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
`;

// Crear un elemento <style> y agregar los estilos CSS
const styleElement = document.createElement('style');
styleElement.innerHTML = styles;
document.head.appendChild(styleElement);

