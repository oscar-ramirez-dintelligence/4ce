import os
import json
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import bp
from cotizador.firebase import get_auth

@bp.route('/login', methods=['GET'])
def login():
    """Renders the login page with the necessary Firebase config."""
    try:
        firebase_config_json = os.getenv('FIREBASE_WEB_CONFIG_JSON', '{}')
        firebase_config = json.loads(firebase_config_json)
    except json.JSONDecodeError:
        flash("La configuración de Firebase para la web no es un JSON válido.", "danger")
        firebase_config = {}

    return render_template('auth/login.html', firebase_config=firebase_config)

@bp.route('/logout', methods=['POST'])
def logout():
    """Logs the user out by clearing the session cookie."""
    session.clear()
    return redirect(url_for('main.index_page'))

@bp.route('/session-login', methods=['POST'])
def session_login():
    """
    Verifies a Firebase ID token sent from the client and creates a server-side session.
    """
    try:
        id_token = request.json.get('idToken')
        if not id_token:
            return jsonify({"error": "No ID token provided."}), 400

        decoded_token = get_auth().verify_id_token(id_token)
        uid = decoded_token['uid']

        session['user_id'] = uid
        session['email'] = decoded_token.get('email')

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": f"Invalid token or error during session creation: {e}"}), 401
