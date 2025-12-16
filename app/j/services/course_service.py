from bson import ObjectId
from datetime import datetime
from config.database import get_database
from config.settings import COLLECTION_COURSES
from app.j.models.course import Course
import logging

logger = logging.getLogger(__name__)

class CourseServiceLogic:
    """Logique métier pour la gestion des cours"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[COLLECTION_COURSES]
    
    def create_course(self, titre, code, description, credits, 
                     enseignant_id, departement, semestre):
        """Créer un nouveau cours"""
        try:
            # Vérifier si le code existe déjà
            if self.collection.find_one({'code': code}):
                return None, "Code de cours déjà existant"
            
            course = Course(
                titre=titre,
                code=code,
                description=description,
                credits=credits,
                enseignant_id=enseignant_id,
                departement=departement,
                semestre=semestre
            )
            
            result = self.collection.insert_one(course.to_dict())
            
            if result.inserted_id:
                created_course = self.collection.find_one({'_id': result.inserted_id})
                return created_course, None
            return None, "Échec de création"
            
        except Exception as e:
            logger.error(f"Erreur create_course: {e}")
            return None, str(e)
    
    def get_course_by_id(self, course_id):
        """Récupérer un cours par ID"""
        try:
            course = self.collection.find_one({'_id': ObjectId(course_id)})
            return course, None if course else "Cours non trouvé"
        except Exception as e:
            logger.error(f"Erreur get_course_by_id: {e}")
            return None, str(e)
    
    def get_course_by_code(self, code):
        """Récupérer un cours par code"""
        try:
            course = self.collection.find_one({'code': code})
            return course, None if course else "Cours non trouvé"
        except Exception as e:
            logger.error(f"Erreur get_course_by_code: {e}")
            return None, str(e)
    
    def get_all_courses(self):
        """Récupérer tous les cours"""
        try:
            courses = list(self.collection.find())
            return courses, None
        except Exception as e:
            logger.error(f"Erreur get_all_courses: {e}")
            return [], str(e)
    
    def update_course(self, course_id, **kwargs):
        """Mettre à jour un cours"""
        try:
            kwargs['date_modification'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(course_id)},
                {'$set': kwargs}
            )
            
            if result.modified_count > 0:
                updated_course = self.collection.find_one({'_id': ObjectId(course_id)})
                return updated_course, None
            return None, "Aucune modification ou cours non trouvé"
            
        except Exception as e:
            logger.error(f"Erreur update_course: {e}")
            return None, str(e)
    
    def delete_course(self, course_id):
        """Supprimer un cours"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(course_id)})
            if result.deleted_count > 0:
                return True, None
            return False, "Cours non trouvé"
        except Exception as e:
            logger.error(f"Erreur delete_course: {e}")
            return False, str(e)
    
    def get_courses_by_department(self, departement):
        """Récupérer les cours par département"""
        try:
            courses = list(self.collection.find({'departement': departement}))
            return courses, None
        except Exception as e:
            logger.error(f"Erreur get_courses_by_department: {e}")
            return [], str(e)