document.addEventListener('DOMContentLoaded', function() {
    var regionSelect = document.getElementById('id_region');
    var comunaSelect = document.getElementById('id_comuna');

    regionSelect.addEventListener('change', function() {
        var regionId = this.value;
        if (regionId) {
            fetch(`/comunas_por_region/${regionId}/`)
                .then(response => response.json())
                .then(data => {
                    comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
                    data.forEach(comuna => {
                        comunaSelect.innerHTML += `<option value="${comuna.id}">${comuna.nombre}</option>`;
                    });
                });
        } else {
            comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
        }
    });
});
