from flask import render_template, request, session, redirect, url_for, flash
from . import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the user login, setting a value in the session cookie."""
    # Clear any existing session
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            flash(f'¡Sesión iniciada como {username}!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Por favor, introduce un nombre de usuario.', 'warning')

    # For a GET request, we will render a template.
    # The template will be created in a later step.
    return render_template('login.html')

@bp.route('/profile')
def profile():
    """Displays a profile page if the user is in the session."""
    if 'username' not in session:
        flash('Debes iniciar sesión para ver esta página.', 'info')
        return redirect(url_for('main.login'))

    # The template will be created in a later step.
    return render_template('profile.html')

@bp.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.pop('username', None)
    flash('Has cerrado la sesión exitosamente.', 'info')
    return redirect(url_for('main.index_page'))

@bp.route('/')
def index_page():
    """Renders the main welcome page of the application."""
    # The 'index' endpoint is set in create_app to point here.
    return render_template('index.html')
