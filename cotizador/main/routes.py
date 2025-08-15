from flask import render_template, session, redirect, url_for
from . import bp

@bp.route('/')
def index_page():
    """
    The main entry point. If logged in, redirects to the sales dashboard.
    If not, redirects to the login page.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Redirect logged-in users to the main sales dashboard
    return redirect(url_for('dashboard.main_dashboard'))
