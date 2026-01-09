import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_PORT = os.environ.get("DB_PORT") or 27017
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SEEDLIST_CONNECTION_FORMAT = os.environ.get("USE_SEEDLIST_CONNECTION_FORMAT") or False

if SEEDLIST_CONNECTION_FORMAT and SEEDLIST_CONNECTION_FORMAT.lower() != "false":
    MONGODB_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
else:
    if DB_USER and DB_PASSWORD:
        MONGODB_URI = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    else:
        MONGODB_URI = f"mongodb://{DB_HOST}:{DB_PORT}/"

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ismaster')
    # Use the requested database name
    db = client["projectdatabase"]
    projects_collection = db["projects"]
    print("MongoDB connection successful")
except Exception as e:
    print(f"Warning: MongoDB connection failed: {e}")
    print("Running in mock mode - no data will persist")
    # Create a mock collection for development
    class MockCollection:
        def __init__(self):
            # If a DB connection cannot be made, this mock collection will be empty.
            self.data = []
        
        def find(self, query, projection=None):
            return self.data
        
        def count_documents(self, query):
            return len(self.data)
        
        def insert_many(self, docs):
            self.data.extend(docs)
    
    projects_collection = MockCollection()
    db = None

# No automatic seeding of dummy data. Use the real MongoDB `projectdatabase` contents.
