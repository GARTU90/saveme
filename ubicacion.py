import os
import requests
from dotenv import load_dotenv

# Cargar la clave API desde el archivo .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la clave API en las variables de entorno.")

# 1️⃣ Obtener ubicación actual
def obtener_ubicacion_actual():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"
    response = requests.post(url)
    data = response.json()
    #esto lo hice yo y probablemnte deba eliminarlo

    print(data)
    
    if "location" in data:
        lat, lng = data["location"]["lat"], data["location"]["lng"]
        return lat, lng
    else:
        print("❌ No se pudo obtener la ubicación actual.")
        return None, None

# 2️⃣ Convertir dirección en coordenadas (geocodificación)
def obtener_coordenadas(direccion):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        print("❌ No se pudo encontrar la dirección.")
        return None, None

# 3️⃣ Obtener ruta con Directions API
def obtener_ruta(origen_lat, origen_lng, destino_lat, destino_lng):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origen_lat},{origen_lng}&destination={destino_lat},{destino_lng}&mode=driving&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        return data
    else:
        print("❌ No se pudo calcular la ruta.")
        return None

# 4️⃣ Ejecutar el programa
if __name__ == "__main__":
    # Obtener ubicación actual
    lat_actual, lng_actual = obtener_ubicacion_actual()
    if lat_actual and lng_actual:
        print(f"📍 Ubicación actual: {lat_actual}, {lng_actual}")

        # Pedir dirección de destino
        destino = input("Introduce la dirección de destino: ")
        lat_destino, lng_destino = obtener_coordenadas(destino)

        if lat_destino and lng_destino:
            print(f"📍 Destino: {lat_destino}, {lng_destino}")

            # Obtener ruta
            ruta = obtener_ruta(lat_actual, lng_actual, lat_destino, lng_destino)
            if ruta:
                print("✅ Ruta encontrada. Primeras instrucciones:")
                for paso in ruta["routes"][0]["legs"][0]["steps"]:
                    print(f"- {paso['html_instructions']} ({paso['distance']['text']})")
                
                # Generar link de Google Maps con la ruta
                url_maps = f"https://www.google.com/maps/dir/{lat_actual},{lng_actual}/{lat_destino},{lng_destino}"
                print(f"🔗 Ver ruta en Google Maps: {url_maps}")
