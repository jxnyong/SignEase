from flask import request, jsonify, session
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from werkzeug.security import check_password_hash, generate_password_hash
from app import database, app, db2

# Route for handling user sign-in
@app.route("/signin", methods=["POST"])
def signin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    print(f'user:{username} tryed to log in')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = database.users.find_one({"username": username})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Bad username or password"}), 401

    fullName = (user.get("full_name", ""),)
    username = (user.get("username", ""),)
    email = user.get("email", "")
    # create a new token
    access_token = create_access_token(identity=username)
    db2.syncMembership()
    return (jsonify({"success": True, "access_token": access_token, "username": username, "fullName": fullName, "email": email}), 200,)


# Route for handling user sign-up
@app.route("/signup", methods=["POST"])
def signup():
    firstName = request.json.get("firstName", None)
    lastName = request.json.get("lastName", None)
    full_name = request.json.get("fullName", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not full_name or not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Check if the username or email already exists in the database
    existing_user = database.users.find_one({"$or": [{"username": username}, {"email": email}]})

    if existing_user:
        return jsonify({"msg": "Username or email already exists"}), 409
    
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user document
    new_user = {
        "firstName": firstName,
        "lastName" : lastName,
        "full_name": full_name,
        "username": username,
        "email": email,
        "password": hashed_password
    }
    database.users.insert_one(new_user)

    return jsonify({"success": True})

# Route for handling user logout
@app.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"logout": True})
    unset_jwt_cookies(resp)
    return resp, 200
