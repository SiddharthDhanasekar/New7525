import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
load_dotenv()

app.secret_key = 'prufia_user'
app.config['WALL_FOLDER'] = 'walls'
app.config['ASSIGNMENT_FOLDER'] = 'assignments'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

socketio = SocketIO(app, cors_allowed_origins="*")
os.makedirs(app.config['ASSIGNMENT_FOLDER'], exist_ok=True)

from app.routes.main_routes    import main_bp
from app.routes.admin_routes   import admin_bp
from app.routes.teacher_routes import teacher_bp

app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
