import pytest
from time import sleep

from users.infraestructure.external_users_api.external_user_api import crear_usuario_api, buscar_usuario_por_id_api







def test_crear_y_buscar_usuario():
    # 1. Crear usuario único (usar un correo y username único para cada pytest)
    email = "testuser123@mail.com"
    username = "testuser123"
    status_create, resp_create = crear_usuario_api(
        nombre="Test User",
        dni="87654321",
        email=email,
        celular="988877766",
        username=username,
        password="abc123",
        id_tipo_usuario=2
    )
    assert status_create == 201, f"Falló creación: {resp_create}"

    user_id = resp_create.get("id")
    assert user_id is not None, "No devolvió el id del usuario creado"

    # Opcional: esperar 1 segundo si tu backend tiene demoras en commit
    # sleep(1)

    # 2. Buscar usuario por id
    status_find, resp_find = buscar_usuario_por_id_api(user_id)
    assert status_find == 200, f"Falló búsqueda: {resp_find}"
    assert resp_find["username"] == username
    assert resp_find["email"] == email
    assert resp_find["dni"] == "87654321"
    assert resp_find["nombre"] == "Test User"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
