from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient("mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority")  # Modify with your MongoDB connection string if needed
db = client["SignEase"]
collection = db["users"]

@app.route('/api/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = collection.find_one({"username": username})
    if user:
        return dumps({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = {"username": username, "password": hashed_password}

    collection.insert_one(new_user)
    return dumps({'message': 'User created successfully'}), 201


@app.route('/api/user/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = collection.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return dumps({'message': 'Invalid username or password'}), 400

    return dumps({'message': 'Login successful'}), 200
