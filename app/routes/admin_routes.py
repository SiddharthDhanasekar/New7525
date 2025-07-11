from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for

# Imports from your existing services
from app.services.auth.login import handle_admin_login

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admins():
    """
    Render the main admin dashboard.
    """
    if 'admin_id' not in session:
        return redirect(url_for('admin.adminLogin'))

    return render_template(
        'admin_page.html'
    )


@admin_bp.route('/admin-login')
def adminLogin():
    """
    Show admin login form (GET).
    """
    return render_template('adminlogin.html')


@admin_bp.route('/admin-login', methods=['POST'])
def admin_login():
    """
    Handle admin login (POST).
    """
    result, status_code = handle_admin_login()
    if status_code != 200:
        return render_template('adminlogin.html', error=result.get('error', 'Unknown error')), status_code

    session['admin_id'] = result['admin_id']
    session['admin_email'] = result['email']
    return redirect(url_for('admin.admins'))


@admin_bp.route('/admin-logout')
def admin_logout():
    """
    Clear admin session and redirect to login.
    """
    session.clear()
    return jsonify({'redirect_url': url_for('admin.adminLogin')})
