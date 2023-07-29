from flask import request, jsonify
from werkzeug.datastructures import FileStorage
from app import app, database
from bson.objectid import ObjectId

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']

    # Here's where we're using FileStorage
    if not isinstance(file, FileStorage):
        return jsonify({"msg": "The uploaded file is not a valid FileStorage instance"}), 400

    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    try:
        file_data = file.read()  # Read the file contents as bytes
        full_name = request.form.get('fullName', '')
        file_type = request.form.get('fileType', '')
        file_description = request.form.get('fileDescription', '')

        # Save the file directly to the database
        file_doc = {
            "filename": file.filename,
            "file_type": file_type,
            "content_type": file.content_type,
            "file_description": file_description,
            "full_name": full_name,
            "data": file_data,
        }

        database.dataset.insert_one(file_doc)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500
