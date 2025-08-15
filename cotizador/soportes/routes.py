import os
from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import soporte_service

@bp.route('/')
def catalogue():
    # ... (existing catalogue code) ...
    start_at_id = request.args.get('start_at')
    start_at_doc = None
    if start_at_id:
        start_at_doc = soporte_service.get_soporte_by_id(start_at_id)

    filters = {
        'nombre_soporte': request.args.get('nombre_soporte'),
        'codigo_soporte': request.args.get('codigo_soporte'),
        'tipo_soporte': request.args.get('tipo_soporte'),
        'municipio': request.args.get('municipio'),
    }
    filters = {k: v for k, v in filters.items() if v}

    soportes, next_page_cursor = soporte_service.get_paginated_soportes(
        start_at_doc=start_at_doc,
        filters=filters
    )

    next_page_cursor_id = next_page_cursor.id if next_page_cursor else None

    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template(
        'soportes/soportes_catalogue.html',
        soportes=soportes,
        next_page_cursor_id=next_page_cursor_id,
        filters=filters,
        google_maps_api_key=google_maps_api_key
    )

@bp.route('/new', methods=['GET', 'POST'])
def new_soporte():
    """Renders the form to create a new soporte and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Convert numeric fields
        form_data['precio_minimo'] = float(form_data.get('precio_minimo', 0))
        form_data['precio_mensual'] = float(form_data.get('precio_mensual', 0))
        form_data['latitud'] = float(form_data.get('latitud', 0))
        form_data['longitud'] = float(form_data.get('longitud', 0))

        soporte_service.create_soporte(form_data)
        flash('Soporte creado exitosamente.', 'success')
        return redirect(url_for('soportes.catalogue'))

    return render_template('soportes/soporte_form.html', soporte={})

@bp.route('/<string:soporte_id>/edit', methods=['GET', 'POST'])
def edit_soporte(soporte_id):
    """Renders the form to edit an existing soporte and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Convert numeric fields
        form_data['precio_minimo'] = float(form_data.get('precio_minimo', 0))
        form_data['precio_mensual'] = float(form_data.get('precio_mensual', 0))
        form_data['latitud'] = float(form_data.get('latitud', 0))
        form_data['longitud'] = float(form_data.get('longitud', 0))

        soporte_service.update_soporte(soporte_id, form_data)
        flash('Soporte actualizado exitosamente.', 'success')
        return redirect(url_for('soportes.catalogue'))

    soporte = soporte_service.get_soporte_by_id(soporte_id)
    if not soporte:
        flash('Soporte no encontrado.', 'danger')
        return redirect(url_for('soportes.catalogue'))

    return render_template('soportes/soporte_form.html', soporte=soporte)
