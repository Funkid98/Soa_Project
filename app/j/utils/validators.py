import re

def validate_course_code(code):
    """Valider le format du code de cours"""
    pattern = r'^[A-Z]{2,4}[0-9]{3,4}$'
    return re.match(pattern, code) is not None

def validate_credits(credits):
    """Valider le nombre de crédits"""
    return isinstance(credits, int) and 1 <= credits <= 12

def validate_semestre(semestre):
    """Valider le semestre"""
    valid_semestres = ['1', '2', '3', '4', '5', '6', '7', '8']
    return semestre in valid_semestres