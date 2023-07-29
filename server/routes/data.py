from flask import request, jsonify
from werkzeug.datastructures import FileStorage
from app import app, database
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dlvjtm893",  # Cloudinary cloud name
    api_key="841663142691876",        # Cloudinary API key
    api_secret="UQ4RPBt1jjxrSe9HVJ6oyLsOa2k"   # Cloudinary API secret
)


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
        upload_preset = request.form.get('upload_preset', 'default_unsigned_preset')

        # Upload the file to Cloudinary and obtain the upload result
        upload_result = cloudinary.uploader.upload(file_data, upload_preset=upload_preset, folder="signease")

        # Save the file directly to the database
        file_doc = {
            "filename": file.filename,
            "file_type": file_type,
            "content_type": file.content_type,
            "file_description": file_description,
            "full_name": full_name,
            "data": file_data,
            # URL of the uploaded file on Cloudinary
            "url": upload_result['secure_url'],
            # Cloudinary public ID of the file
            "cloudinary_public_id": upload_result['public_id']
        }

        database.dataset.insert_one(file_doc)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500
