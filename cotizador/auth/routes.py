from flask import render_template, request, redirect, url_for, flash, session
from . import bp
from cotizador.services import user_service

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email y contraseña son obligatorios.', 'warning')
            return redirect(url_for('auth.login'))

        user = user_service.check_credentials(email, password)

        if user:
            session.clear()
            session['user_id'] = user['uid']
            session['user_name'] = user['nombre_completo']
            session['user_email'] = user['email']
            session['user_role'] = user['rol']
            flash(f'Bienvenido de nuevo, {user["nombre_completo"]}!', 'success')
            return redirect(url_for('dashboard.main_dashboard'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'danger')

    return render_template('auth/login.html')

@bp.route('/logout', methods=['POST'])
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    flash('Has cerrado la sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user registration."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('nombre_completo')

        if not all([email, password, full_name]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            # All self-registered users get the default role 'ejecutivo'
            user_service.create_user(email, password, full_name, role='ejecutivo')
            flash('¡Cuenta creada exitosamente! Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger') # Show error if user already exists
        except Exception as e:
            flash(f'Ocurrió un error inesperado: {e}', 'danger')

    return render_template('auth/register.html')
