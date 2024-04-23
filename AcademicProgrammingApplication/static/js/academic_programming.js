(function () {
    // Select all elements with the class "removal-btn" and store them in a constant
    const removal_btn = document.querySelectorAll(".removal-btn");

    // Iterate over each element with the class "removal-btn"
    removal_btn.forEach(btn => {
        // Prevent the default behavior of the click event
        btn.addEventListener("click", function (e) {
            // Prevent the default behavior of the click event
            e.preventDefault();
            // Display a SweetAlert modal with a confirmation message
            Swal.fire({
                title: "¿Está seguro de que desea eliminar el programa de posgrado?",
                text: "Esta acción no se puede revertir.",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                backdrop: true,
                showLoaderOnConfirm: true,
                // When the user confirms, redirect to the URL specified in the button's href attribute
                preConfirm: () => {
                    location.href = e.target.href;
                },
                // Prevent the modal from being closed by clicking outside of it or pressing the escape key
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,
            });
        });
    });
})();