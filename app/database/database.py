from pymongo import MongoClient

MONGO_URL = "mongodb+srv://smitppatel0712_db_user:oh9u6BYfMIGNOsbW@cluster0.cw23chq.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)

db = client["campusDB"]