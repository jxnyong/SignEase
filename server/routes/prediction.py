from flask import request, jsonify, session
from app import app
import cv2, base64, numpy
from models.gesture import predict
from models.langTranslate import translate_text
from models import predict_action
LANGUAGE_CODE = {
    'english': 'En',
    'chinese': 'Zh',
    'japanese': 'Ja'
}
def stringToImage(base64_string: str):
    """Decode the numpy array as an image using OpenCV"""
    return cv2.imdecode(numpy.frombuffer(base64.b64decode(base64_string.split(',')[1]), numpy.uint8), cv2.IMREAD_COLOR)
@app.route('/gesture', methods=['POST'])
def predict_gesture_():
    image = request.json.get("image", None)
    if image:
        return jsonify({'sentence': predict(stringToImage(image))}) #letters have no translation
    return jsonify({"msg": "Missing image"}),400

@app.route('/action', methods=['POST'])
def predict_action_():
    images = request.json.get("images", None)
    language = request.json.get("language", "english")
    if images:
        action = predict_action([stringToImage(image) for image in images])
        if language != "english":
            return jsonify({'sentence': translate_text(action, LANGUAGE_CODE[language])}) 
        return jsonify({'sentence': action}) 
    return jsonify({"msg": "Missing images"}),400
    

