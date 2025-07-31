import requests

BASE_URL = "http://127.0.0.1:5000"




def create_emprede_user(nombre, dni, email, celular, username, password, id_tipo_usuario, role):
    payload = {
        "nombre": nombre,
        "dni": dni,
        "email": email,
        "celular": celular,
        "username": username,
        "password": password,
        "id_tipo_usuario": id_tipo_usuario,
        "role": role   # siempre se envía role
    }
    response = requests.post(f"{BASE_URL}/external_api/crear", json=payload)
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text



def find_by_emprende_user_id(user_id):
    response = requests.get(f"{BASE_URL}/external_api/{user_id}")
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text
