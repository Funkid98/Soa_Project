import os
from dotenv import load_dotenv

load_dotenv()

# Configuration MongoDB (accepte MONGO_URI ou MONGODB_URI)
MONGO_URI = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI', 'mongodb+srv://...')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'soa_databases')
COLLECTION_COURSES = 'courses'

# Configuration Serveur
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8001))