import requests

def carrega_coordenadas(endereco):
    """
    Faz a geocodificação de um endereço para obter suas coordenadas geográficas
    (latitude e longitude) utilizando a API do Google Maps.

    Parâmetros:
        endereco (str): O endereço completo a ser geocodificado.

    Retorno:
        tuple: Um par de valores (latitude, longitude) se a geocodificação for bem-sucedida.
        None: Se ocorrer algum erro ou o endereço não for encontrado.
    """
    
    if not endereco or not isinstance(endereco, str):
        raise ValueError("Endereço inválido. Verifique se o endereço é uma string válida.")
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": endereco,
        "key": "AIzaSyCj2Tn5LiWlTUgevFKlQ7aUku8ZxYyjyXM"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)  # Adiciona timeout de 10 segundos
        response.raise_for_status()  # Levanta exceção se a resposta não for 200 OK
        data = response.json()
        
        if data.get("status") == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            latitude = location.get("lat")
            longitude = location.get("lng")
            
            if latitude is not None and longitude is not None:
                return latitude, longitude
            else:
                return None  # Coordenadas não encontradas
        
        else:
            return None  # Status diferente de "OK" ou resultados vazios

    except requests.exceptions.Timeout:
        print("Erro: A solicitação à API demorou muito para responder.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None
