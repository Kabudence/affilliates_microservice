import json
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("fullventas-api")

BASE_URL = "https://cascadagym.fulventas.com/public/json"

def register_fullventas_user(
    type_, first_name, username, email, password, dni, mobile, verify=False
):
    url = f"{BASE_URL}/register_cliente.php"
    payload = {
        "type": type_,
        "first_name": first_name,
        "username": username,
        "email": email,
        "password": password,
        "dni": dni,
        "mobile": mobile
    }
    log.info("POST  %s  » %s", url, json.dumps(payload))
    try:
        resp = requests.post(url, json=payload, timeout=15, verify=False)
    except requests.RequestException as err:
        log.error("✖  Error de red: %s", err)
        raise

    log.info("← %s %s", resp.status_code, resp.text[:150])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


def find_fullventas_user_by_id(user_id: int):
    """
    GET /find_clienteById.php?user_id=<user_id>
    Devuelve (status_code, json|texto)
    """
    url = f"{BASE_URL}/find_clienteById.php?user_id={user_id}"
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


def update_fullventas_tienda(
    user_id: int,
    business_name: str,
    district: str,
    gallery: str,
    razon_social: str,
    ruc: str,
    useraddress: str,
    cod_distrito: str,
verify=False
):
    """
    POST /update_user_tienda.php
    Devuelve (status_code, json|texto)
    """
    url = f"{BASE_URL}/update_user_tienda.php"
    payload = {
        "user_id": user_id,
        "business_name": business_name,
        "district": district,
        "gallery": gallery,
        "razon_social": razon_social,
        "ruc": ruc,
        "useraddress": useraddress,
        "cod_distrito": cod_distrito
    }
    log.info("POST  %s  » %s", url, json.dumps(payload))
    try:
        resp = requests.post(url, json=payload, timeout=15, verify=verify)
    except requests.RequestException as err:
        log.error("✖  Error de red: %s", err)
        raise

    log.info("← %s %s", resp.status_code, resp.text[:150])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


def login_fullventas_user(username: str, password: str, *, verify = False):
    """
    1) POST  /simulator_login.php      → valida credenciales
    2) GET   /find_clienteById.php     → trae ficha completa
    Devuelve (status_code, json-completo | texto)
    """
    # ---------- 1. LOGIN ----------
    login_url = f"{BASE_URL}/simulator_login.php"
    payload   = {"username": username, "password": password}
    log.info("POST  %s  » %s", login_url, json.dumps(payload))
    try:
        login_resp = requests.post(login_url, json=payload, timeout=10, verify=False)
    except requests.RequestException as err:
        log.error("✖  Error de red (login): %s", err)
        raise

    log.info("← %s %s", login_resp.status_code, login_resp.text[:150])

    # Si no fue 200 ó el JSON es inválido, salimos con la respuesta tal cual
    try:
        login_data = login_resp.json()
    except ValueError:
        return login_resp.status_code, login_resp.text

    # Si el login falló, devolvemos lo mismo que el endpoint
    if login_resp.status_code != 200 or "user" not in login_data:
        return login_resp.status_code, login_data

    # ---------- 2. FICHA COMPLETA ----------
    user_id = login_data["user"].get("user_id")
    if not user_id:                         # Sanity check
        return login_resp.status_code, login_data

    detail_url = f"{BASE_URL}/find_clienteById.php?user_id={user_id}"
    log.info("GET  %s", detail_url)
    try:
        detail_resp = requests.get(detail_url, timeout=10, verify=verify)
    except requests.RequestException as err:
        log.warning("⚠ No se pudo obtener ficha completa: %s", err)
        # devolvemos el login mínimo, pero avisamos con un flag
        login_data["partial_data"] = True
        return login_resp.status_code, login_data

    log.info("← %s %s", detail_resp.status_code, detail_resp.text[:150])

    try:
        detail_data = detail_resp.json()
    except ValueError:
        # Si la ficha completa no es JSON, devolvemos el login mínimo
        login_data["partial_data"] = True
        return login_resp.status_code, login_data

    # Si obtenemos la ficha completa correctamente, devolvemos eso
    if detail_resp.status_code == 200 and "user" in detail_data:
        return 200, detail_data  # <- user completo
    else:
        # fallback: login mínimo
        login_data["partial_data"] = True
        return login_resp.status_code, login_data
