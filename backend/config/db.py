import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_URI)
db = client['ing360_db']

def get_db():
    return db
