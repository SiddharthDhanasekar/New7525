from flask import request
from app.services.db.mysql import db_connection
from app.services.teacher.business import saveLog
from werkzeug.security import check_password_hash

def handle_teacher_login():
    email = request.form.get('email')
    code = request.form.get('code')

    print(f"Debug: Received email = {email}")
    print(f"Debug: Received code = {code}")

    if not email or not code:
        print("Debug: Missing email or code")
        return {'error': 'Email and code are required'}, 400

    conn = None
    try:
        conn = db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, password_hash FROM teachers WHERE email=%s",
                (email,)
            )
            teacher = cursor.fetchone()

            if not teacher:
                print("Debug: No teacher found with email")
                return {'error': 'Invalid credentials'}, 401

            teacher_id = teacher[0]
            stored_password_hash = teacher[1]

            print(f"Debug: Stored hash from DB = {stored_password_hash}")

            if not check_password_hash(stored_password_hash, code):
                print("Debug: Password check failed")
                return {'error': 'Incorrect passcode'}, 401

            print("Debug: Password check succeeded")
            saveLog(email, "login")

            return {
                'teacher_id': teacher_id,
                'email': email
            }, 200

    except Exception as e:
        print(f"Login error: {e}")
        if conn:
            conn.rollback()
        return {'error': 'Login failed'}, 500
    finally:
        if conn:
            conn.close()


def handle_admin_login():
    """
    Handles admin login authentication
    Returns:
        tuple: (dict response, int status_code)
    """
    email = request.form.get('email')
    code = request.form.get('code')

    if not email or not code:
        return {'error': 'Email and code are required'}, 400

    conn = None
    try:
        conn = db_connection()
        with conn.cursor() as cursor:
            # Get admin info
            cursor.execute(
                "SELECT id, password_hash FROM admins WHERE email=%s",
                (email,)
            )
            admin = cursor.fetchone()

            if not admin:
                return {'error': 'Invalid credentials'}, 401


            admin_id = admin[0]
            stored_password_hash = admin[1]
            input_password_hash = hashlib.sha256(code.encode()).hexdigest()

            # Check passcode
           
            if input_password_hash != stored_password_hash:
                return {'error': 'Incorrect passcode'}, 401

            return {
                'admin_id': admin_id,
                'email': email
            }, 200

    except Exception as e:
        print(f"Login error: {e}")
        if conn:
            conn.rollback()
        return {'error': 'Login failed'}, 500
    finally:
        if conn:
            conn.close()
