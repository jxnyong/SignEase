from flask import render_template, request, redirect, jsonify
import requests, json
from app import app, db2

# @app.route('/')
# def index():
#     return render_template('RequestLang.tsx')
CONFIG_FILE = 'langConfig.json'
@app.route('/process', methods=['POST', 'GET'])
def process():
    email = request.json.get('email')
    language = request.json.get('language')
    
    # For example, print them to the console:
    print(f'Email: {email}, Language: {language}')
    sender_data = {
        "email":email,
        "language": language
    }
    receiver_url = db2.getAliveHost(email)
    if receiver_url == None:
        raise IndexError("No email found")
    try:
        receiver_url = f"{receiver_url}/receive"  # Change this URL to match your receiver's endpoint
        response = requests.post(receiver_url, json=sender_data)
    except requests.exceptions.ConnectionError as e:
        print(e)
    # return "Data successfully"
    return jsonify({"success": True}),200
    # f"Email: {email}, Language: {language}"
@app.route('/setLink',  methods=['POST'])
def setLink():
    """
curl -X POST -F "email=andrewlinyongsheng@gmail.com" -F "link=https://cabf-175-156-152-50.ngrok-free.app" http://localhost:5000/setLink
    """
    email = request.form.get('email')
    link = request.form.get('link')
    db2.updateAliveHosts(email, link)
    return jsonify({"email": email, "link":link})
@app.route('/refreshStripe',  methods=['GET'])
def refreshStripe():
    db2.syncStripe()
    return jsonify({"success": True}),200
if __name__ == '__main__':
    app.run(debug=True, port=5000)
