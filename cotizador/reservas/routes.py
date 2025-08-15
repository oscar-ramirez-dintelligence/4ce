from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import reserva_service

@bp.route('/')
def list_page():
    """Renders the page that lists all reservas."""
    reservas = reserva_service.get_all_reservas()
    return render_template('reservas/list.html', reservas=reservas)

@bp.route('/new', methods=['GET', 'POST'])
def new_page():
    """Renders the form to create a new reserva and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Basic validation could be added here
        reserva_service.create_reserva(form_data)
        flash('Reserva creada exitosamente.', 'success')
        return redirect(url_for('reservas.list_page'))

    # In a real scenario, we'd pass a list of soportes to select from
    return render_template('reservas/form.html', reserva={})

@bp.route('/<string:reserva_id>/edit', methods=['GET', 'POST'])
def edit_page(reserva_id):
    """Renders the form to edit an existing reserva and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        reserva_service.update_reserva(reserva_id, form_data)
        flash('Reserva actualizada exitosamente.', 'success')
        return redirect(url_for('reservas.list_page'))

    reserva = reserva_service.get_reserva_by_id(reserva_id)
    if not reserva:
        flash('Reserva no encontrada.', 'danger')
        return redirect(url_for('reservas.list_page'))

    return render_template('reservas/form.html', reserva=reserva)
