from flask import jsonify, request
from app import app, database
from bson.json_util import dumps

@app.route('/translations', methods=['GET'])
def get_translations():
    username = request.args.get('username', default=None, type=str)  # get the username query param
    if username is not None:
        translations = database.translations.find({ 'username': username })  # filter translations by username
    else:
        translations = database.translations.find()
    return jsonify(dumps(translations)), 200
