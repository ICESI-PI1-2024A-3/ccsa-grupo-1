(function () {
    // Cuando se hace clic en el botón "Solicitar viático", se muestra el modal
    document.getElementById('solicitar-viatico-btn').addEventListener('click', function () {
        Swal.fire({
            html: `
            <!-- Bootstrap style sheet for CSS-->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
            <div class="input-group mb-3">
                <span class="input-group-text">Tiquetes</span>
                <select class="form-select" id="tiquetes-select">
                    <option value="Si">Si</option>
                    <option value="No">No</option>
                </select>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">Hotel</span>
                <select class="form-select" id="hotel-select">
                    <option value="Si">Si</option>
                    <option value="No">No</option>
                </select>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">Viático</span>
                <select class="form-select" id="viatico-select">
                    <option value="Si">Si</option>
                    <option value="No">No</option>
                </select>
            </div>
            `,
            title: 'Solicitud de viáticos',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            cancelButtonColor: 'rgba(108, 117, 125)',
            confirmButtonText: 'Aceptar',
            showConfirmButton: true,
            confirmButtonColor: 'rgba(23, 104, 172, 0.9)',
            reverseButtons: true,
            allowOutsideClick: false,
            preConfirm: () => {
                const tiquetes = Swal.getPopup().querySelector('#tiquetes-select').value;
                const hotel = Swal.getPopup().querySelector('#hotel-select').value;
                const viatico = Swal.getPopup().querySelector('#viatico-select').value;
            
                if (!tiquetes || !hotel || !viatico) {
                    Swal.showValidationMessage('Debes seleccionar tanto los tiquetes, el hotel y el viático.');
                }
                return {tiquetes: tiquetes, hotel: hotel, viatico: viatico};
            }
            }).then((result) => {
                if (result.isConfirmed) {
                    const data = {
                        tiquetes: result.value.tiquetes,
                        hotel: result.value.hotel,
                        viatico: result.value.viatico
                    };
            
                    $.ajax({
                        url: '/ruta/a/tu/vista/',  // Actualiza esto con la ruta a tu vista
                        method: 'POST',
                        data: {
                            'transport': data.tiquetes,
                            'accommodation': data.hotel,
                            'viatic': data.viatico,
                            'teacher_id': id_del_profesor,  // Actualiza esto con el ID del profesor
                        },
                        success: function (response) {
                            if (response.status === 'success') {
                                Swal.fire({
                                    html: `
                                    <!-- Bootstrap style sheet for CSS-->
                                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
                                    <div class="p-1">Recibirá un correo de confirmación cuando su solicitud sea aprobada.</div>
                                    `,
                                    titleText: "Solicitud enviada",
                                    icon: "success",
                                    confirmButtonText: "Aceptar",
                                    confirmButtonColor: 'rgba(23, 104, 172, 0.9)'
                                });
                            } else {
                                Swal.fire('¡Error!', 'Hubo un error al guardar la solicitud de viáticos.', 'error');
                            }
                        },
                    });
                }
            });            
    });        

    // Cuando se hace clic en el botón "Aceptar" dentro del modal, se muestra un mensaje de confirmación
    document.getElementById('solicitar-viatico-confirm-btn').addEventListener('click', function () {
        const tiquetes = document.getElementById('tiquetes-select').value;
        const hotel = document.getElementById('hotel-select').value;
        const viatico = document.getElementById('viatico-select').value;

        if (!tiquetes || !hotel || !viatico) {
            Swal.showValidationMessage('Debes seleccionar tanto los tiquetes, el hotel y el viático.');
        } else {
            const data = {
                tiquetes: tiquetes,
                hotel: hotel,
                viatico: viatico
            };

            Swal.fire({
                html: `
                <!-- Bootstrap style sheet for CSS-->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
                <div class="p-1">Recibirá un correo de confirmación cuando su solicitud sea aprobada.</div>
                `,
                titleText: "Solicitud enviada",
                icon: "success",
                confirmButtonText: "Aceptar",
                confirmButtonColor: 'rgba(23, 104, 172, 0.9)'
            });

            var viaticRequestModal = bootstrap.Modal.getInstance(document.getElementById('viatic-request-modal'));
            viaticRequestModal.hide();
        }
    });
})();