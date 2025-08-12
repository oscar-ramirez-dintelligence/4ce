import os
from flask import render_template, request
from . import bp
from cotizador.services import soporte_service

# Note: The routes in this file will be prefixed with `/soportes` as defined
# in the blueprint registration in `create_app`.

@bp.route('/')
def catalogue():
    """
    Renders the catalogue page for advertising supports, including pagination
    and data for the Google Map.
    """
    # Get the cursor for pagination from the query string
    start_at = request.args.get('start_at')

    # Call the service layer to get the data
    soportes, next_page_cursor = soporte_service.get_paginated_soportes(start_at)

    # Get the Google Maps API key from environment variables
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template(
        'soportes_catalogue.html',
        soportes=soportes,
        next_page_cursor=next_page_cursor,
        google_maps_api_key=google_maps_api_key
    )
