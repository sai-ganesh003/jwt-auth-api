# JWT Auth API

A production-ready JWT Authentication REST API built with Flask, MySQL, and bcrypt.

## Live Demo
Base URL: `https://jwt-auth-api-production-61d5.up.railway.app`
Swagger Docs: `https://jwt-auth-api-production-61d5.up.railway.app/apidocs`

## Tech Stack
- Python 3.11, Flask
- MySQL (Railway), SQLAlchemy ORM
- bcrypt password hashing
- JWT access + refresh tokens (flask-jwt-extended)
- Token blocklist for real logout
- Role-based access control (RBAC)
- Swagger UI via Flasgger
- Deployed on Railway

## Features
- `POST /register` — create user with hashed password
- `POST /login` — returns access + refresh tokens
- `POST /refresh` — get new access token
- `GET /me` — get current user (protected)
- `DELETE /logout` — revoke token (blocklist)
- `GET /admin/users` — list all users (admin only)
- `DELETE /admin/users/<id>` — delete user (admin only)

## Run Locally
```bash
git clone https://github.com/sai-ganesh003/jwt-auth-api
cd jwt-auth-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# create .env with DATABASE_URL and JWT_SECRET_KEY
python run.py
```

## Environment Variables
```
DATABASE_URL=mysql+pymysql://user:password@host:port/dbname
JWT_SECRET_KEY=your-secret-key
```