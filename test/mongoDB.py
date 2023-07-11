import pymongo
from pymongo import MongoClient
import datetime

# Your connection string
cluster = MongoClient("mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority")

# Select the database
database = cluster["SignEase"]

# Select the collection within the database
collection = database["users"]

# This is your document to insert into the users collection
user = {
    "userId": "user1",
    "firstName": "John",
    "lastName": "Doe",
    "email": "johndoe@example.com",
    "passwordHash": "plaintextpassword",  
    "createdAt": datetime.datetime.utcnow(),
    "updatedAt": datetime.datetime.utcnow()
}

post1 = {
        "userId": "2",
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "janesmith@example.com",
        "passwordHash": "plaintextpassword2",  # This should be a hashed password in production!
        "createdAt": datetime.datetime.utcnow(),
        "updatedAt": datetime.datetime.utcnow()
}

post2 = {
    "userId": "3",
    "firstName": "Bob",
    "lastName": "Johnson",
    "email": "bobjohnson@example.com",
    "passwordHash": "plaintextpassword3",  # This should be a hashed password in production!
    "createdAt": datetime.datetime.utcnow(),
    "updatedAt": datetime.datetime.utcnow()
}

# Insert the document into the collection
# collection.insert_one(user)

# #Insert multiple documents into the collection
# collection.insert_many([post1, post2])

results = collection.find({"userId":"3"})

for result in results:
    print(result)

# uri = "mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)