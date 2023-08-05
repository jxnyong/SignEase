from flask import render_template, request, redirect
import requests
from app import app

# @app.route('/')
# def index():
#     return render_template('RequestLang.tsx')

@app.route('/process', methods=['POST', 'GET'])
def process():
    email = request.form.get('email')
    language = request.form.get('language')
    
    # For example, print them to the console:
    print(f'Email: {email}, Language: {language}')
    sender_data = {
        "email":email,
        "language": language
    }
    try:
        receiver_url = "http://localhost:5001/receive"  # Change this URL to match your receiver's endpoint

        response = requests.post(receiver_url, json=sender_data)
    except requests.exceptions.ConnectionError as e:
        print(e)
    # return "Data successfully"
    return redirect("http://localhost:5173/")
    # f"Email: {email}, Language: {language}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
