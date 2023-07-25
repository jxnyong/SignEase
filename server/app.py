from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS

# <-- Database Configurations -->
client = MongoClient("mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority")
database = client["SignEase"]

# JWT setup
app.config["JWT_SECRET_KEY"] = "bb123"
jwt = JWTManager(app)
