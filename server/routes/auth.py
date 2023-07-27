from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import database, app

# Route for handling user sign-in
@app.route('/signin', methods=['POST'])
def signin():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = database.users.find_one({"username": username})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({"success": True, "access_token": access_token}), 200