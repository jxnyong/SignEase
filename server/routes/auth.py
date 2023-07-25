from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import database, app

@app.route('/signin', methods=['POST'])
def signin():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = database.users.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200
