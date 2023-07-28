from flask import jsonify
from app import app, database
from bson.json_util import dumps

@app.route('/translations', methods=['GET'])
def get_translations():
    translations = database.translations.find()
    return jsonify(dumps(translations)), 200
