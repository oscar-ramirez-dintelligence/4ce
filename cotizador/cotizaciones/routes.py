from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import cotizacion_service, soporte_service, tipos_cliente_service

# Note: The routes in this file will be prefixed with `/cotizaciones`

@bp.route('/')
def list_page():
    """Renders the page that lists all existing quotations."""
    cotizaciones = cotizacion_service.get_all_cotizaciones()
    return render_template('cotizaciones_list.html', cotizaciones=cotizaciones)

@bp.route('/new', methods=['GET', 'POST'])
def new_page():
    """
    Renders the form to create a new quotation and handles the form submission.
    """
    if request.method == 'POST':
        try:
            # Extract data from the form
            form_data = {
                "titulo": request.form.get('titulo'),
                "ejecutivo": request.form.get('ejecutivo'),
                "anunciante": request.form.get('anunciante'),
                "agencia": request.form.get('agencia', ''),
                "tipo_cliente": request.form.get('tipo_cliente'),
                "probabilidad_cierre": float(request.form.get('probabilidad_cierre', 0)) / 100.0,
                "presupuesto_estimado": float(request.form.get('presupuesto_estimado', 0)),
                "periodo_inicio": request.form.get('periodo_inicio'),
                "periodo_fin": request.form.get('periodo_fin'),
                "soportes_seleccionados": request.form.getlist('soportes_seleccionados'),
                "logo_cliente_ref": "", # Placeholder
                "logo_agencia_ref": ""  # Placeholder
            }

            # Call the service layer to create the document
            new_cotizacion = cotizacion_service.create_cotizacion(form_data)

            if new_cotizacion:
                flash(f"Cotización '{new_cotizacion['titulo']}' creada exitosamente.", 'success')
                return redirect(url_for('cotizaciones.list_page'))
            else:
                flash('Ocurrió un error al guardar la cotización en la base de datos.', 'danger')

        except Exception as e:
            flash(f"Ocurrió un error al procesar el formulario: {e}", 'danger')
            # Fall through to render the form again

    # For a GET request, fetch all the data needed to populate the form's dynamic fields
    tipos_cliente = tipos_cliente_service.get_all_tipos_cliente()
    soportes = soporte_service.get_all_soportes()

    return render_template('cotizacion_form.html', tipos_cliente=tipos_cliente, soportes=soportes)
