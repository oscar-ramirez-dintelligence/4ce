import os
from flask import render_template, request
from . import bp
from cotizador.services import soporte_service

@bp.route('/')
def catalogue():
    """
    Renders the catalogue page for advertising supports, including pagination
    and data for the Google Map.
    """
    start_at = request.args.get('start_at')
    soportes, next_page_cursor = soporte_service.get_paginated_soportes(start_at)
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template(
        'soportes_catalogue.html',
        soportes=soportes,
        next_page_cursor=next_page_cursor,
        google_maps_api_key=google_maps_api_key
    )
