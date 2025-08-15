from flask import render_template, request, redirect, url_for, flash
from . import bp
from cotizador.services import campana_service

@bp.route('/')
def list_page():
    """Renders the page that lists all campanas."""
    campanas = campana_service.get_all_campanas()
    return render_template('campanas/list.html', campanas=campanas)

@bp.route('/new', methods=['GET', 'POST'])
def new_page():
    """Renders the form to create a new campana and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        campana_service.create_campana(form_data)
        flash('Campaña creada exitosamente.', 'success')
        return redirect(url_for('campanas.list_page'))

    return render_template('campanas/form.html', campana={})

@bp.route('/<string:campana_id>/edit', methods=['GET', 'POST'])
def edit_page(campana_id):
    """Renders the form to edit an existing campana and handles submission."""
    if request.method == 'POST':
        form_data = request.form.to_dict()
        campana_service.update_campana(campana_id, form_data)
        flash('Campaña actualizada exitosamente.', 'success')
        return redirect(url_for('campanas.list_page'))

    campana = campana_service.get_campana_by_id(campana_id)
    if not campana:
        flash('Campaña no encontrada.', 'danger')
        return redirect(url_for('campanas.list_page'))

    return render_template('campanas/form.html', campana=campana)
