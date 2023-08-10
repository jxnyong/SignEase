from pymongo.mongo_client import MongoClient
from datetime import datetime
import stripe
from datetime import datetime
from dateutil.relativedelta import relativedelta
TABLES =["session", "translations", "users", 'membership', 'transactions', 'aliveHosts']
stripe.api_key = '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'
def get_checkout_history():
    try:
        sessions = stripe.checkout.Session.list(limit=10)
        return sessions.data  # List of Checkout Sessions
    except stripe.error.StripeError as e:
        # Handle any errors that may occur
        print(f"Error: {e}")
        return []
def datetimePlus(months:int=1, datetime=datetime.now()):
    return datetime + relativedelta(months=months)
def checkoutHistory():
    return [
        {   'sessionId': session.id,
            'Amount': session.amount_total,
            'Date': session.created,
            'email': session.customer_details.email
            } for session in get_checkout_history() if session.customer_details
    ]
CLIENT = "mongodb+srv://mongoAdmin:Exxurn9zbT5vERbH@maincluster.vrqckh2.mongodb.net/?retryWrites=true&w=majority"
class MongoDB:
    def __init__(self,*collections,client:str = CLIENT,database:str="SignEase") -> None:
        self._client = MongoClient(client)
        self._database = self._client[database]
        self.collections = {collection:self._database[collection] for collection in self._database.list_collection_names() if isinstance(collection,str)}
    def insert_one(self, collection:str, data:dict):
        return self.collections[collection].insert_one(data) 
    def get_user_by_field(self, field: str, fieldname:str="username"):
        return self.collections["users"].find_one({fieldname: field})
    def syncStripeTransactions(self, checkoutHistory:list = checkoutHistory()):
        for item in checkoutHistory:
            # Check if the item with the given sessionId already exists in the collection
            if self.collections["transactions"].find_one({"sessionId": item["sessionId"]}) is None:
                # If not, insert the item into the collection
                self.collections["transactions"].insert_one(item)
                print("Inserted:", item)
    def syncMembership(self):
        #Query the "transactions" collection and sort by "Date" in descending order for each unique "email"
        pipeline = [
            {"$sort": {"Date": -1}},
            {"$group": {
                "_id": "$email",
                "latest_transaction": {"$first": "$$ROOT"}
            }}
        ]
        latest_transactions = list(self.collections["transactions"].aggregate(pipeline)) #expensive in bigger tables
        #Loop through the results and update the "membership" collection if needed
        for transaction in latest_transactions:
            email = transaction["_id"]
            latest_transaction_id = transaction["latest_transaction"]["sessionId"]
            # latest_transaction_date = datetime.fromtimestamp(transaction["latest_transaction"]["Date"])
            # Query the "membership" collection to find the matching document with the same email
            membership_doc = self.collections["membership"].find_one({"email": email})
            if membership_doc:
                # Compare the latest sessionId with the transactionId from "membership" collection
                if membership_doc["transactionID"] != latest_transaction_id:
                    # Update the document in the "membership" collection with the new transactionId
                    expiration_date = membership_doc["expirationDate"]
                    months=round(transaction["latest_transaction"]["Amount"]/50,0)
                    self.collections["membership"].update_one(
                        {"_id": membership_doc["_id"]},
                        {"$set": {"transactionID": latest_transaction_id}}
                    )
                    self.collections["expirationDate"].update_one(
                        {"_id": membership_doc["_id"]},
                        {"$set": {"expirationDate": datetimePlus(months,expiration_date)}}
                    )
            else:
                # If no matching membership document found, add a new row for this email
                data = {
                    "email": email,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "expirationDate": datetimePlus(round(transaction["latest_transaction"]["Amount"]/50,0)),
                    "transactionID": latest_transaction_id
                }
                self.collections["membership"].insert_one(data)
    def syncStripe(self):
        self.syncMembership()
        self.syncStripeTransactions()
    def checkStripeMembership(self,user,sync:bool=False) -> bool: 
        if sync:
            self.syncStripe()
        user = self.get_user_by_field(user)
        if not user: return False
        member = self.collections["membership"].find_one({"email": user['email']})
        if member:
            if datetime.now() > member['expirationDate']: return False
            return True
        return False
    def updateAliveHosts(self, email:str, newLink:str):
        if "aliveHosts" not in self._database.list_collection_names():
            raise NotImplementedError("aliveHosts collection does not exist")
        self.collections["aliveHosts"].update_one(
            {"email": email},
            {"$set": {"link": newLink}},
        )
    def getAliveHost(self, email:str):
        if "aliveHosts" not in self._database.list_collection_names():
            raise NotImplementedError("aliveHosts collection does not exist")
        return self.collections["aliveHosts"].find_one({"email": email}).get('link', None)
    @property
    def database(self):
        return self._database
    @property
    def get_collections(self):
        return self.collections
    
if __name__ == "__main__":
    db = MongoDB()
    data = {
        "email": "andrewlinyongsheng@gmail.com",
        "link" : "https://cabf-175-156-152-50.ngrok-free.app",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
    }
    db.updateAliveHosts("andrewlinyongsheng@gmail.com", 'hello!')
    # db.insert_one('aliveHosts', data)
    # db.syncStripeTransactions()
    # db.syncMembership()
    # print(db.checkStripeMembership('sam'))