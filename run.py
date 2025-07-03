import os
import sys

from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

# 1) Flask‐app initialization (with custom template/static dirs)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
load_dotenv()

app.secret_key = 'prufia_user'
app.config['WALL_FOLDER'] = 'walls'
app.config['ASSIGNMENT_FOLDER'] = 'assignments'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# 2) Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 3) Ensure folder existence
os.makedirs(app.config['ASSIGNMENT_FOLDER'], exist_ok=True)

# 4) Import and register all blueprints after Flask and SocketIO exist
from app.routes.main_routes    import main_bp
from app.routes.admin_routes   import admin_bp
from app.routes.teacher_routes import teacher_bp

app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)

def run_server():
    """
    Attempt to run on PORT, or PORT+1, or PORT+2 if ports already in use.
    """
    try:
        port = int(os.environ.get('PORT', 80))
        host = os.environ.get('HOST', '0.0.0.0')

        for p in [port, port + 1, port + 2]:
            try:
                app.run(host=host, port=p, debug=True)
                break
            except OSError as e:
                if "address in use" in str(e):
                    print(f"Port {p} in use, trying next...")
                    continue
                raise
    except Exception as e:
        print(f"Server failed: {str(e)}")

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=80,
        debug=True,
        use_reloader=False
    )