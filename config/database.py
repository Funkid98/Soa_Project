from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config.settings import MONGO_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Établir la connexion à MongoDB"""
        if self._client is None:
            try:
                self._client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
                self._db = self._client[DATABASE_NAME]
                logger.info("Connexion MongoDB établie")
            except Exception as e:
                logger.error(f"Erreur de connexion MongoDB: {e}")
                raise
        return self._db
    
    def get_db(self):
        """Obtenir l'instance de la base de données"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Fermer la connexion"""
        if self._client:
            self._client.close()
            logger.info("Connexion MongoDB fermée")

# Instance globale
db_instance = Database()

def get_database():
    """Fonction helper pour obtenir la DB"""
    return db_instance.get_db()

def test_connection():
    """Tester la connexion MongoDB"""
    try:
        db = get_database()
        db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Test de connexion échoué: {e}")
        return False