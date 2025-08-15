from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import cotizacion_service, tipos_cliente_service, soporte_service

@bp.route('/')
def list_page():
    """Renders the page that lists all quotations, with advanced filtering."""
    filters = {k: v for k, v in request.args.items() if v}
    cotizaciones = cotizacion_service.get_all_cotizaciones(filters=filters)
    return render_template(
        'cotizaciones/cotizaciones_list.html',
        cotizaciones=cotizaciones,
        filters=filters
    )

@bp.route('/new', methods=['GET', 'POST'])
def new_page():
    """Renders the form to create a new quotation and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_data['soportes_seleccionados'] = request.form.getlist('soportes_seleccionados')
        # Basic type conversion, more robust validation could be added
        form_data['probabilidad_cierre'] = float(form_data.get('probabilidad_cierre', 0))
        form_data['presupuesto_estimado'] = float(form_data.get('presupuesto_estimado', 0))

        cotizacion_service.create_cotizacion(form_data)
        flash('Cotización creada exitosamente.', 'success')
        return redirect(url_for('cotizaciones.list_page'))

    # For GET request, fetch data needed to populate the form
    tipos_cliente = tipos_cliente_service.get_all_tipos_cliente()
    soportes = soporte_service.get_all_soportes() # This could be slow if there are many

    return render_template(
        'cotizaciones/cotizacion_form.html',
        cotizacion={},
        tipos_cliente=tipos_cliente,
        soportes=soportes
    )

@bp.route('/<string:cotizacion_id>/edit', methods=['GET', 'POST'])
def edit_page(cotizacion_id):
    """Renders the form to edit an existing quotation and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_data['soportes_seleccionados'] = request.form.getlist('soportes_seleccionados')
        form_data['probabilidad_cierre'] = float(form_data.get('probabilidad_cierre', 0))
        form_data['presupuesto_estimado'] = float(form_data.get('presupuesto_estimado', 0))

        cotizacion_service.update_cotizacion(cotizacion_id, form_data)
        flash('Cotización actualizada exitosamente.', 'success')
        return redirect(url_for('cotizaciones.list_page'))

    cotizacion = cotizacion_service.get_cotizacion_by_id(cotizacion_id)
    if not cotizacion:
        flash('Cotización no encontrada.', 'danger')
        return redirect(url_for('cotizaciones.list_page'))

    tipos_cliente = tipos_cliente_service.get_all_tipos_cliente()
    soportes = soporte_service.get_all_soportes()

    return render_template(
        'cotizaciones/cotizacion_form.html',
        cotizacion=cotizacion,
        tipos_cliente=tipos_cliente,
        soportes=soportes
    )
