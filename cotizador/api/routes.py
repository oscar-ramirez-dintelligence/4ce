from flask import request, jsonify
from . import bp
from cotizador.services import soporte_service, cotizacion_service, tipos_cliente_service

@bp.route('/tipos_cliente', methods=['GET'])
def get_tipos_cliente():
    """Returns a list of all client types."""
    tipos = tipos_cliente_service.get_all_tipos_cliente()
    return jsonify(tipos)

@bp.route('/soportes', methods=['GET'])
def get_soportes():
    """Returns a paginated list of advertising supports."""
    start_at = request.args.get('start_at')
    soportes, cursor = soporte_service.get_paginated_soportes(start_at)
    return jsonify({"soportes": soportes, "next_page_cursor": cursor})

@bp.route('/soporte/<string:soporte_id>', methods=['GET'])
def get_soporte(soporte_id):
    """Returns a single advertising support by its ID."""
    soporte = soporte_service.get_soporte_by_id(soporte_id)
    if soporte:
        return jsonify(soporte)
    return jsonify({"error": "Soporte not found"}), 404

@bp.route('/soportes', methods=['POST'])
def create_soporte():
    """Creates a new advertising support."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    new_soporte = soporte_service.create_soporte(data)
    if new_soporte:
        return jsonify(new_soporte), 201
    return jsonify({"error": "Failed to create soporte"}), 500

@bp.route('/soporte/<string:soporte_id>', methods=['PUT', 'PATCH'])
def update_soporte(soporte_id):
    """Updates an existing advertising support."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    updated_soporte = soporte_service.update_soporte(soporte_id, data)
    if updated_soporte:
        return jsonify(updated_soporte)
    return jsonify({"error": "Soporte not found or update failed"}), 404

@bp.route('/soporte/<string:soporte_id>', methods=['DELETE'])
def delete_soporte(soporte_id):
    """Deletes an advertising support."""
    success = soporte_service.delete_soporte(soporte_id)
    if success:
        return '', 204
    return jsonify({"error": "Soporte not found or delete failed"}), 404

@bp.route('/cotizaciones', methods=['GET'])
def get_cotizaciones():
    """Returns a list of all quotations."""
    cotizaciones = cotizacion_service.get_all_cotizaciones()
    return jsonify(cotizaciones)

@bp.route('/cotizacion/<string:cotizacion_id>', methods=['GET'])
def get_cotizacion(cotizacion_id):
    """Returns a single quotation by its ID."""
    cotizacion = cotizacion_service.get_cotizacion_by_id(cotizacion_id)
    if cotizacion:
        return jsonify(cotizacion)
    return jsonify({"error": "Cotizacion not found"}), 404

@bp.route('/cotizaciones', methods=['POST'])
def create_cotizacion():
    """Creates a new quotation."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    new_cotizacion = cotizacion_service.create_cotizacion(data)
    if new_cotizacion:
        return jsonify(new_cotizacion), 201
    return jsonify({"error": "Failed to create cotizacion"}), 500
