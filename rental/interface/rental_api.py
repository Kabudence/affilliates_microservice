from typing import Optional

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

from application.domain.entities.application_data import ApplicationType
from rental.domain.entities.goal import GoalType
from rental.domain.entities.percent_comissions import CommissionType
from rental.domain.entities.plan import PlanType
from users.domain.model.entities.user import User

rental_module_api = Blueprint('rental_module_api', __name__)
# rental/interfaces/http/controllers/goals.py (o donde tengas las rutas)


@rental_module_api.route('/metas')
def metas_index():
    goal_qs = current_app.config["goal_query_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario.", "danger")
        return redirect(url_for('register_module_api.show_applications'))

    info, is_franchise = std  # info es dict, is_franchise bool

    owner_id = info["account_id"] if is_franchise else info["app_id"]
    gtype    = GoalType.FRANCHISE if is_franchise else GoalType.APPLICATION

    goals = goal_qs.list_by_owner_id_and_goal_type(owner_id, gtype)

    # Pasa también info estandarizada si quieres mostrar quién es el owner usado
    return render_template(
        'rental/goals/metas_index.html',
        goals=goals,
        user_data=info,
        is_franchise=is_franchise,
        owner_id=owner_id,
        goal_type=gtype.value
    )


@rental_module_api.route('/metas/create', methods=['GET', 'POST'])
def metas_create():
    goal_command_service = current_app.config["goal_command_service"]

    # 1) Usuario estandarizado (dict info, bool is_franchise)
    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.metas_index'))

    info, is_franchise = std
    # 2) Derivar owner y tipo de meta desde el contexto del usuario
    from rental.domain.entities.goal import GoalType
    owner_id = info["account_id"] if is_franchise else info["app_id"]
    goal_type = GoalType.FRANCHISE if is_franchise else GoalType.APPLICATION

    if request.method == 'POST':
        try:
            number_of_clients   = int(request.form['number_of_clients'])
            month               = int(request.form['month'])
            percentage_to_bonus = float(request.form['percentage_to_bonus'])

            # 3) Crear meta con owner/tipo derivados (no confiamos en el cliente)
            goal_command_service.create(
                number_of_clients=number_of_clients,
                month=month,
                percentage_to_bonus=percentage_to_bonus,
                owner_id=owner_id,
                goal_type=goal_type,
            )
            flash('Meta creada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.metas_index'))
        except Exception as e:
            flash('Error al crear la meta: ' + str(e), 'danger')

    # 4) Render: mostramos owner/tipo como contexto informativo (no editables)
    return render_template(
        'rental/goals/metas_create.html',
        user_data=info,
        is_franchise=is_franchise,
        owner_id=owner_id,
        goal_type=goal_type.value
    )



@rental_module_api.route('/metas/edit/<int:goal_id>', methods=['GET', 'POST'])
def metas_edit(goal_id):
    goal_query_service    = current_app.config["goal_query_service"]
    goal_command_service  = current_app.config["goal_command_service"]

    # 1) Usuario estandarizado
    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.metas_index'))

    info, is_franchise = std
    owner_id_ctx = info["account_id"] if is_franchise else info["app_id"]
    goal_type_ctx = GoalType.FRANCHISE if is_franchise else GoalType.APPLICATION

    # 2) Cargar meta
    goal = goal_query_service.get_by_id(goal_id)
    if not goal:
        flash('Meta no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.metas_index'))

    if request.method == 'POST':
        try:
            number_of_clients   = int(request.form['number_of_clients'])
            month               = int(request.form['month'])
            percentage_to_bonus = float(request.form['percentage_to_bonus'])

            # 3) Actualizar forzando owner/type desde el contexto (no confiamos en el form)
            goal_command_service.update(
                goal_id=goal_id,
                number_of_clients=number_of_clients,
                month=month,
                percentage_to_bonus=percentage_to_bonus,
                owner_id=owner_id_ctx,
                goal_type=goal_type_ctx
            )
            flash('Meta actualizada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.metas_index'))
        except Exception as e:
            flash('Error al actualizar la meta: ' + str(e), 'danger')

    # 4) Render con contexto (solo informativo)
    return render_template(
        'rental/goals/metas_edit.html',
        goal=goal,
        user_data=info,
        is_franchise=is_franchise,
        owner_id=owner_id_ctx,
        goal_type=goal_type_ctx.value
    )


@rental_module_api.route('/metas/delete/<int:goal_id>', methods=['POST'])
def metas_delete(goal_id):
    goal_cs = current_app.config["goal_command_service"]
    try:
        goal_cs.delete(goal_id)
        flash('Meta eliminada exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar la meta: ' + str(e), 'danger')
    return redirect(url_for('rental_module_api.metas_index'))


# ---------- Applications ----------
@rental_module_api.route('/aplicaciones')
def aplicaciones_index():
    application_query_service = current_app.config["application_query_service"]
    aplicaciones = application_query_service.list_all()
    user_data = session.get('user_data')
    return render_template('rental/applications/aplicaciones_index.html', aplicaciones=aplicaciones, user_data=user_data)

@rental_module_api.route('/aplicaciones/create', methods=['GET', 'POST'])
def aplicaciones_create():
    application_command_service = current_app.config["application_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            application_type = ApplicationType(request.form['application_type'])
            application_command_service.create(name, description, application_type)
            flash('Aplicación creada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.aplicaciones_index'))
        except Exception as e:
            flash('Error al crear la aplicación: ' + str(e), 'danger')
    return render_template('rental/applications/aplicaciones_create.html', user_data=user_data)

@rental_module_api.route('/aplicaciones/edit/<int:application_id>', methods=['GET', 'POST'])
def aplicaciones_edit(application_id):
    application_query_service = current_app.config["application_query_service"]
    application_command_service = current_app.config["application_command_service"]
    user_data = session.get('user_data')
    app = application_query_service.get_by_id(application_id)
    if not app:
        flash('Aplicación no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.aplicaciones_index'))
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            application_type = ApplicationType(request.form['application_type'])
            application_command_service.update(application_id, name, description, application_type)
            flash('Aplicación actualizada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.aplicaciones_index'))
        except Exception as e:
            flash('Error al actualizar la aplicación: ' + str(e), 'danger')
    return render_template('rental/applications/aplicaciones_edit.html', app=app, user_data=user_data)

@rental_module_api.route('/aplicaciones/delete/<int:application_id>', methods=['POST'])
def aplicaciones_delete(application_id):
    application_command_service = current_app.config["application_command_service"]
    try:
        application_command_service.delete(application_id)
        flash('Aplicación eliminada exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar la aplicación: ' + str(e), 'danger')
    return redirect(url_for('rental_module_api.aplicaciones_index'))


# ----------- Inscription -----------
@rental_module_api.route('/niveles-inscripcion')
def inscription_levels_index():
    inscription_level_query_service = current_app.config["inscription_level_query_service"]
    levels = inscription_level_query_service.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/inscription_levels/index.html',
        levels=levels, user_data=user_data
    )

@rental_module_api.route('/niveles-inscripcion/create', methods=['GET', 'POST'])
def inscription_levels_create():
    inscription_level_command_service = current_app.config["inscription_level_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            name_level = request.form['name_level']
            registration_cost = float(request.form['registration_cost'])
            inscription_level_command_service.create(name_level, registration_cost)
            flash('Nivel de inscripción creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.inscription_levels_index'))
        except Exception as e:
            flash(f'Error al crear el nivel: {e}', 'danger')
    return render_template('rental/inscription_levels/create.html', user_data=user_data)

@rental_module_api.route('/niveles-inscripcion/edit/<int:level_id>', methods=['GET', 'POST'])
def inscription_levels_edit(level_id):
    inscription_level_query_service = current_app.config["inscription_level_query_service"]
    inscription_level_command_service = current_app.config["inscription_level_command_service"]
    user_data = session.get('user_data')
    level = inscription_level_query_service.get_by_id(level_id)
    if not level:
        flash('Nivel de inscripción no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.inscription_levels_index'))
    if request.method == 'POST':
        try:
            name_level = request.form['name_level']
            registration_cost = float(request.form['registration_cost'])
            inscription_level_command_service.update(level_id, name_level, registration_cost)
            flash('Nivel de inscripción actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.inscription_levels_index'))
        except Exception as e:
            flash(f'Error al actualizar el nivel: {e}', 'danger')
    return render_template('rental/inscription_levels/edit.html', level=level, user_data=user_data)

@rental_module_api.route('/niveles-inscripcion/delete/<int:level_id>', methods=['POST'])
def inscription_levels_delete(level_id):
    inscription_level_command_service = current_app.config["inscription_level_command_service"]
    try:
        inscription_level_command_service.delete(level_id)
        flash('Nivel de inscripción eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el nivel: {e}', 'danger')
    return redirect(url_for('rental_module_api.inscription_levels_index'))

# ----------- Listar Royalties -----------
@rental_module_api.route('/royalties')
def royalties_index():
    royalties_query_service = current_app.config["royalties_query_service"]
    inscription_level_query_service = current_app.config["inscription_level_query_service"]
    royalties = royalties_query_service.list_all()
    # (opcional: para mostrar nombre del nivel en tabla)
    levels = {lvl.id: lvl for lvl in inscription_level_query_service.list_all()}
    user_data = session.get('user_data')
    return render_template(
        'rental/royalties/index.html',
        royalties=royalties, levels=levels, user_data=user_data
    )

# ----------- Crear Royalty -----------
@rental_module_api.route('/royalties/create', methods=['GET', 'POST'])
def royalties_create():
    royalties_command_service = current_app.config["royalties_command_service"]
    inscription_level_query_service = current_app.config["inscription_level_query_service"]
    user_data = session.get('user_data')
    levels = inscription_level_query_service.list_all()
    if request.method == 'POST':
        try:
            inscription_level_id = int(request.form['inscription_level_id'])
            cost = float(request.form['cost'])
            royalties_command_service.create(inscription_level_id, cost)
            flash('Royalty creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.royalties_index'))
        except Exception as e:
            flash(f'Error al crear el royalty: {e}', 'danger')
    return render_template('rental/royalties/create.html', levels=levels, user_data=user_data)

# ----------- Editar Royalty -----------
@rental_module_api.route('/royalties/edit/<int:royalty_id>', methods=['GET', 'POST'])
def royalties_edit(royalty_id):
    royalties_query_service = current_app.config["royalties_query_service"]
    royalties_command_service = current_app.config["royalties_command_service"]
    inscription_level_query_service = current_app.config["inscription_level_query_service"]
    user_data = session.get('user_data')
    royalty = royalties_query_service.get_by_id(royalty_id)
    levels = inscription_level_query_service.list_all()
    if not royalty:
        flash('Royalty no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.royalties_index'))
    if request.method == 'POST':
        try:
            inscription_level_id = int(request.form['inscription_level_id'])
            cost = float(request.form['cost'])
            royalties_command_service.update(royalty_id, inscription_level_id, cost)
            flash('Royalty actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.royalties_index'))
        except Exception as e:
            flash(f'Error al actualizar el royalty: {e}', 'danger')
    return render_template(
        'rental/royalties/edit.html',
        royalty=royalty, levels=levels, user_data=user_data
    )

# ----------- Eliminar Royalty -----------
@rental_module_api.route('/royalties/delete/<int:royalty_id>', methods=['POST'])
def royalties_delete(royalty_id):
    royalties_command_service = current_app.config["royalties_command_service"]
    try:
        royalties_command_service.delete(royalty_id)
        flash('Royalty eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el royalty: {e}', 'danger')
    return redirect(url_for('rental_module_api.royalties_index'))


@rental_module_api.route('/modulos')
def modules_index():
    module_query_service = current_app.config["module_query_service"]
    modules = module_query_service.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/modules/index.html',
        modules=modules, user_data=user_data
    )

# ----------- Crear módulo -----------
@rental_module_api.route('/modulos/create', methods=['GET', 'POST'])
def modules_create():
    module_command_service = current_app.config["module_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            module_command_service.create(name, description)
            flash('Módulo creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.modules_index'))
        except Exception as e:
            flash(f'Error al crear el módulo: {e}', 'danger')
    return render_template('rental/modules/create.html', user_data=user_data)

# ----------- Editar módulo -----------
@rental_module_api.route('/modulos/edit/<int:module_id>', methods=['GET', 'POST'])
def modules_edit(module_id):
    module_query_service = current_app.config["module_query_service"]
    module_command_service = current_app.config["module_command_service"]
    user_data = session.get('user_data')
    module = module_query_service.get_by_id(module_id)
    if not module:
        flash('Módulo no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.modules_index'))
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            module_command_service.update(module_id, name, description)
            flash('Módulo actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.modules_index'))
        except Exception as e:
            flash(f'Error al actualizar el módulo: {e}', 'danger')
    return render_template(
        'rental/modules/edit.html',
        module=module, user_data=user_data
    )

# ----------- Eliminar módulo -----------
@rental_module_api.route('/modulos/delete/<int:module_id>', methods=['POST'])
def modules_delete(module_id):
    module_command_service = current_app.config["module_command_service"]
    try:
        module_command_service.delete(module_id)
        flash('Módulo eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el módulo: {e}', 'danger')
    return redirect(url_for('rental_module_api.modules_index'))


@rental_module_api.route('/comisiones-actuales')
def comisiones_usuario():
    user_data = session.get('user_data')
    if not user_data:
        flash("Debes iniciar sesión para ver tus comisiones.", "danger")
        return redirect(url_for('register_module_api.login'))
    commission_query_service = current_app.config["commission_query_service"]
    commissions = commission_query_service.list_by_user_id(user_data['id'])
    return render_template(
        'rental/commissions/index.html',
        commissions=commissions,
        user_data=user_data
    )

# ---------- LISTAR PLANES ----------
@rental_module_api.route('/planes')
def planes_index():
    plan_qs      = current_app.config["plan_query_service"]
    plan_time_qs = current_app.config["plan_time_query_service"]
    module_qs    = current_app.config["module_query_service"]

    app_id   = session.get('app_id')
    user     = session.get('user_data')
    if not app_id:
        flash("No hay aplicación seleccionada.", "danger")
        return redirect(url_for('dashboard_index'))

    plans = plan_qs.list_by_app_id(app_id)

    # ✓ horarios y módulos por plan con los métodos nuevos
    plan_times_by_plan = {
        p.id: plan_time_qs.list_by_plan_id(p.id) for p in plans
    }
    modules_by_plan = {
        p.id: module_qs.get_all_by_plan_id(p.id) for p in plans
    }

    return render_template(
        'rental/plans/index.html',
        plans=plans,
        plan_times_by_plan=plan_times_by_plan,
        modules_by_plan=modules_by_plan,
        user_data=user
    )

@rental_module_api.route('/planes/create', methods=['GET', 'POST'])
def planes_create():
    plan_command_service = current_app.config["plan_command_service"]
    module_query_service = current_app.config["module_query_service"]
    app_id = session.get('app_id')
    user_data = session.get('user_data')
    modules = module_query_service.list_all()
    from rental.domain.entities.plan import PlanType

    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            plan_type = request.form['plan_type']
            selected_modules = request.form.getlist('modules')
            ids_modules = [int(mid) for mid in selected_modules]

            # LOGS para depuración
            print('----[DEBUG POST /planes/create]----')
            print('name:', name)
            print('description:', description)
            print('plan_type:', plan_type)
            print('ids_modules:', ids_modules)
            print('app_id:', app_id)
            print('user_data:', user_data)

            # Llama a create SIN times (solo los datos requeridos)
            plan = plan_command_service.create(
                name=name,
                description=description,
                app_id=app_id,
                plan_type=PlanType(plan_type),
                ids_modules=ids_modules
            )
            flash("Plan creado. Ahora agrega los precios/duraciones.", "success")
            return redirect(url_for('rental_module_api.planes_add_times', plan_id=plan.id))
        except Exception as e:
            print('[ERROR EN CREAR PLAN]:', e)  # log de error
            flash("Error creando plan: " + str(e), "danger")
    return render_template(
        'rental/plans/create.html',
        modules=modules,
        user_data=user_data
    )


@rental_module_api.route('/planes/<int:plan_id>/add-times', methods=['GET', 'POST'])
def planes_add_times(plan_id):
    plan_time_command_service = current_app.config["plan_time_command_service"]
    plan_query_service = current_app.config["plan_query_service"]
    plan_time_query_service = current_app.config["plan_time_query_service"]
    user_data = session.get('user_data')

    plan = plan_query_service.get_by_id(plan_id)
    if not plan:
        flash("Plan no encontrado.", "danger")
        return redirect(url_for('rental_module_api.planes_index'))

    if request.method == 'POST':
        try:
            durations = request.form.getlist('duration')
            prices = request.form.getlist('price')
            for dur, price in zip(durations, prices):
                if dur and price:
                    plan_time_command_service.create(plan_id, int(dur), float(price))
            flash("Horarios agregados correctamente.", "success")
            return redirect(url_for('rental_module_api.planes_index'))
        except Exception as e:
            flash("Error agregando horarios: " + str(e), "danger")
    # Mostrar horarios existentes para editar/eliminar (opcional)
    plan_times = plan_time_query_service.list_by_plan_id(plan_id)
    return render_template(
        'rental/plans/add_times.html',
        plan=plan,
        plan_times=plan_times,
        user_data=user_data
    )


# ---------- Editar / eliminar Plan ----------
@rental_module_api.route('/planes/edit/<int:plan_id>', methods=['GET', 'POST'])
def planes_edit(plan_id):
    plan_query_service  = current_app.config["plan_query_service"]
    plan_command_service= current_app.config["plan_command_service"]
    module_query_service= current_app.config["module_query_service"]
    user_data = session.get('user_data')
    plan   = plan_query_service.get_by_id(plan_id)
    if not plan:
        flash('Plan no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.planes_index'))

    modules      = module_query_service.list_all()
    current_mods = {pm.id for pm in plan_command_service.plan_module_repo.get_modules_ids_by_plan(plan_id)}

    if request.method == 'POST':
        try:
            name  = request.form['name']
            desc  = request.form['description']
            ptype = request.form['plan_type']
            mods  = [int(mid) for mid in request.form.getlist('modules')]
            plan_command_service.update(
                plan_id, name, desc, plan.app_id,
                PlanType(ptype), ids_modules=mods
            )
            flash('Plan actualizado.', 'success')
            return redirect(url_for('rental_module_api.planes_index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template(
        'rental/plans/edit.html',
        plan=plan, modules=modules,
        current_mods=current_mods, user_data=user_data
    )

@rental_module_api.route('/planes/delete/<int:plan_id>', methods=['POST'])
def planes_delete(plan_id):
    plan_command_service = current_app.config["plan_command_service"]
    try:
        plan_command_service.delete(plan_id)
        flash('Plan eliminado.', 'success')
    except Exception as e:
        flash(f'Error eliminando plan: {e}', 'danger')
    return redirect(url_for('rental_module_api.planes_index'))

# ---------- Eliminar horario ----------
@rental_module_api.route('/plans/<int:plan_id>/times/delete/<int:time_id>', methods=['POST'])
def plan_time_delete(plan_id, time_id):
    plan_time_command_service = current_app.config["plan_time_command_service"]
    try:
        plan_time_command_service.delete(time_id)
        flash('Horario eliminado.', 'success')
    except Exception as e:
        flash(f'Error eliminando horario: {e}', 'danger')
    return redirect(url_for('rental_module_api.planes_add_times', plan_id=plan_id))



#FRANCHISE_CONFIG
# FRANCHISE_CONFIG

@rental_module_api.route('/franchise-config')
def franchise_config_index():
    franchise_config_qs = current_app.config["franchise_config_query_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('register_module_api.show_applications'))

    info, _is_franchise = std
    account_id = info.get("account_id")

    # Solo listamos la config del owner autenticado
    cfg = franchise_config_qs.get_by_franchise_owner_id(account_id)
    configs = [cfg] if cfg else []

    return render_template(
        'rental/franchise_config/index.html',
        configs=configs,
        user_data=info,             # pásalo estandarizado
        owner_id=account_id
    )


# ---------- CREATE ----------
@rental_module_api.route('/franchise-config/create', methods=['GET', 'POST'])
def franchise_config_create():
    franchise_config_cs = current_app.config["franchise_config_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_config_index'))

    info, _is_franchise = std
    account_id = info.get("account_id")

    if request.method == 'POST':
        try:
            # Checkbox: presente -> True
            activate_commissions = request.form.get('activate_commissions') is not None
            franchise_config_cs.create(account_id, activate_commissions)
            flash('Configuración creada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_config_index'))
        except Exception as e:
            flash(f'Error al crear la configuración: {e}', 'danger')

    return render_template(
        'rental/franchise_config/create.html',
        user_data=info,
        owner_id=account_id
    )


# ---------- EDIT ----------
@rental_module_api.route('/franchise-config/edit/<int:config_id>', methods=['GET', 'POST'])
def franchise_config_edit(config_id):
    franchise_config_qs = current_app.config["franchise_config_query_service"]
    franchise_config_cs = current_app.config["franchise_config_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_config_index'))

    info, _is_franchise = std
    account_id = info.get("account_id")

    config = franchise_config_qs.get_by_id(config_id)
    if not config:
        flash('Configuración no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.franchise_config_index'))

    # (Opcional) Asegura ownership
    if config.franchise_owner_id != account_id:
        flash('No tienes permisos para editar esta configuración.', 'danger')
        return redirect(url_for('rental_module_api.franchise_config_index'))

    if request.method == 'POST':
        try:
            activate_commissions = request.form.get('activate_commissions') is not None
            # Forzamos owner con el autenticado
            franchise_config_cs.update(config_id, account_id, activate_commissions)
            flash('Configuración actualizada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_config_index'))
        except Exception as e:
            flash(f'Error al actualizar la configuración: {e}', 'danger')

    return render_template(
        'rental/franchise_config/edit.html',
        config=config,
        user_data=info,
        owner_id=account_id
    )


# ---------- DELETE ----------
@rental_module_api.route('/franchise-config/delete/<int:config_id>', methods=['POST'])
def franchise_config_delete(config_id):
    franchise_config_qs = current_app.config["franchise_config_query_service"]
    franchise_config_cs = current_app.config["franchise_config_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_config_index'))

    info, _is_franchise = std
    account_id = info.get("account_id")

    config = franchise_config_qs.get_by_id(config_id)
    if not config:
        flash('Configuración no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.franchise_config_index'))

    # (Opcional) Asegura ownership
    if config.franchise_owner_id != account_id:
        flash('No tienes permisos para eliminar esta configuración.', 'danger')
        return redirect(url_for('rental_module_api.franchise_config_index'))

    try:
        franchise_config_cs.delete(config_id)
        flash('Configuración eliminada.', 'success')
    except Exception as e:
        flash(f'Error eliminando configuración: {e}', 'danger')

    return redirect(url_for('rental_module_api.franchise_config_index'))


#FRANCHISE DISCOUT
@rental_module_api.route('/franchise-discount')
def franchise_discount_index():
    discount_qs = current_app.config["franchise_discount_query_service"]
    discounts = discount_qs.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/franchise_discount/index.html',
        discounts=discounts, user_data=user_data
    )

@rental_module_api.route('/franchise-discount/create', methods=['GET', 'POST'])
def franchise_discount_create():
    discount_cs = current_app.config["franchise_discount_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            percent = float(request.form['percent'])
            app_id = int(request.form['app_id'])
            discount_cs.create(percent, app_id)
            flash('Descuento creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_discount_index'))
        except Exception as e:
            flash(f'Error al crear el descuento: {e}', 'danger')
    return render_template('rental/franchise_discount/create.html', user_data=user_data)

@rental_module_api.route('/franchise-discount/edit/<int:discount_id>', methods=['GET', 'POST'])
def franchise_discount_edit(discount_id):
    discount_qs = current_app.config["franchise_discount_query_service"]
    discount_cs = current_app.config["franchise_discount_command_service"]
    user_data = session.get('user_data')
    discount = discount_qs.get_by_id(discount_id)
    if not discount:
        flash('Descuento no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.franchise_discount_index'))
    if request.method == 'POST':
        try:
            percent = float(request.form['percent'])
            app_id = int(request.form['app_id'])
            discount_cs.update(discount_id, percent, app_id)
            flash('Descuento actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_discount_index'))
        except Exception as e:
            flash(f'Error al actualizar el descuento: {e}', 'danger')
    return render_template(
        'rental/franchise_discount/edit.html',
        discount=discount, user_data=user_data
    )

@rental_module_api.route('/franchise-discount/delete/<int:discount_id>', methods=['POST'])
def franchise_discount_delete(discount_id):
    discount_cs = current_app.config["franchise_discount_command_service"]
    try:
        discount_cs.delete(discount_id)
        flash('Descuento eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el descuento: {e}', 'danger')
    return redirect(url_for('rental_module_api.franchise_discount_index'))






@rental_module_api.route('/percent-commissions')
def percent_commission_index():
    pc_qs = current_app.config["percent_commission_query_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('register_module_api.show_applications'))

    info, is_franchise = std
    owner_id = info["account_id"] if is_franchise else info["app_id"]
    ctype    = CommissionType.FRANCHISE if is_franchise else CommissionType.APPLICATION

    # único % relevante al contexto actual
    pc = pc_qs.get_by_owner_and_type(owner_id, ctype)
    percent_commissions = [pc] if pc else []

    return render_template(
        'rental/percent_commission/index.html',
        percent_commissions=percent_commissions,
        user_data=info,
        owner_id=owner_id,
        commission_type=ctype.value,
        is_franchise=is_franchise
    )


@rental_module_api.route('/percent-commissions/create', methods=['GET', 'POST'])
def percent_commission_create():
    pc_cs = current_app.config["percent_commission_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.percent_commission_index'))

    info, is_franchise = std
    owner_id = info["account_id"] if is_franchise else info["app_id"]
    ctype    = CommissionType.FRANCHISE if is_franchise else CommissionType.APPLICATION

    if request.method == 'POST':
        try:
            percent = float(request.form['percent'])
            # Forzamos owner y tipo desde contexto
            pc_cs.create(owner_id, percent, ctype)
            flash('Porcentaje creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.percent_commission_index'))
        except Exception as e:
            flash(f'Error al crear el porcentaje: {e}', 'danger')

    return render_template(
        'rental/percent_commission/create.html',
        user_data=info,
        owner_id=owner_id,
        commission_type=ctype.value
    )


@rental_module_api.route('/percent-commissions/edit/<int:percent_commission_id>', methods=['GET', 'POST'])
def percent_commission_edit(percent_commission_id):
    pc_qs = current_app.config["percent_commission_query_service"]
    pc_cs = current_app.config["percent_commission_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.percent_commission_index'))

    info, is_franchise = std
    owner_id_ctx = info["account_id"] if is_franchise else info["app_id"]
    ctype_ctx    = CommissionType.FRANCHISE if is_franchise else CommissionType.APPLICATION

    percent_commission = pc_qs.get_by_id(percent_commission_id)
    if not percent_commission:
        flash('Porcentaje no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.percent_commission_index'))

    # (Opcional) Valida ownership por contexto
    if percent_commission.owner_id != owner_id_ctx or percent_commission.commission_type != ctype_ctx:
        flash('No tienes permisos para editar este porcentaje en este contexto.', 'danger')
        return redirect(url_for('rental_module_api.percent_commission_index'))

    if request.method == 'POST':
        try:
            percent = float(request.form['percent'])
            # Forzamos owner y tipo desde contexto (no confiamos en el form)
            pc_cs.update(percent_commission_id, owner_id_ctx, percent, ctype_ctx)
            flash('Porcentaje actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.percent_commission_index'))
        except Exception as e:
            flash(f'Error al actualizar el porcentaje: {e}', 'danger')

    return render_template(
        'rental/percent_commission/edit.html',
        percent_commission=percent_commission,
        user_data=info,
        owner_id=owner_id_ctx,
        commission_type=ctype_ctx.value
    )


@rental_module_api.route('/percent-commissions/delete/<int:percent_commission_id>', methods=['POST'])
def percent_commission_delete(percent_commission_id):
    pc_qs = current_app.config["percent_commission_query_service"]
    pc_cs = current_app.config["percent_commission_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.percent_commission_index'))

    info, is_franchise = std
    owner_id_ctx = info["account_id"] if is_franchise else info["app_id"]
    ctype_ctx    = CommissionType.FRANCHISE if is_franchise else CommissionType.APPLICATION

    percent_commission = pc_qs.get_by_id(percent_commission_id)
    if not percent_commission:
        flash('Porcentaje no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.percent_commission_index'))

    # (Opcional) Valida ownership por contexto
    if percent_commission.owner_id != owner_id_ctx or percent_commission.commission_type != ctype_ctx:
        flash('No tienes permisos para eliminar este porcentaje en este contexto.', 'danger')
        return redirect(url_for('rental_module_api.percent_commission_index'))

    try:
        pc_cs.delete(percent_commission_id)
        flash('Porcentaje eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el porcentaje: {e}', 'danger')

    return redirect(url_for('rental_module_api.percent_commission_index'))


@rental_module_api.route('/franchise-overpriced')
def franchise_overpriced_index():
    fo_qs = current_app.config["franchise_overpriced_query_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('register_module_api.show_applications'))

    info, is_franchise = std
    if not is_franchise:
        # Si no es franquiciado, no tiene sentido el módulo
        flash("Este módulo es solo para franquiciados.", "warning")
        return render_template(
            'rental/franchise_overpriced/index.html',
            overpriced=[],
            user_data=info,
            owner_id=None,
            is_franchise=is_franchise
        )

    franchise_id = info["account_id"]
    overpriced = fo_qs.list_by_franchise_id(franchise_id)

    return render_template(
        'rental/franchise_overpriced/index.html',
        overpriced=overpriced,
        user_data=info,
        owner_id=franchise_id,
        is_franchise=is_franchise
    )


@rental_module_api.route('/franchise-overpriced/create', methods=['GET', 'POST'])
def franchise_overpriced_create():
    fo_cs = current_app.config["franchise_overpriced_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    info, is_franchise = std
    if not is_franchise:
        flash("Solo un franquiciado puede crear sobreprecios.", "warning")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    franchise_id = info["account_id"]

    if request.method == 'POST':
        try:
            extra_price = float(request.form['extra_price'])
            plan_id_raw = request.form.get('plan_id') or None
            plan_id = int(plan_id_raw) if plan_id_raw else None

            # Forzamos franchise_id desde el contexto
            fo_cs.create(extra_price, franchise_id, plan_id)
            flash('Sobreprecio creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_overpriced_index'))
        except Exception as e:
            flash(f'Error al crear el sobreprecio: {e}', 'danger')

    return render_template(
        'rental/franchise_overpriced/create.html',
        user_data=info,
        owner_id=franchise_id
    )


@rental_module_api.route('/franchise-overpriced/edit/<int:overpriced_id>', methods=['GET', 'POST'])
def franchise_overpriced_edit(overpriced_id):
    fo_qs = current_app.config["franchise_overpriced_query_service"]
    fo_cs = current_app.config["franchise_overpriced_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    info, is_franchise = std
    if not is_franchise:
        flash("Solo un franquiciado puede editar sobreprecios.", "warning")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    franchise_id_ctx = info["account_id"]

    overpriced = fo_qs.get_by_id(overpriced_id)
    if not overpriced:
        flash('Sobreprecio no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    # Enforce ownership
    if overpriced.franchise_id != franchise_id_ctx:
        flash('No tienes permisos para editar este sobreprecio.', 'danger')
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    if request.method == 'POST':
        try:
            extra_price = float(request.form['extra_price'])
            plan_id_raw = request.form.get('plan_id') or None
            plan_id = int(plan_id_raw) if plan_id_raw else None

            # Forzamos franchise_id del contexto
            fo_cs.update(overpriced_id, extra_price, franchise_id_ctx, plan_id)
            flash('Sobreprecio actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_overpriced_index'))
        except Exception as e:
            flash(f'Error al actualizar el sobreprecio: {e}', 'danger')

    return render_template(
        'rental/franchise_overpriced/edit.html',
        overpriced=overpriced,
        user_data=info,
        owner_id=franchise_id_ctx
    )


@rental_module_api.route('/franchise-overpriced/delete/<int:overpriced_id>', methods=['POST'])
def franchise_overpriced_delete(overpriced_id):
    fo_qs = current_app.config["franchise_overpriced_query_service"]
    fo_cs = current_app.config["franchise_overpriced_command_service"]

    std = get_user_data_standardized()
    if not std or not isinstance(std, tuple) or not std[0]:
        flash("No se pudo determinar el usuario autenticado.", "danger")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    info, is_franchise = std
    if not is_franchise:
        flash("Solo un franquiciado puede eliminar sobreprecios.", "warning")
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    franchise_id_ctx = info["account_id"]

    overpriced = fo_qs.get_by_id(overpriced_id)
    if not overpriced:
        flash('Sobreprecio no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    # Enforce ownership
    if overpriced.franchise_id != franchise_id_ctx:
        flash('No tienes permisos para eliminar este sobreprecio.', 'danger')
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))

    try:
        fo_cs.delete(overpriced_id)
        flash('Sobreprecio eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el sobreprecio: {e}', 'danger')
    return redirect(url_for('rental_module_api.franchise_overpriced_index'))



def get_user_data_standardized():
    """
    Devuelve:
    (
        {
            "id": int,
            "role": str | None,
            "type": str | None,
            "username": str,
            "account_id": int,
            "user_owner_id": int | None,
            "app_id": int
        },
        bool  # this_user_is_franchise
    )
    """

    user_data = session.get('user_data')
    app_id_raw = session.get('app_id')

    if not user_data:
        return None, False

    # --- Normalizar ID, role, type y username según formato recibido ---
    if isinstance(user_data, dict):
        if "role" in user_data:  # Plataforma tipo 1
            user_id = user_data.get("id")
            role = user_data.get("role")
            type_ = None
            username = user_data.get("username")
        elif "user_id" in user_data:  # Plataforma tipo 2
            user_id = int(user_data.get("user_id"))
            role = None
            type_ = user_data.get("type")
            username = user_data.get("username")
        else:
            return None, False
    else:
        return None, False

    # --- Convertir app_id ---
    try:
        app_id = int(app_id_raw) if app_id_raw else None
    except (ValueError, TypeError):
        return None, False

    if not user_id or not app_id:
        return None, False

    # --- Obtener usuario interno ---
    user_query_service = current_app.config["user_query_service"]
    user_cross = user_query_service.find_by_account_and_app(user_id, app_id)
    if not user_cross:
        return None, False

    # --- Armar primer objeto ---
    result_info = {
        "id": user_id,
        "role": role,
        "type": type_,
        "username": username,
        "account_id": user_cross.id,
        "user_owner_id": user_cross.user_owner_id,
        "app_id": user_cross.app_id
    }
    print( result_info )

    # --- Determinar si ESTE usuario es franquicia ---
    plan_qs = current_app.config["plan_query_service"]
    subscription_qs = current_app.config["subscription_query_service"]

    subscription = subscription_qs.get_subscription_by_user_id(user_cross.id)
    if subscription:
        plan = plan_qs.get_by_id(subscription.plan_id)
        this_user_is_franchise = (
            plan is not None and plan.plan_type.name == "FRANQUICIA_EXCLUSIVA"
        )
    else:
        this_user_is_franchise = False

    return result_info, this_user_is_franchise


