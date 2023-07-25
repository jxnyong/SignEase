from flask import Flask
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

# <-- Database configuration -->
cluster = MongoClient("mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority") # Create a new client and connect to the server

# Select the database
database = cluster["SignEase"]

# Select the collection within the database
collection = database["users"]

# # Send a ping to confirm a successful connection
try:
    cluster.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)