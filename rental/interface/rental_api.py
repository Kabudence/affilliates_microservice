from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

from application.domain.entities.application_data import ApplicationType
from rental.domain.entities.plan import PlanType

rental_module_api = Blueprint('rental_module_api', __name__)

@rental_module_api.route('/metas')
def metas_index():
    goal_query_service = current_app.config["goal_query_service"]
    goals = goal_query_service.list_all()
    user_data = session.get('user_data')
    return render_template('rental/goals/metas_index.html', goals=goals, user_data=user_data)

@rental_module_api.route('/metas/create', methods=['GET', 'POST'])
def metas_create():
    goal_command_service = current_app.config["goal_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            number_of_clients = int(request.form['number_of_clients'])
            month = int(request.form['month'])
            percentage_to_bonus = float(request.form['percentage_to_bonus'])
            goal_command_service.create(number_of_clients, month, percentage_to_bonus)
            flash('Meta creada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.metas_index'))
        except Exception as e:
            flash('Error al crear la meta: ' + str(e), 'danger')
    return render_template('rental/goals/metas_create.html', user_data=user_data)

@rental_module_api.route('/metas/edit/<int:goal_id>', methods=['GET', 'POST'])
def metas_edit(goal_id):
    goal_query_service = current_app.config["goal_query_service"]
    goal_command_service = current_app.config["goal_command_service"]
    user_data = session.get('user_data')
    goal = goal_query_service.get_by_id(goal_id)
    if not goal:
        flash('Meta no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.metas_index'))
    if request.method == 'POST':
        try:
            number_of_clients = int(request.form['number_of_clients'])
            month = int(request.form['month'])
            percentage_to_bonus = float(request.form['percentage_to_bonus'])
            goal_command_service.update(goal_id, number_of_clients, month, percentage_to_bonus)
            flash('Meta actualizada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.metas_index'))
        except Exception as e:
            flash('Error al actualizar la meta: ' + str(e), 'danger')
    return render_template('rental/goals/metas_edit.html', goal=goal, user_data=user_data)

@rental_module_api.route('/metas/delete/<int:goal_id>', methods=['POST'])
def metas_delete(goal_id):
    goal_command_service = current_app.config["goal_command_service"]
    try:
        goal_command_service.delete(goal_id)
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

@rental_module_api.route('/franchise-config')
def franchise_config_index():
    franchise_config_qs = current_app.config["franchise_config_query_service"]
    configs = franchise_config_qs.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/franchise_config/index.html',
        configs=configs,
        user_data=user_data
    )


# ---------- CREATE ----------
@rental_module_api.route('/franchise-config/create', methods=['GET', 'POST'])
def franchise_config_create():
    franchise_config_cs = current_app.config["franchise_config_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            franchise_owner_id = int(request.form['franchise_owner_id'])
            activate_commissions = bool(request.form.get('activate_commissions'))
            franchise_config_cs.create(franchise_owner_id, activate_commissions)
            flash('Configuración creada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_config_index'))
        except Exception as e:
            flash(f'Error al crear la configuración: {e}', 'danger')
    return render_template('rental/franchise_config/create.html', user_data=user_data)


# ---------- EDIT ----------
@rental_module_api.route('/franchise-config/edit/<int:config_id>', methods=['GET', 'POST'])
def franchise_config_edit(config_id):
    franchise_config_qs = current_app.config["franchise_config_query_service"]
    franchise_config_cs = current_app.config["franchise_config_command_service"]
    user_data = session.get('user_data')
    config = franchise_config_qs.get_by_id(config_id)
    if not config:
        flash('Configuración no encontrada.', 'danger')
        return redirect(url_for('rental_module_api.franchise_config_index'))
    if request.method == 'POST':
        try:
            franchise_owner_id = int(request.form['franchise_owner_id'])
            activate_commissions = bool(request.form.get('activate_commissions'))
            franchise_config_cs.update(config_id, franchise_owner_id, activate_commissions)
            flash('Configuración actualizada exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_config_index'))
        except Exception as e:
            flash(f'Error al actualizar la configuración: {e}', 'danger')
    return render_template(
        'rental/franchise_config/edit.html',
        config=config,
        user_data=user_data
    )


# ---------- DELETE ----------
@rental_module_api.route('/franchise-config/delete/<int:config_id>', methods=['POST'])
def franchise_config_delete(config_id):
    franchise_config_cs = current_app.config["franchise_config_command_service"]
    try:
        franchise_config_cs.delete(config_id)
        flash('Configuración eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la configuración: {e}', 'danger')
    return redirect(url_for('rental_module_api.franchise_config_index'))



#---------------------FRANCHISE DISCOUT---------------------
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
    percent_commissions = pc_qs.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/percent_commission/index.html',
        percent_commissions=percent_commissions,
        user_data=user_data
    )

@rental_module_api.route('/percent-commissions/create', methods=['GET', 'POST'])
def percent_commission_create():
    pc_cs = current_app.config["percent_commission_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            owner_id = int(request.form['owner_id'])
            percent = float(request.form['percent'])
            commission_type = request.form['commission_type']
            pc_cs.create(owner_id, percent, commission_type)
            flash('Porcentaje creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.percent_commission_index'))
        except Exception as e:
            flash(f'Error al crear el porcentaje: {e}', 'danger')
    return render_template('rental/percent_commission/create.html', user_data=user_data)

@rental_module_api.route('/percent-commissions/edit/<int:percent_commission_id>', methods=['GET', 'POST'])
def percent_commission_edit(percent_commission_id):
    pc_qs = current_app.config["percent_commission_query_service"]
    pc_cs = current_app.config["percent_commission_command_service"]
    user_data = session.get('user_data')
    percent_commission = pc_qs.get_by_id(percent_commission_id)
    if not percent_commission:
        flash('Porcentaje no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.percent_commission_index'))
    if request.method == 'POST':
        try:
            owner_id = int(request.form['owner_id'])
            percent = float(request.form['percent'])
            commission_type = request.form['commission_type']
            pc_cs.update(percent_commission_id, owner_id, percent, commission_type)
            flash('Porcentaje actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.percent_commission_index'))
        except Exception as e:
            flash(f'Error al actualizar el porcentaje: {e}', 'danger')
    return render_template(
        'rental/percent_commission/edit.html',
        percent_commission=percent_commission,
        user_data=user_data
    )

@rental_module_api.route('/percent-commissions/delete/<int:percent_commission_id>', methods=['POST'])
def percent_commission_delete(percent_commission_id):
    pc_cs = current_app.config["percent_commission_command_service"]
    try:
        pc_cs.delete(percent_commission_id)
        flash('Porcentaje eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el porcentaje: {e}', 'danger')
    return redirect(url_for('rental_module_api.percent_commission_index'))


@rental_module_api.route('/franchise-overpriced')
def franchise_overpriced_index():
    fo_qs = current_app.config["franchise_overpriced_query_service"]
    overpriced = fo_qs.list_all()
    user_data = session.get('user_data')
    return render_template(
        'rental/franchise_overpriced/index.html',
        overpriced=overpriced,
        user_data=user_data
    )

@rental_module_api.route('/franchise-overpriced/create', methods=['GET', 'POST'])
def franchise_overpriced_create():
    fo_cs = current_app.config["franchise_overpriced_command_service"]
    user_data = session.get('user_data')
    if request.method == 'POST':
        try:
            extra_price = float(request.form['extra_price'])
            franchise_id = request.form.get('franchise_id') or None
            plan_id = request.form.get('plan_id') or None
            fo_cs.create(
                extra_price,
                int(franchise_id) if franchise_id else None,
                int(plan_id) if plan_id else None
            )
            flash('Sobreprecio creado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_overpriced_index'))
        except Exception as e:
            flash(f'Error al crear el sobreprecio: {e}', 'danger')
    return render_template('rental/franchise_overpriced/create.html', user_data=user_data)

@rental_module_api.route('/franchise-overpriced/edit/<int:overpriced_id>', methods=['GET', 'POST'])
def franchise_overpriced_edit(overpriced_id):
    fo_qs = current_app.config["franchise_overpriced_query_service"]
    fo_cs = current_app.config["franchise_overpriced_command_service"]
    user_data = session.get('user_data')
    overpriced = fo_qs.get_by_id(overpriced_id)
    if not overpriced:
        flash('Sobreprecio no encontrado.', 'danger')
        return redirect(url_for('rental_module_api.franchise_overpriced_index'))
    if request.method == 'POST':
        try:
            extra_price = float(request.form['extra_price'])
            franchise_id = request.form.get('franchise_id') or None
            plan_id = request.form.get('plan_id') or None
            fo_cs.update(
                overpriced_id,
                extra_price,
                int(franchise_id) if franchise_id else None,
                int(plan_id) if plan_id else None
            )
            flash('Sobreprecio actualizado exitosamente.', 'success')
            return redirect(url_for('rental_module_api.franchise_overpriced_index'))
        except Exception as e:
            flash(f'Error al actualizar el sobreprecio: {e}', 'danger')
    return render_template(
        'rental/franchise_overpriced/edit.html',
        overpriced=overpriced,
        user_data=user_data
    )

@rental_module_api.route('/franchise-overpriced/delete/<int:overpriced_id>', methods=['POST'])
def franchise_overpriced_delete(overpriced_id):
    fo_cs = current_app.config["franchise_overpriced_command_service"]
    try:
        fo_cs.delete(overpriced_id)
        flash('Sobreprecio eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el sobreprecio: {e}', 'danger')
    return redirect(url_for('rental_module_api.franchise_overpriced_index'))
