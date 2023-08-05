from flask import Flask, redirect, request, jsonify
import requests
import json

app = Flask(__name__)



@app.route('/receive', methods=['POST'])
def access_lang():
    data = request.json  # This assumes the data is sent as JSON in the request body

    email = data.get('email')
    language = data.get('language')
    print(f"{language=}")

    #change the path
    with open('langConfig.json', 'r') as f:
        langdata = json.load(f)
    langdata["Setting"]["outputLanguage"] = language

    # Save the updated configuration back to the JSON file
    with open('langConfig.json', 'w') as f:
        json.dump(langdata, f, indent=4)

    return jsonify({'email': email, 'language': language })
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)

# @app.route('/trigger-request')
# def trigger_request():
#     print("GET REQUEST")
#     return redirect('/')

# ngrok_url = "https://afa6-203-127-47-48.ngrok-free.app"
    
    # # Make a GET request to the first Flask app
    # response = requests.get(f"{ngrok_url}/process")
    
    # # Process the response or do something with it
    # print(response.text)
    # return f"{response.text}"