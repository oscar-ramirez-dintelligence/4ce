from flask import render_template, session, redirect, url_for
from . import bp

@bp.route('/')
def index_page():
    """
    Renders the main dashboard for logged-in users.
    If the user is not logged in, it redirects them to the login page.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # For now, it's a simple welcome. This can be expanded with real data.
    return render_template('main/dashboard.html')
