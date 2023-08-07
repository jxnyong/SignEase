from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from typing import Dict
import asyncio
# from model import HandGestureRecogniser 
from model import mediapipe_detection, draw_landmarks, holistic, actions, extract_keypoints, model as Model
from model.gestures import landmarking
import model.gestures as gestures
import cv2, model, time
import numpy as np
import base64, threading
from mongodb import MongoDB, TABLES
from werkzeug.security import check_password_hash
from concurrent.futures import ThreadPoolExecutor
database = MongoDB(*TABLES)
model.__draw__ = (False, True, True)
# slots:Dict[str, HandGestureRecogniser] = dict()
app = Flask(__name__)
sentence = []
sequence = []
predictions = []
frames = []
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, methods=['POST', 'GET'])
def stringToImage(base64_string: str):
    """Decode the numpy array as an image using OpenCV"""
    return cv2.imdecode(np.frombuffer(base64.b64decode(base64_string.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)
# def predict_action():
#     global predictions, sentence, sequence, frames
#     res = Model.predict(np.expand_dims(sequence, axis=0))[0]
#     print(actions[np.argmax(res)])
#     predictions.append(np.argmax(res))
#     if np.unique(predictions[-10:])[0] == np.argmax(res): #Ensuring there are no wrong prediction during transitions
#         print(f'{res=}')
#         if res[np.argmax(res)] > 0.4:
#             if len(sentence) > 0:
#                 if actions[np.argmax(res)] != sentence[-1]:
#                     sentence.append(actions[np.argmax(res)])
#             else:
#                 sentence.append(actions[np.argmax(res)])
async def predict():
    global sequence
    return Model.predict(np.expand_dims(sequence, axis=0))[0]
async def gather():
    global frames
    tasks = [predict(), gestures.predictions(frames)]
    results = await asyncio.gather(*tasks)
    return results
def predict_action():
    global predictions, sentence
    pred = None
    res, res2 = asyncio.run(gather())
    predictions.append(np.argmax(res))
    predictions = predictions[-10:]
    if res[np.argmax(res)] > 0.4:
        if np.unique(predictions)[0] != np.argmax(res): #inverted from chris
            pred = actions[np.argmax(res)]
    if all(element == res2[0] for element in res2) and res2[0] != 'Blank':
        pred = res2[0]
    if pred:
        if len(sentence) > 0:
            if pred != sentence[-1]:
                sentence.append(pred)
        else:
            sentence.append(pred)

@app.route('/video', methods=['POST'])
def process_video() -> Response:
    global sentence, sequence, frames
    try:
        start = time.perf_counter()
        # if not slots.get(session, False): slots[session] = HandGestureRecogniser()
        screenshot = request.files['screenshot']
        session = request.form.get('name')  # Get the name from the form data
        image_bytes = screenshot.read()
       
        if screenshot:
            frame = cv2.flip(cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR),1)
            frames.append(frame)
            frames = frames[-5:]
            image, results = mediapipe_detection(frame, holistic)
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            print(len(sequence))
            sequence = sequence[-30:]
            if len(sequence) == 30:
                threading.Thread(target=predict_action).start()

            #Drawing landmarks
            draw_landmarks(image, results)

            reti, frame = cv2.imencode(".jpg", image)
            processed = f"data:image/jpeg;base64,{base64.b64encode(frame.tobytes()).decode('utf-8')}"
            # with open('lastFrame.txt', 'w') as file: file.write(processed) # record last frame for debug
            # print(f"{slots[session]}")
            print(f"time elapsed: {time.perf_counter()-start}")
            return jsonify({
                'status': 'success',
                'message': 'Image processed successfully',
                'image': processed,
                'sentence': " ".join(sentence)
            })
        else:
            return {'message': 'No screenshot file provided'}, 400
    except Exception as e:
        print(e)
        return {'message': 'Error uploading screenshot: ' + str(e)}, 500
    
@app.route('/clear', methods=['POST'])
def clearText() -> None:
    global sentence
    sentence.clear()
    return jsonify({"success": True})

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