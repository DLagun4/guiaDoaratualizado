(function() {
    function initMap() {
        var latField = document.getElementById('id_latitude');
        var lngField = document.getElementById('id_longitude');
        if (!latField || !lngField) return;

        // Pega os valores atuais ou define padrão (centro do Brasil)
        var lat = parseFloat(latField.value) || -14.2350;
        var lng = parseFloat(lngField.value) || -51.9253;

        // Cria o container do mapa
        var container = document.createElement('div');
        container.id = 'mapa-admin';
        container.style.height = '400px';
        container.style.width = '100%';
        container.style.marginTop = '10px';
        container.style.marginBottom = '10px';
        container.style.border = '1px solid #ccc';
        container.style.borderRadius = '8px';

        // Insere o mapa depois do campo de longitude (ou do último fieldset)
        var parent = lngField.closest('.form-row') || lngField.parentNode.parentNode;
        parent.parentNode.insertBefore(container, parent.nextSibling);

        // Carrega Leaflet se não estiver carregado
        if (typeof L === 'undefined') {
            var leafletCss = document.createElement('link');
            leafletCss.rel = 'stylesheet';
            leafletCss.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
            document.head.appendChild(leafletCss);

            var leafletJs = document.createElement('script');
            leafletJs.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
            leafletJs.onload = function() {
                criarMapa(lat, lng);
            };
            document.head.appendChild(leafletJs);
        } else {
            criarMapa(lat, lng);
        }

        function criarMapa(lat, lng) {
            var map = L.map(container.id).setView([lat, lng], 15);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            var marker = L.marker([lat, lng], {draggable: true}).addTo(map);

            marker.on('dragend', function(e) {
                var pos = marker.getLatLng();
                latField.value = pos.lat.toFixed(6);
                lngField.value = pos.lng.toFixed(6);
                // Dispara um evento 'change' para o Django admin registrar a alteração
                latField.dispatchEvent(new Event('change'));
                lngField.dispatchEvent(new Event('change'));
            });

            map.on('click', function(e) {
                marker.setLatLng(e.latlng);
                latField.value = e.latlng.lat.toFixed(6);
                lngField.value = e.latlng.lng.toFixed(6);
                latField.dispatchEvent(new Event('change'));
                lngField.dispatchEvent(new Event('change'));
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMap);
    } else {
        initMap();
    }
})();