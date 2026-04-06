from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db, bcrypt
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: saiganesh
            email:
              type: string
              example: sai@example.com
            password:
              type: string
              example: secret123
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields
      409:
        description: Email or username already exists
    """
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "username, email and password are required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "email already registered"}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "username already taken"}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role='user'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login():
    """
    Login and get JWT tokens
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: sai@example.com
            password:
              type: string
              example: secret123
    responses:
      200:
        description: Login successful, returns access and refresh tokens
      400:
        description: Missing fields
      401:
        description: Invalid credentials
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"error": "invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Get new access token using refresh token
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: New access token
      401:
        description: Invalid or expired refresh token
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token}), 200


@auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Get current logged in user details
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Current user details
      401:
        description: Missing or invalid token
      404:
        description: User not found
    """
    identity = get_jwt_identity()
    user = User.query.get(int(identity))
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200


@auth.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    """
    Logout and revoke access token
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Successfully logged out
      401:
        description: Missing or invalid token
    """
    jti = get_jwt()['jti']
    from app.models import TokenBlocklist
    blocked_token = TokenBlocklist(jti=jti)
    db.session.add(blocked_token)
    db.session.commit()
    return jsonify({"message": "successfully logged out"}), 200