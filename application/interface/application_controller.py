from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for

from users.domain.model.entities.user import role_to_user_type
from users.infraestructure.external_users_api.external_user_api import create_emprede_user

register_module_api = Blueprint('register_module_api', __name__)

@register_module_api.route('/register', methods=['GET'])
def show_applications():
    application_query_service = current_app.config["application_query_service"]
    plan_query_service = current_app.config["plan_query_service"]

    user_id = request.args.get('user_id')
    excedent_amount = request.args.get('excedent_amount')
    apps = application_query_service.list_all()
    # Junta los planes de cada app
    apps_data = []
    for app in apps:
        plans = plan_query_service.list_by_app_id(app.id)
        plans_dicts = [plan.to_dict() for plan in plans]  # CONVIERTE AQUÍ
        apps_data.append({
            "id": app.id,
            "name": app.name,
            "description": app.description,
            "plans": plans_dicts,  # SOLO DICTS AQUÍ
            "user_id": user_id,
            "excedent_amount": excedent_amount,
        })
    return render_template("register/netflix_apps.html", apps=apps_data)


from flask import current_app


@register_module_api.route('/register/user', methods=['GET', 'POST'])
def register_user():
    # ① ─── servicios que necesitamos siempre
    plan_query_service = current_app.config["plan_query_service"]

    if request.method == 'POST':
        # ---------- 1. Datos del formulario ----------
        nombre   = request.form['nombre']
        dni      = request.form['dni']
        email    = request.form['email']
        celular  = request.form['celular']
        username = request.form['username']
        password = request.form['password']
        id_tipo_usuario = 2
        role     = request.form['role']

        plan_id_raw   = request.form.get('plan_id')      # ← solo esto viaja oculto
        user_owner_id = request.form.get('user_owner_id')

        # plan_id es obligatorio para BUYER; lo convertimos seguro
        try:
            plan_id = int(plan_id_raw)
        except (TypeError, ValueError):
            flash("Plan no seleccionado o inválido.", "danger")
            return redirect(url_for('register_module_api.show_applications'))

        # ② ─── obtener plan ► nos da app_id
        plan_obj = plan_query_service.get_by_id(plan_id)
        if not plan_obj:
            flash("El plan indicado no existe.", "danger")
            return redirect(url_for('register_module_api.show_applications'))

        app_id = plan_obj.app_id   # lo usaremos al crear el usuario

        current_app.logger.info(
            "[REG] Form POST  » nombre=%s dni=%s email=%s username=%s role=%s plan_id=%s owner=%s",
            nombre, dni, email, username, role, plan_id, user_owner_id
        )

        # ---------- 2. Llama API externa ----------
        status, data = create_emprede_user(
            nombre, dni, email, celular, username,
            password, id_tipo_usuario, role
        )
        current_app.logger.info("[REG] API externa ← %s  %s", status, data)

        if status != 201:
            flash(f"Error API externa: {data.get('error', data)}", "danger")
            return redirect(request.url)

        account_id = data["id"]

        # ---------- 3. Crea usuario interno ----------
        user_service = current_app.config["user_command_service"]
        user_type    = role_to_user_type(role)

        try:
            user_obj = user_service.create(
                account_id   = account_id,
                app_id       = app_id,
                user_type    = user_type,
                user_owner_id= int(user_owner_id) if user_owner_id else None
            )
            current_app.logger.info("[REG] Usuario interno OK  id=%s", user_obj.id)
        except Exception as ex:
            current_app.logger.exception("[REG] Error creando usuario interno")
            flash("Error creando usuario interno: " + str(ex), "danger")
            return redirect(request.url)

        flash("¡Registro exitoso!", "success")

        # ---------- 4. Lógica de flujo ----------
        user_flow_service = current_app.config["user_flow_service"]
        user_flow_service.user_flow(user_obj.id, plan_id)

        return redirect(url_for('register_module_api.show_applications'))

    # ---------- GET ----------
    plan_id = request.args.get('plan_id')
    user_owner_id = request.args.get('user_owner_id')

    if plan_id:
        default_role = "BUYER"
        titulo = "Regístrate en EmprendeX Como Comprador"
    else:
        default_role = "AFILIATE"
        titulo = "Regístrate en EmprendeX Como Vendedor"

    current_app.logger.info("[REG] Render formulario  plan_id=%s owner=%s",
                            plan_id, user_owner_id)

    return render_template(
        "register/registro_usuario.html",
        plan_id       = plan_id,
        user_owner_id = user_owner_id,
        default_role  = default_role,
        titulo        = titulo
    )


@register_module_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Valida usuario/contraseña aquí...
        username = request.form['username']
        password = request.form['password']

        datos_user = {
            "id": 7,
            "username": username,
            "email": "algo@correo.com"
        }
        # Renderiza con datos_user solo si login OK
        return render_template('login/inicio_sesion.html', datos_user=datos_user)
    # GET normal
    return render_template('login/inicio_sesion.html')