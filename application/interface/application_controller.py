from flask import Blueprint, render_template, redirect, url_for, request, current_app,flash, session

from users.domain.model.entities.user import role_to_user_type
from users.infraestructure.external_users_api.external_emprende_user_api import create_emprede_user, login_emprende_user
from users.infraestructure.external_users_api.external_fullventas_user_api import register_fullventas_user, \
    login_fullventas_user

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
    # ── 1) plan_time_id (puede venir por GET o POST, o no venir) ────────────
    raw_plan_time_id = request.form.get('plan_time_id') or request.args.get('plan_time_id')
    plan_time_id = raw_plan_time_id.strip() if raw_plan_time_id else None          # '' → None

    plan_qs      = current_app.config["plan_query_service"]
    plan_time_qs = current_app.config["plan_time_query_service"]

    if plan_time_id and plan_time_id.isdigit():
        plan_time = plan_time_qs.get_by_id(int(plan_time_id))
        plan_id_raw = plan_time.plan_id if plan_time else None
    else:
        plan_time   = None        # flujo AFILIATE o link mal formado
        plan_id_raw = None

    # ── 2) POST: procesar registro ──────────────────────────────────────────
    if request.method == 'POST':
        nombre   = request.form['nombre']
        dni      = request.form['dni']
        email    = request.form['email']
        celular  = request.form['celular']
        username = request.form['username']
        password = request.form['password']
        role     = request.form['role']              # BUYER | AFILIATE
        id_tipo_usuario = 2
        user_owner_id   = request.form.get('user_owner_id')

        # --- validar / obtener plan & app_id según rol ---------------------
        if role == "BUYER":
            if not plan_id_raw:
                flash("Debes seleccionar un plan para registrarte como comprador.", "danger")
                return redirect(url_for('register_module_api.show_applications'))
            plan_id  = int(plan_id_raw)
            plan_obj = plan_qs.get_by_id(plan_id)
            if not plan_obj:
                flash("El plan indicado no existe.", "danger")
                return redirect(url_for('register_module_api.show_applications'))
            app_id = plan_obj.app_id
        else:  # AFILIATE
            plan_id = None
            # app_id primero del cuerpo y luego de la query
            app_id = (request.form.get('app_id') or request.args.get('app_id', type=int))
            try:
                app_id = int(app_id)
            except (TypeError, ValueError):
                flash("ID de aplicación faltante o inválido.", "danger")
                return redirect(url_for('register_module_api.show_applications'))

        # --- 3) Crear cuenta externa --------------------------------------
        account_id = None
        if app_id == 1:  # EmprendeX
            status, data = create_emprede_user(
                nombre, dni, email, celular, username,
                password, id_tipo_usuario, role
            )
            if status != 201:
                flash(f"Error API EmprendeX: {data.get('error', data)}", "danger")
                return redirect(request.url)
            account_id = data.get("id")

        elif app_id == 2:  # Fullventas
            status, data = register_fullventas_user(
                type_=2,
                first_name=nombre,
                username=username,
                email=email,
                password=password,
                dni=dni,
                mobile=celular
            )
            if status != 200:
                flash(f"Error API Fullventas: {data.get('message') or data.get('error') or data}", "danger")
                return redirect(request.url)
            account_id = data.get("user_id") or data.get("id")

        if not account_id:
            flash("No se pudo obtener el ID del usuario externo.", "danger")
            return redirect(request.url)

        # --- 4) Crear usuario interno -------------------------------------
        user_service = current_app.config["user_command_service"]
        user_type    = role_to_user_type(role)
        try:
            user_obj = user_service.create(
                account_id   = account_id,
                app_id       = app_id,
                user_type    = user_type,
                user_owner_id= int(user_owner_id) if user_owner_id else None
            )
        except Exception as ex:
            current_app.logger.exception("[REG] Error creando usuario interno")
            flash("Error creando usuario interno: " + str(ex), "danger")
            return redirect(request.url)

        # --- 5) Flujo post-registro sólo si hay plan -----------------------
        if plan_time_id and plan_id:
            user_flow_svc = current_app.config["user_flow_service"]
            user_flow_svc.user_flow(user_obj.id, plan_id, int(plan_time_id))

        flash("¡Registro exitoso!", "success")
        return redirect(url_for('register_module_api.show_applications'))

    # ── 3) GET: mostrar formulario ─────────────────────────────────────────
    user_owner_id = request.args.get('user_owner_id')
    app_id_arg    = request.args.get('app_id')
    plan_id       = int(plan_id_raw) if plan_id_raw is not None else None

    default_role = "BUYER" if plan_id else "AFILIATE"
    titulo       = "Regístrate como Comprador" if plan_id else "Regístrate como Vendedor"

    return render_template(
        "register/registro_usuario.html",
        plan_time_id  = plan_time_id,
        user_owner_id = user_owner_id,
        app_id        = app_id_arg,
        default_role  = default_role,
        titulo        = titulo
    )




@register_module_api.route('/login', methods=['GET', 'POST'])
def login():
    application_query_service = current_app.config["application_query_service"]
    apps = application_query_service.list_all()           # para el <select>

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_id   = request.form.get('app_id')             # string (desde <select>)

        # ---------- 1) Validar app_id ----------
        try:
            app_id_int = int(app_id)
        except (TypeError, ValueError):
            flash('ID de aplicación inválido.', 'danger')
            return render_template('login/inicio_sesion.html', apps=apps)

        # ---------- 2) Llamar API externa ----------
        if app_id_int == 1:
            status, data, _cookies = login_emprende_user(username, password)
            success   = status == 200 and "user" in data
            user_data = data.get("user") if success else None

        elif app_id_int == 2:
            status, data = login_fullventas_user(username, password)
            # La API de Fullventas devuelve {"user": {...}} (según tu registro) o algo distinto
            success   = status == 200 and isinstance(data, dict)
            # Ajusta el “path” al objeto usuario según tu API:
            user_data = data.get("user") if "user" in data else data if success else None

        else:
            flash('Aplicación no soportada.', 'danger')
            return render_template('login/inicio_sesion.html', apps=apps, app_id=app_id)

        # ---------- 3) Manejar respuesta ----------
        if not success or not user_data:
            flash('Usuario o contraseña inválidos', 'danger')
            return render_template('login/inicio_sesion.html', apps=apps, app_id=app_id)

        # ---------- 4) Guardar en sesión ----------
        session['user_data'] = user_data
        session['app_id']    = app_id                       # conserva string/int indiferente
        # si tienes plan_time_id o plan_id ponlo aquí cuando corresponda:
        session.pop('plan_time_id', None)
        session.pop('plan_id', None)

        # ---------- 5) Verificar que exista user interno ----------
        user_query_service = current_app.config["user_query_service"]

        # Lee el id correcto, según la app
        if app_id_int == 1:
            # API EmprendeX → usa 'id'
            ext_user_id = user_data.get("id")
        elif app_id_int == 2:
            # API Fullventas → usa 'user_id'
            ext_user_id = user_data.get("user_id")
        else:
            ext_user_id = None

        if not ext_user_id:
            flash('No se pudo identificar el usuario externo.', 'danger')
            session.clear()
            return render_template('login/inicio_sesion.html', apps=apps, app_id=app_id)

        print("userdataid:", ext_user_id, "app_id_int:", app_id_int)
        user_obj = user_query_service.find_by_account_and_app(int(ext_user_id), app_id_int)

        if not user_obj:
            flash('No existe usuario asociado a esta aplicación para tu cuenta.', 'danger')
            session.clear()  # limpia todo
            return render_template('login/inicio_sesion.html', apps=apps, app_id=app_id)

        # ---------- 6) Éxito ----------
        return redirect(url_for('register_module_api.dashboard_index'))

    # ---------- GET ----------
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
    print(user_data)
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
    # --- seleccionar id correcto según la app ---
    if app_id_int == 1:  # EmprendeX
        ext_user_id = user_data.get('id')
    else:  # Fullventas
        ext_user_id = user_data.get('user_id')

    if not ext_user_id:
        flash("No se pudo determinar el usuario externo.", "danger")
        return redirect(url_for('register_module_api.dashboard_index'))

    user_obj = user_query_service.find_by_account_and_app(int(ext_user_id), app_id_int)

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
