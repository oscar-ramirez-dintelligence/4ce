from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import user_service, company_service

@bp.route('/users')
def list_users():
    """Renders the page that lists all users."""
    users = user_service.get_all_users()
    return render_template('admin/users_list.html', users=users)

@bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    """Renders the form to create a new user and handles submission."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('nombre_completo')
        role = request.form.get('rol')

        if not all([email, password, full_name, role]):
            flash('Todos los campos son obligatorios.', 'danger')
        else:
            try:
                new_user = user_service.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    role=role
                )
                if new_user:
                    flash(f"Usuario '{full_name}' creado exitosamente.", 'success')
                    return redirect(url_for('admin.list_users'))
                else:
                    flash('Ocurrió un error al crear el usuario.', 'danger')
            except Exception as e:
                flash(f"Error: {e}", 'danger')

    return render_template('admin/user_form.html')

@bp.route('/company', methods=['GET', 'POST'])
def company_config():
    """
    Renders the company configuration form and handles updates.
    """
    if request.method == 'POST':
        try:
            # In a real app, you would handle file uploads for logos separately.
            # Here we just save the text data.
            form_data = {
                "nombre_empresa": request.form.get('nombre_empresa'),
                "idioma": request.form.get('idioma'),
                "opciones_inventario": request.form.get('opciones_inventario') == 'on',
                "direccion": request.form.get('direccion'),
                "telefono": request.form.get('telefono'),
                "correo_electronico": request.form.get('correo_electronico'),
                "descripcion": request.form.get('descripcion'),
            }
            company_service.update_company_config(form_data)
            flash('La configuración de la empresa se ha actualizado correctamente.', 'success')
            return redirect(url_for('admin.company_config'))
        except Exception as e:
            flash(f"Ocurrió un error al actualizar la configuración: {e}", 'danger')

    config_data = company_service.get_company_config()
    return render_template('admin/company_form.html', config=config_data)
