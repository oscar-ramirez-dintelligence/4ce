from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import agencia_service

@bp.route('/')
def list_page():
    """Renders the page that lists all agencies, with advanced filtering."""
    filters = {k: v for k, v in request.args.items() if v}
    agencias = agencia_service.get_all_agencias(filters=filters)
    return render_template(
        'agencias/agencias_list.html',
        agencias=agencias,
        filters=filters
    )

@bp.route('/new', methods=['GET', 'POST'])
def new_page():
    """Renders the form to create a new agency and handles submission."""
    if request.method == 'POST':
        # This is a simplified data extraction. A real app would have more validation
        # and would handle the nested 'contactos' structure more robustly.
        form_data = {
            "nombre": request.form.get('nombre'),
            "razon_social": request.form.get('razon_social'),
            "rfc": request.form.get('rfc'),
            "giro": request.form.get('giro'),
            "direccion": request.form.get('direccion'),
            "grupo": request.form.get('grupo'),
            "contactos": {
                "financiero": {
                    "nombre": request.form.get('contacto_financiero_nombre'),
                    "email": request.form.get('contacto_financiero_email'),
                    "telefono": request.form.get('contacto_financiero_telefono'),
                },
                "comercial": {
                    "nombre": request.form.get('contacto_comercial_nombre'),
                    "email": request.form.get('contacto_comercial_email'),
                    "telefono": request.form.get('contacto_comercial_telefono'),
                }
            }
        }
        agencia_service.create_agencia(form_data)
        flash('Agencia creada exitosamente.', 'success')
        return redirect(url_for('agencias.list_page'))

    return render_template('agencias/agencia_form.html', agencia={})

@bp.route('/<string:agencia_id>/edit', methods=['GET', 'POST'])
def edit_page(agencia_id):
    """Renders the form to edit an existing agency and handles submission."""
    if request.method == 'POST':
        form_data = {
            "nombre": request.form.get('nombre'),
            "razon_social": request.form.get('razon_social'),
            "rfc": request.form.get('rfc'),
            "giro": request.form.get('giro'),
            "direccion": request.form.get('direccion'),
            "grupo": request.form.get('grupo'),
            "contactos": {
                "financiero": {
                    "nombre": request.form.get('contacto_financiero_nombre'),
                    "email": request.form.get('contacto_financiero_email'),
                    "telefono": request.form.get('contacto_financiero_telefono'),
                },
                "comercial": {
                    "nombre": request.form.get('contacto_comercial_nombre'),
                    "email": request.form.get('contacto_comercial_email'),
                    "telefono": request.form.get('contacto_comercial_telefono'),
                }
            }
        }
        agencia_service.update_agencia(agencia_id, form_data)
        flash('Agencia actualizada exitosamente.', 'success')
        return redirect(url_for('agencias.list_page'))

    agencia = agencia_service.get_agencia_by_id(agencia_id)
    if not agencia:
        flash('Agencia no encontrada.', 'danger')
        return redirect(url_for('agencias.list_page'))

    return render_template('agencias/agencia_form.html', agencia=agencia)
