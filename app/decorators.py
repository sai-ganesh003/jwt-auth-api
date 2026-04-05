from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if not user or user.role != 'admin':
            return jsonify({"error": "admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.get(int(identity))
            if not user or user.role != role:
                return jsonify({"error": f"{role} access required"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator