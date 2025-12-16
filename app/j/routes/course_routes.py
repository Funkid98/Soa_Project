from spyne import ServiceBase, rpc, Unicode, Integer, Iterable, ComplexModel
from app.j.services.course_service import CourseServiceLogic
import json

# Définition du modèle complexe pour les réponses
class CourseResponse(ComplexModel):
    success = Unicode
    message = Unicode
    data = Unicode

class CourseService(ServiceBase):
    """Service SOAP pour la gestion des cours"""
    
    def __init__(self):
        super().__init__()
        self.service = CourseServiceLogic()
    
    @rpc(Unicode, Unicode, Unicode, Integer, Unicode, Unicode, Unicode, 
         _returns=CourseResponse)
    def create_course(ctx, titre, code, description, credits, 
                     enseignant_id, departement, semestre):
        """Créer un nouveau cours"""
        service = CourseServiceLogic()
        course, error = service.create_course(
            titre, code, description, credits,
            enseignant_id, departement, semestre
        )
        
        if course:
            course['_id'] = str(course['_id'])
            course['date_creation'] = str(course['date_creation'])
            course['date_modification'] = str(course['date_modification'])
            
            return CourseResponse(
                success='true',
                message='Cours créé avec succès',
                data=json.dumps(course)
            )
        else:
            return CourseResponse(
                success='false',
                message=error,
                data=''
            )
    
    @rpc(Unicode, _returns=CourseResponse)
    def get_course_by_id(ctx, course_id):
        """Récupérer un cours par ID"""
        service = CourseServiceLogic()
        course, error = service.get_course_by_id(course_id)
        
        if course:
            course['_id'] = str(course['_id'])
            course['date_creation'] = str(course['date_creation'])
            course['date_modification'] = str(course['date_modification'])
            
            return CourseResponse(
                success='true',
                message='Cours trouvé',
                data=json.dumps(course)
            )
        else:
            return CourseResponse(
                success='false',
                message=error,
                data=''
            )
    
    @rpc(Unicode, _returns=CourseResponse)
    def get_course_by_code(ctx, code):
        """Récupérer un cours par code"""
        service = CourseServiceLogic()
        course, error = service.get_course_by_code(code)
        
        if course:
            course['_id'] = str(course['_id'])
            course['date_creation'] = str(course['date_creation'])
            course['date_modification'] = str(course['date_modification'])
            
            return CourseResponse(
                success='true',
                message='Cours trouvé',
                data=json.dumps(course)
            )
        else:
            return CourseResponse(
                success='false',
                message=error,
                data=''
            )
    
    @rpc(_returns=CourseResponse)
    def get_all_courses(ctx):
        """Récupérer tous les cours"""
        service = CourseServiceLogic()
        courses, error = service.get_all_courses()
        
        if not error:
            for course in courses:
                course['_id'] = str(course['_id'])
                course['date_creation'] = str(course['date_creation'])
                course['date_modification'] = str(course['date_modification'])
            
            return CourseResponse(
                success='true',
                message=f'{len(courses)} cours trouvés',
                data=json.dumps(courses)
            )
        else:
            return CourseResponse(
                success='false',
                message=error,
                data='[]'
            )
    
    @rpc(Unicode, _returns=CourseResponse)
    def delete_course(ctx, course_id):
        """Supprimer un cours"""
        service = CourseServiceLogic()
        success, error = service.delete_course(course_id)
        
        if success:
            return CourseResponse(
                success='true',
                message='Cours supprimé avec succès',
                data=''
            )
        else:
            return CourseResponse(
                success='false',
                message=error,
                data=''
            )