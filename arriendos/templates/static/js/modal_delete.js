$(document).ready(function () {
    // Manejar clic en cualquier botón con la clase 'btnEliminar'
    $('.btnEliminar').click(function (e) {
        e.preventDefault(); // Evitar que el enlace redirija
        var form = $(this).closest('form'); // Obtener el formulario más cercano
        
        // Ajustar acción del formulario según el tipo de eliminación
        if ($(this).data('bs-target') == "#eliminarModal") {
            form = $('#eliminarUsuarioForm'); // Usar el formulario específico del modal
        }
        
        $('#eliminarModal').data('form', form); // Guardar el formulario en el modal
        $('#eliminarModal form').attr('action', form.attr('action')); // Asignar la action del formulario original al formulario del modal
        $('#eliminarModal').modal('show'); // Mostrar el modal
    });

    // Manejar clic en el botón "Aceptar" del modal
    $('#btnConfirmarEliminar').click(function(e) {
        e.preventDefault();
        var modal = $('#eliminarModal');
        var form = modal.data('form'); // Obtener el formulario guardado
        form.submit(); // Enviar el formulario
    });
});