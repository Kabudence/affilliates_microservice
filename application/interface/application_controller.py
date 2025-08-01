from flask import Blueprint, render_template, request, current_app

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

