# Service de Gestion de Cours - SOAP

Service SOAP pour la gestion des cours dans un système SOA universitaire.

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurer les variables d'environnement dans .env

3. Lancer le serveur:
```bash
python server.py
```

## Endpoints SOAP

- WSDL: http://localhost:8001/?wsdl
- Service: http://localhost:8001

## Opérations disponibles

- create_course
- get_course_by_id
- get_course_by_code
- get_all_courses
- delete_course

## Structure de données Course

- titre: string
- code: string (ex: INFO101)
- description: string
- credits: integer
- enseignant_id: string
- departement: string
- semestre: string