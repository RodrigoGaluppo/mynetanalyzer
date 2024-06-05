from flask import Blueprint, request, jsonify
from models.User import User
from datetime import datetime, timedelta
from Global import sessionMaker, SECRET_KEY, token_required
import jwt

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        role=data['role'],
        created_at=datetime.now()
    )
    new_user.set_password(data['password'])
    session = sessionMaker()
    try:
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@user_blueprint.route('', methods=['GET'])
def get_users():
    session = sessionMaker()
    try:
        users = session.query(User).all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = sessionMaker()
    try:
        user = session.query(User).get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@user_blueprint.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    session = sessionMaker()
    try:
        user = session.query(User).get(user_id)
        if user:
            if 'password' in data:
                user.set_password(data['password'])
            session.commit()
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = sessionMaker()
    try:
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User deleted"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    session = sessionMaker()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, SECRET_KEY, algorithm='HS256')
            return jsonify({
                "user":user.to_dict(),
                'token': token
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
