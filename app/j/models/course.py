from datetime import datetime
from bson import ObjectId

class Course:
    """Modèle pour un cours"""
    
    def __init__(self, titre, code, description, credits, 
                 enseignant_id, departement, semestre, 
                 _id=None, date_creation=None, date_modification=None):
        self._id = _id or ObjectId()
        self.titre = titre
        self.code = code
        self.description = description
        self.credits = credits
        self.enseignant_id = enseignant_id
        self.departement = departement
        self.semestre = semestre
        self.date_creation = date_creation or datetime.utcnow()
        self.date_modification = date_modification or datetime.utcnow()
    
    def to_dict(self):
        """Convertir en dictionnaire pour MongoDB"""
        return {
            '_id': self._id,
            'titre': self.titre,
            'code': self.code,
            'description': self.description,
            'credits': self.credits,
            'enseignant_id': self.enseignant_id,
            'departement': self.departement,
            'semestre': self.semestre,
            'date_creation': self.date_creation,
            'date_modification': self.date_modification
        }
    
    @staticmethod
    def from_dict(data):
        """Créer un objet Course depuis un dictionnaire"""
        return Course(
            _id=data.get('_id'),
            titre=data.get('titre'),
            code=data.get('code'),
            description=data.get('description'),
            credits=data.get('credits'),
            enseignant_id=data.get('enseignant_id'),
            departement=data.get('departement'),
            semestre=data.get('semestre'),
            date_creation=data.get('date_creation'),
            date_modification=data.get('date_modification')
        )