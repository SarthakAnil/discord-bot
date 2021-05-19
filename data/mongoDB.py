from dotenv import load_dotenv
import pymongo
import os

load_dotenv()
mongoClient = pymongo.MongoClient(f"mongodb+srv://{os.getenv('user')}:{os.getenv('pass')}@{os.getenv('cluster_db')}")
db = mongoClient.Ghost_Bot
dbCollection = db.guild_properties