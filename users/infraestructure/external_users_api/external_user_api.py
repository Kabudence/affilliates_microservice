import json
import logging
import requests
from datetime import datetime

# Configura el logger (una sola vez en tu micro-servicio)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("external-api")

BASE_URL   = "http://192.168.18.82:5000"
API_PREFIX = "/external_api/usuarios"     # Ajusta si cambias prefijo

# ----------  CREATE  ----------
def create_emprede_user(nombre, dni, email, celular, username, password,
                        id_tipo_usuario, role):
    """
    POST  /external_api/usuarios/crear
    Devuelve (status_code, json|texto)
    """
    url = f"{BASE_URL}{API_PREFIX}/crear"
    payload = {
        "nombre": nombre, "dni": dni, "email": email, "celular": celular,
        "username": username, "password": password,
        "id_tipo_usuario": id_tipo_usuario, "role": role
    }

    log.info("POST  %s  » %s", url, json.dumps(payload))
    try:
        resp = requests.post(url, json=payload, timeout=10)
    except requests.RequestException as err:
        log.error("✖  Error de red: %s", err)
        raise

    log.info("← %s %s", resp.status_code, resp.text[:150])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


# ----------  FIND BY ID  ----------
def find_by_emprende_user_id(user_id: int):
    """
    GET /external_api/usuarios/<user_id>
    """
    url = f"{BASE_URL}{API_PREFIX}/{user_id}"
    log.info("GET  %s", url)

    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException as err:
        log.error("✖  Error de red: %s", err)
        raise

    log.info("← %s %s", resp.status_code, resp.text[:150])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text
