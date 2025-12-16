from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap.soap11 import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from app.j.routes.course_routes import CourseService
from config.database import test_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Créer l'application SOAP"""
    application = Application(
        [CourseService],
        tns='soa.course.service',
        in_protocol=Soap11(),
        out_protocol=Soap11()
    )
    
    return WsgiApplication(application)

if __name__ == '__main__':
    # Test de la connexion MongoDB
    if test_connection():
        logger.info("Connexion MongoDB réussie!")
        
        # Créer et lancer le serveur SOAP
        app = create_app()
        server = make_server('0.0.0.0', 8001, app)
        
        logger.info("Serveur SOAP démarré sur http://0.0.0.0:8001")
        logger.info("WSDL disponible sur http://0.0.0.0:8001/?wsdl")
        
        server.serve_forever()
    else:
        logger.error("Échec de connexion à MongoDB!")