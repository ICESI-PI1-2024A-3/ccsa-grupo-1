document.getElementById('miBoton').addEventListener('click', function () {

    Swal.fire({
        html: `
            <!-- Bootstrap style sheet for CSS-->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
            <div class="input-group mb-4 mt-4">
                <span class="input-group-text">Tipo de espacio</span>
                <select class="form-select" name="classroom_type" id="select">
                    <option value="Aula" selected>Aula</option>
                    <option value="Laboratorio">Laboratorio</option>
                    <option value="Auditorio">Auditorio</option>
                </select>
            </div>
            <div class="input-group mb-4">
                <span class="input-group-text">Fecha de inicio</span>
                <input id="datetime1" type="datetime-local" class="form-control">
            </div>
            <div class="input-group">
                <span class="input-group-text">Fecha de finalización</span>
                <input id="datetime2" type="datetime-local" class="form-control">
            </div>
        `,
        title: 'Reserva de Espacios',
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
            const datetime2 = Swal.getPopup().querySelector('#datetime2').value;
            const salon = Swal.getPopup().querySelector('#select').value;
            if (!datetime1 || !datetime2 || !salon) {
                Swal.showValidationMessage('Debes seleccionar tanto las fechas como las horas, así como también especificar el tipo de salón.');
            }
            return {datetime1: datetime1, datetime2: datetime2, salon: salon};
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const data = {
                datetime1: result.value.datetime1,
                datetime2: result.value.datetime2,
                salon: result.value.salon
            };
            Swal.fire({
                html: `
                <!-- Bootstrap style sheet for CSS-->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
                <div class="p-1">Se le notificará por correo electrónico una vez la Oficina de Planeación Académica apruebe su solicitud.</div>
                `,
                titleText: "Solicitud Enviada Exitosamente",
                icon: "success",
                confirmButtonText: "Aceptar",
                confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
            });
        }
    });
});