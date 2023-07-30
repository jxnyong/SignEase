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
        full_name = request.form.get('fullName', '')
        sign_type = request.form.get('signType', '')
        file_description = request.form.get('fileDescription', '')
        upload_preset = request.form.get('upload_preset', '')

        # Upload the file to Cloudinary and obtain the upload result
        upload_result = cloudinary.uploader.upload(
            file,
            upload_preset=upload_preset,
            folder="signease",
            resource_type="auto",)
        # Save the file directly to the database
        file_doc = {
            "filename": file.filename,
            "sign_type": sign_type,
            "content_type": file.content_type,
            "file_description": file_description,
            "full_name": full_name,
            # URL of the uploaded file on Cloudinary
            "url": upload_result['secure_url'],
            # Cloudinary public ID of the file
            "cloudinary_public_id": upload_result['public_id']
        }

        database.dataset.insert_one(file_doc)

        return jsonify({"success": True}), 200

    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')  # This logs the error
        return jsonify({"msg": "Internal Server Error: " + str(e)}), 500
