
// this is a global variable that will be used to store the value of class.subject.code
var code_clase;
var code_materia;

//create a new instance of the class, in class user the function import is called
document.addEventListener("DOMContentLoaded", function () {
    // get the value of class.subject.code from the HTML
    code_materia = document.getElementById("valor").textContent;
    code_clase = document.getElementById("valor_clase").textContent;

    // user the value as you wish
    console.log("El valor de class.subject.code es:", code_materia, "El valor de class.code es:", code_clase);
});

document.getElementById('start_date_class').addEventListener('click', function () {
    Swal.fire({
        html: `
            <!-- Bootstrap style sheet for CSS-->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
            <div class="input-group mb-4 mt-4">
                <span class="input-group-text">Fecha</span>
                <input id="datetime1" type="datetime-local" class="form-control">
            </div>
            
        `,
        title: 'Editar fecha inicio de clase',
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        cancelButtonColor: 'rgba(108, 117, 125)',
        confirmButtonText: 'Aceptar',
        showConfirmButton: true,
        confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
        reverseButtons: true,
        allowOutsideClick: false,
        preConfirm: () => {
            const datetime1 = Swal.getPopup().querySelector('#datetime1').value;
            if (!datetime1) {
                Swal.showValidationMessage('Debes seleccionar tanto las fechas como las horas.');
            }
            return { datetime1: datetime1, code_materia: code_materia, code_clase: code_clase };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const data = {
                code_materia: result.value.code_materia,
                code_clase: result.value.code_clase,
                datetime1: result.value.datetime1
            };
            Swal.fire({
                html: `
                <!-- Bootstrap style sheet for CSS-->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
                <div class="p-1">Se le notificará por correo electrónico una vez la Oficina de Planeación Académica apruebe su solicitud.</div>
                `,
                titleText: "cambio de fehca exitoso",
                icon: "success",
                confirmButtonText: "Aceptar",
                confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
            });
            // Send data to Django backend
            fetch('/dateCLass/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    // If the request was successful, you can take additional actions here
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

document.getElementById('end_date_class').addEventListener('click', function () {
    Swal.fire({
        html: `
            <!-- Bootstrap style sheet for CSS-->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
            <div class="input-group mb-4 mt-4">
                <span class="input-group-text">Fecha</span>
                <input id="datetime1" type="datetime-local" class="form-control">
            </div>
            
        `,
        title: 'Editar fecha fin de clase',
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        cancelButtonColor: 'rgba(108, 117, 125)',
        confirmButtonText: 'Aceptar',
        showConfirmButton: true,
        confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
        reverseButtons: true,
        allowOutsideClick: false,
        preConfirm: () => {
            const datetime1 = Swal.getPopup().querySelector('#datetime1').value;
            if (!datetime1) {
                Swal.showValidationMessage('Debes seleccionar tanto las fechas como las horas.');
            }
            return { datetime1: datetime1, code_materia: code_materia, code_clase: code_clase };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const data = {
                code_materia: result.value.code_materia,
                code_clase: result.value.code_clase,
                datetime1: result.value.datetime1
            };
            Swal.fire({
                html: `
                <!-- Bootstrap style sheet for CSS-->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
                <div class="p-1">Se le notificará por correo electrónico una vez la Oficina de Planeación Académica apruebe su solicitud.</div>
                `,
                titleText: "cambio de fehca exitoso",
                icon: "success",
                confirmButtonText: "Aceptar",
                confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
            });
            // Send data to Django backend
            fetch('/dateCLass/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    // If the request was successful, you can take additional actions here
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