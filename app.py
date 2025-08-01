from flask import Flask

from application.interface.application_controller import register_module_api
# Importa tu factory y DB initializer (ajusta la ruta real si es necesario)
from shared.factory.container_factory import build_services
from shared.infrastructure.database import init_db

# Importa tu blueprint de registro de módulos/apps

app = Flask(__name__)
app.secret_key = 'TU_SECRET_KEY_SEGURO'  # Pásalo por variable de entorno en producción

# Registra solo el blueprint que vas a probar (agrega otros luego si quieres)
app.register_blueprint(register_module_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()  # Inicializa tu base de datos, si aplica
        # Inyecta los servicios (dependency injection)
        services = build_services()
        for key, value in services.items():
            app.config[key] = value

if __name__ == '__main__':
    app.run(debug=True)
