from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Show the landing page (index.html).
    """
    # return render_template('index.html')
    return redirect(url_for('teacher.teacher_home'))

# If you want to add SocketIO events here later, use a lazy import inside the function, e.g.:

# @socketio.on('join-admin-room')
# def handle_join_admin_room():
#     from run import socketio  # import inside the function to avoid circular imports
#     from flask_socketio import join_room
#     join_room('admin-room')
#     print("Admin joined admin-room")
