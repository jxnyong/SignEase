from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from typing import Dict
from model import HandGestureRecogniser 
import cv2, model
import numpy as np
import base64
from mongodb import MongoDB, TABLES
from werkzeug.security import check_password_hash
from concurrent.futures import ThreadPoolExecutor
database = MongoDB(*TABLES)
model.__draw__ = (False, True, True)
slots:Dict[str, HandGestureRecogniser] = dict()
app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=['POST', 'GET'])
def stringToImage(base64_string: str):
    """Decode the numpy array as an image using OpenCV"""
    return cv2.imdecode(np.frombuffer(base64.b64decode(base64_string.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)
@app.route('/video', methods=['POST'])
def process_video() -> Response:
    global slots
    try:
        session = request.form.get('name')  # Get the name from the form data
        if not slots.get(session, False): slots[session] = HandGestureRecogniser()
        screenshot = request.files['screenshot']
        image_bytes = screenshot.read()
        frame = cv2.flip(cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR),1)
        if screenshot:
            processed = f"data:image/jpeg;base64,{base64.b64encode(slots[session].landmarks(frame)).decode('utf-8')}"
            with open('lastFrame.txt', 'w') as file: file.write(processed) # record last frame for debug
            print(f"{slots[session]}")
            return jsonify({
                'status': 'success',
                'message': 'Image processed successfully',
                'image': processed,
                'sentence': f"{slots[session]}"
            })
        else:
            return {'message': 'No screenshot file provided'}, 400
    except Exception as e:
        print(e)
        return {'message': 'Error uploading screenshot: ' + str(e)}, 500
    
@app.route('/clear', methods=['POST'])
def clearText() -> None:
    global slots
    session = request.json['username']
    print("clear",session)
    print(slots)
    slots[session].clear()

@app.route("/toggle_landmarks", methods=['POST'])
def settings() -> None:
    global slots
    session = request.json['session']
    landmarks = request.json['landmarks']
    slots[session].setLandmarks(landmarks)
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    # Extract username and password from the request data
    username = data.get('username')
    password = data.get('password')
    user = database.collections['users'].find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        # print(f"Login Success as user: {user['email']}")
        with ThreadPoolExecutor(max_workers=1) as executor:
            # Submit the functions to the executor for concurrent execution
            future_one = executor.submit(database.syncStripe)
        return jsonify({"message": "Login successful", "username": username, "email": user["email"]})
    return jsonify({"error": "Invalid credentials"}), 400
@app.route("/checkMembership", methods=['POST'])
def checkMembership():
    data = request.get_json()
    # Extract username and password from the request data
    user = data.get('username')
    if (user == None):
        return jsonify({"validity": None})
    validity = database.checkStripeMembership(user)
    # print(data, validity)
    return jsonify({"validity": validity})

@app.route('/ping')
def check_alive():
    return "Alive"
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81, debug=True)