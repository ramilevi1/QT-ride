from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime, timedelta
import jwt  # <-- JWT support added
import os

from database import db
from models import User

app = Flask(__name__)
# Use absolute path for SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'auth_service.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'auth_service_secret_key'  # used by Flask internally
JWT_SECRET = 'your_secret'  # <-- used for signing JWT

db.init_app(app)
migrate = Migrate(app, db)

# ----------- JWT Helper -----------
def generate_jwt(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 409

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    app.logger.info(f"Received sign-in request for email: {data['email']}")
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        app.logger.info("Sign-in successful")

        # 🔐 Generate JWT token
        token = generate_jwt(user_id=str(user.id), email=user.email)

        # 🍪 Set token in cookie
        response = make_response(jsonify({
            'message': 'Signed in successfully',
            'access_token': token  # ✅ ADD JWT in JSON too
        }))
        response.set_cookie(
            'access_token',
            token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            max_age=24 * 60 * 60  # 1 day
        )
        return response

    app.logger.info("Sign-in failed: Invalid email or password")
    return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/signout', methods=['POST'])
def signout():
    response = jsonify({'message': 'Signed out successfully'})
    response.set_cookie('access_token', '', expires=0)
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5001, debug=True)
