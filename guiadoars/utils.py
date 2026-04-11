from geopy.geocoders import Nominatim
import time

def geocode_endereco(endereco_completo, tentativas=3):
    """
    Converte um endereço em latitude/longitude usando Nominatim (OpenStreetMap).
    Retorna uma tupla (latitude, longitude) ou (None, None) se falhar.
    """
    geolocator = Nominatim(user_agent="guia_doar_app")  # Identificação do seu app
    for i in range(tentativas):
        try:
            location = geolocator.geocode(endereco_completo, timeout=5)
            if location:
                return location.latitude, location.longitude
        except Exception as e:
            print(f"Erro na geocodificação (tentativa {i+1}): {e}")
        time.sleep(1)  # Respeita o limite de 1 requisição por segundo
    return None, None