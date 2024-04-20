function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

(function () {
    
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

                    const urlParts = window.location.pathname.split('/');
                    const teacherId = urlParts[urlParts.length - 2];

                    const data = {
                        tiquetes: result.value.tiquetes,
                        hotel: result.value.hotel,
                        viatico: result.value.viatico,
                        id_teacher: teacherId
                    };

                    fetch('/save_viatic/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')  
                        },
                        body: JSON.stringify(data)
                    }).then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            Swal.fire('Éxito', data.message, 'success');
                        } else if (data.error) {
                            Swal.fire('Error', data.error, 'error');
                        }
                    });
                }
            });            
    });        
})();