import requests

BASE_URL = "http://127.0.0.1:5000"




def crear_usuario_api(nombre, dni, email, celular, username, password, id_tipo_usuario):
    payload = {
        "nombre": nombre,
        "dni": dni,
        "email": email,
        "celular": celular,
        "username": username,
        "password": password,
        "id_tipo_usuario": id_tipo_usuario
    }
    response = requests.post(f"{BASE_URL}/external_api/crear", json=payload)
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text


def buscar_usuario_por_id_api(user_id):
    response = requests.get(f"{BASE_URL}/external_api/{user_id}")
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text
