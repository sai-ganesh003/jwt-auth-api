from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.decorators import admin_required
from app.models import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role
    } for u in users]), 200

@admin.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    from app import db
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"user {user_id} deleted"}), 200