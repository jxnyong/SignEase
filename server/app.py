from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask_cors import CORS
from mongodb import MongoDB, TABLES

# Flask app setup
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "https://fe36-2406-3003-206f-1b4b-3c6d-9b37-250c-ec3e.ngrok-free.app"]}}, supports_credentials=True)  # Enable CORS

# <-- Database Configurations -->
client = MongoClient("mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority")
database = client["SignEase"]
db2 = MongoDB(*TABLES)

# JWT setup
app.config["JWT_SECRET_KEY"] = "bb123"
jwt = JWTManager(app)

