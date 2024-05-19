document.getElementById('regionSelect').addEventListener('change', function() {
    var regionId = this.value;
    var comunaSelect = document.getElementById('comunaSelect');
    var comunas = comunaSelect.querySelectorAll('option[data-region]');
    
    comunaSelect.value = ''; // Reset the comuna select
    comunas.forEach(function(comuna) {
        if (regionId === '' || comuna.getAttribute('data-region') === regionId) {
            comuna.style.display = 'block';
        } else {
            comuna.style.display = 'none';
        }
    });
});
