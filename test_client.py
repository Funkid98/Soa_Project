from zeep import Client
import json

# Connexion au service SOAP
wsdl_url = 'http://localhost:8001/?wsdl'
client = Client(wsdl=wsdl_url)

print("=" * 60)
print("🧪 TEST DU SERVICE SOAP - GESTION DE COURS")
print("=" * 60)

# Test 1: Créer un cours
print("\n1️⃣ TEST: Créer un nouveau cours")
print("-" * 60)
try:
    result = client.service.create_course(
        titre="Introduction à Python",
        code="INFO101",
        description="Cours d'introduction à la programmation Python",
        credits=3,
        enseignant_id="ENS001",
        departement="Informatique",
        semestre="1"
    )
    print(f"✅ Succès: {result.success}")
    print(f"📝 Message: {result.message}")
    if result.data:
        course_data = json.loads(result.data)
        print(f"🆔 ID du cours: {course_data['_id']}")
        print(f"📚 Titre: {course_data['titre']}")
        print(f"🔢 Code: {course_data['code']}")
        COURSE_ID = course_data['_id']  # Sauvegarder l'ID pour les tests suivants
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 2: Créer un deuxième cours
print("\n2️⃣ TEST: Créer un deuxième cours")
print("-" * 60)
try:
    result = client.service.create_course(
        titre="Structures de Données",
        code="INFO201",
        description="Cours sur les structures de données avancées",
        credits=4,
        enseignant_id="ENS002",
        departement="Informatique",
        semestre="2"
    )
    print(f"✅ Succès: {result.success}")
    print(f"📝 Message: {result.message}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 3: Récupérer tous les cours
print("\n3️⃣ TEST: Récupérer tous les cours")
print("-" * 60)
try:
    result = client.service.get_all_courses()
    print(f"✅ Succès: {result.success}")
    print(f"📝 Message: {result.message}")
    if result.data:
        courses = json.loads(result.data)
        print(f"📊 Nombre de cours trouvés: {len(courses)}")
        for course in courses:
            print(f"  - {course['code']}: {course['titre']} ({course['credits']} crédits)")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 4: Récupérer un cours par code
print("\n4️⃣ TEST: Récupérer un cours par code (INFO101)")
print("-" * 60)
try:
    result = client.service.get_course_by_code(code="INFO101")
    print(f"✅ Succès: {result.success}")
    print(f"📝 Message: {result.message}")
    if result.data:
        course = json.loads(result.data)
        print(f"📚 Titre: {course['titre']}")
        print(f"👨‍🏫 Enseignant ID: {course['enseignant_id']}")
        print(f"🏢 Département: {course['departement']}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 5: Essayer de créer un cours avec un code existant
print("\n5️⃣ TEST: Créer un cours avec un code déjà existant (doit échouer)")
print("-" * 60)
try:
    result = client.service.create_course(
        titre="Test Duplication",
        code="INFO101",  # Code déjà utilisé
        description="Ce cours ne devrait pas être créé",
        credits=3,
        enseignant_id="ENS999",
        departement="Test",
        semestre="1"
    )
    print(f"⚠️ Succès: {result.success}")
    print(f"📝 Message: {result.message}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 60)
print("✅ TESTS TERMINÉS")
print("=" * 60)