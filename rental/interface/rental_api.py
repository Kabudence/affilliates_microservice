from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

from application.domain.entities.application_data import ApplicationType

rental_module_api = Blueprint('rental_module_api', __name__)

@rental_module_api.route('/metas')
def metas_index():
    goal_query_service = current_app.config["goal_query_service"]
    goals = goal_query_service.list_all()
    user_data = session.get('user_data')
    return render_template('rental/metas_index.html', goals=goals, user_data=user_data)

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
    return render_template('rental/metas_create.html', user_data=user_data)

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
    return render_template('rental/metas_edit.html', goal=goal, user_data=user_data)

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
