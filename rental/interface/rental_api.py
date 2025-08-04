# rental_module_api.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

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
    return render_template('rental/metas_create.html')

@rental_module_api.route('/metas/edit/<int:goal_id>', methods=['GET', 'POST'])
def metas_edit(goal_id):
    goal_query_service = current_app.config["goal_query_service"]
    goal_command_service = current_app.config["goal_command_service"]
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
    return render_template('rental/metas_edit.html', goal=goal)

@rental_module_api.route('/metas/delete/<int:goal_id>', methods=['POST'])
def metas_delete(goal_id):
    goal_command_service = current_app.config["goal_command_service"]
    try:
        goal_command_service.delete(goal_id)
        flash('Meta eliminada exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar la meta: ' + str(e), 'danger')
    return redirect(url_for('rental_module_api.metas_index'))
