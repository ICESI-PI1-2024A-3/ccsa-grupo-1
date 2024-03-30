(function () {
    const removal_btn = document.querySelectorAll(".removal-btn");

    removal_btn.forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            Swal.fire({
                title: "¿Está seguro de que desea eliminar el programa de posgrado?",
                text: "Esta acción no se puede revertir.",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    location.href = e.target.href;
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,
            });
        });
    });
})();