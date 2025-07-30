import requests

# Cambia la URL base si tu servidor corre en otra dirección o puerto
BASE_URL = "http://127.0.0.1:5000"

# 1. REGISTRAR UN NUEVO CLIENTE
def registrar_usuario():
    url = f"{BASE_URL}/api/registro"
    # Puedes ajustar estos datos a tu modelo real
    data = {
        "nombre_completo": "Ejemplo Test",
        "whatsapp": "999888777",
        "correo": "testejemplo@mail.com",
        "fecha": "2025-07-31",
        "contrasena": "secretpass",
        "tipo_cliente_id": 1,
        "id_negocio": 1,
    }
    # Imagen a subir
    files = {
        "foto": open("ruta/tu_imagen.jpg", "rb")  # Cambia la ruta por una imagen local válida
    }
    resp = requests.post(url, data=data, files=files)
    print("Registro - status:", resp.status_code)
    print("Respuesta:", resp.json())
    return resp.json().get("id")

# 2. CONSULTAR USUARIO POR ID
def consultar_usuario(user_id):
    url = f"{BASE_URL}/api/usuario/{user_id}"
    resp = requests.get(url)
    print("Consulta - status:", resp.status_code)
    print("Usuario:", resp.json())

if __name__ == "__main__":
    # Registra un usuario y consulta el mismo ID
    user_id = registrar_usuario()
    if user_id:
        consultar_usuario(user_id)
