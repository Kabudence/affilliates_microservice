from flask import Blueprint, render_template, redirect, url_for, request, current_app,flash, session

from users.domain.model.entities.user import role_to_user_type
from users.infraestructure.external_users_api.external_emprende_user_api import create_emprede_user, login_emprende_user
from users.infraestructure.external_users_api.external_fullventas_user_api import register_fullventas_user

register_module_api = Blueprint('register_module_api', __name__)

@register_module_api.route('/register', methods=['GET'])
def show_applications():
    application_qs      = current_app.config["application_query_service"]
    plan_qs             = current_app.config["plan_query_service"]
    module_qs           = current_app.config["module_query_service"]
    plan_time_qs        = current_app.config["plan_time_query_service"]

    user_id         = request.args.get('user_id')
    excedent_amount = request.args.get('excedent_amount')
    app_id          = request.args.get('app_id', type=int)

    apps_data = []

    apps = [application_qs.get_by_id(app_id)] if app_id else application_qs.list_all()

    for app in apps:
        if not app:
            continue
        plans_raw = plan_qs.list_by_app_id(app.id)

        plans = []
        for p in plans_raw:
            # módulos de este plan
            modules = module_qs.get_all_by_plan_id(p.id)      # ← NUEVO
            # tomamos el precio + corto (ej.: 1 mes) si existe
            times   = plan_time_qs.list_by_plan_id(p.id)
            times_sorted = sorted(times, key=lambda t: t.duration or 99)
            price   = times_sorted[0].price if times_sorted else None
            promos = [{"id": t.id, "duration": t.duration, "price": t.price}
                      for t in times_sorted]

            plans.append({
                "id"         : p.id,
                "name"       : p.name,
                "plan_type"  : p.plan_type.value,
                "price"      : price,
                "modules": [m.to_dict() for m in modules],
                "promos": promos,

            })

        apps_data.append({
            "id"            : app.id,
            "name"          : app.name,
            "description"   : app.description,
            "plans"         : plans,
            "user_id"       : user_id,
            "excedent_amount": excedent_amount,
        })

    return render_template("register/netflix_apps.html", apps=apps_data)



@register_module_api.route('/register/user', methods=['GET', 'POST'])
def register_user():
    plan_query_service = current_app.config["plan_query_service"]
    plan_time_query_service = current_app.config["plan_time_query_service"]
    plan_time_id = request.args.get('plan_time_id')
    plan_time = plan_time_query_service.get_by_id(int(plan_time_id)) if plan_time_id else None
    plan_id_raw = plan_time.plan_id if plan_time else None
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
        account_id = None
        app_name=None
        if app_id == 1:
            status, data = create_emprede_user(
                nombre, dni, email, celular, username,
                password, id_tipo_usuario, role
            )
            app_name = "Emprende"
            current_app.logger.info("[REG] API externa ← %s  %s", status, data)
            if status != 201:
                flash(f"Error API externa: {data.get('error', data)}", "danger")
                return redirect(request.url)
            account_id = data.get("id")
        elif app_id == 2:
            app_name = "Fullventas"
            status, data = register_fullventas_user(
                type_=2,
                first_name=nombre,
                username=username,
                email=email,
                password=password,
                dni=dni,
                mobile=celular
            )
            current_app.logger.info("[REG] API Fullventas ← %s  %s", status, data)
            if status != 200:
                flash(f"Error API Fullventas: {data.get('message') or data.get('error') or data}", "danger")
                return redirect(request.url)
            account_id = data.get("user_id") or data.get("id")

        if not account_id:
            flash("No se pudo obtener el ID del usuario externo.", "danger")
            return redirect(request.url)

        # ---------- 3. Crea usuario interno ----------
        user_service = current_app.config["user_command_service"]
        user_type = role_to_user_type(role)

        try:
            user_obj = user_service.create(
                account_id=account_id,
                app_id=app_id,
                user_type=user_type,
                user_owner_id=int(user_owner_id) if user_owner_id else None
            )
            current_app.logger.info("[REG] Usuario interno OK  id=%s", user_obj.id)
        except Exception as ex:
            current_app.logger.exception("[REG] Error creando usuario interno")
            flash("Error creando usuario interno: " + str(ex), "danger")
            return redirect(request.url)

        flash("¡Registro exitoso!", "success")

        # ---------- 4. Lógica de flujo ----------
        user_flow_service = current_app.config["user_flow_service"]
        user_flow_service.user_flow(user_obj.id, plan_id,int(plan_time_id))

        return redirect(url_for('register_module_api.show_applications'))

    # ---------- GET ----------
    user_owner_id = request.args.get('user_owner_id')
    plan_id = int(plan_id_raw)

    if plan_id:
        default_role = "BUYER"
        titulo = "Regístrate como Comprador"
    else:
        default_role = "AFILIATE"
        titulo = "Regístrate como Vendedor"

    current_app.logger.info("[REG] Render formulario  plan_id=%s owner=%s",
                            plan_id, user_owner_id)

    return render_template(
        "register/registro_usuario.html",
        plan_time_id  = plan_time_id,
        user_owner_id = user_owner_id,
        default_role  = default_role,
        titulo        = titulo
    )


@register_module_api.route('/login', methods=['GET', 'POST'])
def login():
    application_query_service = current_app.config["application_query_service"]
    apps = application_query_service.list_all()  # Lista de ApplicationData

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_id = request.form.get('app_id')

        # Llamada al login externo
        status, data, cookies = login_emprende_user(username, password)
        if status == 200 and "user" in data:
            datos_user = data["user"]
            session['user_data'] = datos_user
            session['app_id'] = app_id

            user_query_service = current_app.config["user_query_service"]
            try:
                app_id_int = int(app_id)
            except (TypeError, ValueError):
                flash('ID de aplicación inválido.', 'danger')
                return render_template('login/inicio_sesion.html', datos_user=datos_user, apps=apps, app_id=app_id)

            # Buscar usuario (usando account_id y app_id)
            user_obj = user_query_service.find_by_account_and_app(datos_user['id'], app_id_int)

            if not user_obj:
                flash('No existe usuario asociado a esta aplicación para tu cuenta.', 'danger')
                # Limpia la sesión si quieres evitar acceso a otras rutas
                session.pop('user_data', None)
                session.pop('app_id', None)
                return render_template(
                    'login/inicio_sesion.html',
                    apps=apps,
                    app_id=app_id
                )

            # Si existe, continúa como normalmente (redirige o muestra dashboard)
            # Por ejemplo, redirige a dashboard:
            return redirect(url_for('register_module_api.dashboard_index'))

        else:
            flash('Usuario o contraseña inválidos', 'danger')
            return render_template('login/inicio_sesion.html', apps=apps, app_id=app_id)
    # GET normal
    return render_template('login/inicio_sesion.html', apps=apps)


@register_module_api.route('/dashboard')
def dashboard_index():
    # Intenta obtener los datos del usuario autenticado desde session
    user_data = session.get('user_data')
    if not user_data:
        # Si no hay usuario logueado, redirige al login
        return redirect(url_for('register_module_api.login'))
    return render_template('dashboard/index.html', user_data=user_data)



from flask import current_app, session, flash, redirect, url_for, render_template

@register_module_api.route('/dashboard/links')
def generar_links():
    # Log del inicio de la función
    current_app.logger.info('===> Entrando a /dashboard/links')

    user_data = session.get('user_data')
    app_id = session.get('app_id')
    plan_id = session.get('plan_id')

    current_app.logger.debug(f"Datos de sesión: user_data={user_data}, app_id={app_id}, plan_id={plan_id}")

    if not user_data or not app_id:
        current_app.logger.warning("Sesión inválida o falta app_id")
        flash("Sesión inválida. Inicia sesión o selecciona aplicación/plan.", "danger")
        return redirect(url_for('register_module_api.dashboard_index'))

    # INTENTA CONVERTIR app_id A int
    try:
        app_id_int = int(app_id)
        current_app.logger.debug(f"app_id convertido a int: {app_id_int}")
    except (ValueError, TypeError):
        current_app.logger.error(f"ID de aplicación inválido: app_id={app_id}")
        flash("ID de aplicación inválido.", "danger")
        return redirect(url_for('register_module_api.dashboard_index'))

    user_query_service = current_app.config["user_query_service"]

    # Log antes de llamar al servicio
    user_obj = user_query_service.find_by_account_and_app(user_data['id'], app_id_int)

    return render_template(
        'dashboard/generar_links.html',
        user_data=user_data,
        user_obj=user_obj,
        app_id=app_id_int,
        plan_id=plan_id
    )



@register_module_api.route('/logout')
def logout():
    session.clear()  # Limpia toda la sesión (logout total)
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('register_module_api.login'))  # Redirige al login o donde prefieras
