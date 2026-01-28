"""
Script de test pour vérifier votre serverless RunPod
===================================================
"""

import runpod
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration - À remplir avec vos valeurs
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY', 'VOTRE_CLE_API_ICI')
ENDPOINT_ID = os.getenv('ENDPOINT_ID', 'VOTRE_ENDPOINT_ID_ICI')

# Configurer la clé API
runpod.api_key = RUNPOD_API_KEY


def test_health():
    """Vérifie que l'endpoint est accessible."""
    print("\n" + "="*60)
    print("1️⃣  TEST: Health Check")
    print("="*60)
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        health = endpoint.health()
        print(f"✅ Endpoint accessible")
        print(f"Health status: {health}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_echo():
    """Test l'opération echo."""
    print("\n" + "="*60)
    print("2️⃣  TEST: Opération Echo")
    print("="*60)
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        print("Envoi de la requête...")
        result = endpoint.run_sync({
            "input": {
                "message": "Hello from RunPod!",
                "operation": "echo"
            }
        }, timeout=60)
        
        print(f"✅ Résultat:")
        print(f"   Output: {result.get('output')}")
        print(f"   Operation: {result.get('operation')}")
        
        if result.get('output') == "Hello from RunPod!":
            print("✅ Test réussi!")
            return True
        else:
            print("⚠️  Résultat inattendu")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_uppercase():
    """Test l'opération uppercase."""
    print("\n" + "="*60)
    print("3️⃣  TEST: Opération Uppercase")
    print("="*60)
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        print("Envoi de la requête...")
        result = endpoint.run_sync({
            "input": {
                "message": "runpod serverless",
                "operation": "uppercase"
            }
        }, timeout=60)
        
        print(f"✅ Résultat:")
        print(f"   Input: runpod serverless")
        print(f"   Output: {result.get('output')}")
        
        if result.get('output') == "RUNPOD SERVERLESS":
            print("✅ Test réussi!")
            return True
        else:
            print("⚠️  Résultat inattendu")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_reverse():
    """Test l'opération reverse."""
    print("\n" + "="*60)
    print("4️⃣  TEST: Opération Reverse")
    print("="*60)
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        result = endpoint.run_sync({
            "input": {
                "message": "RunPod",
                "operation": "reverse"
            }
        }, timeout=60)
        
        print(f"✅ Résultat:")
        print(f"   Output: {result.get('output')}")
        
        if result.get('output') == "doPnuR":
            print("✅ Test réussi!")
            return True
        else:
            print("⚠️  Résultat inattendu")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_async():
    """Test une requête asynchrone."""
    print("\n" + "="*60)
    print("5️⃣  TEST: Requête Asynchrone")
    print("="*60)
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        print("Envoi de la requête asynchrone...")
        run_request = endpoint.run({
            "input": {
                "message": "Test async",
                "operation": "length"
            }
        })
        
        job_id = run_request.job_id
        print(f"Job ID: {job_id}")
        
        print("Attente du résultat...")
        import time
        max_attempts = 30
        for attempt in range(max_attempts):
            status = endpoint.status(run_request)
            print(f"  Statut: {status.get('status')} ({attempt+1}/{max_attempts})")
            
            if status.get('status') == 'COMPLETED':
                result = status.get('output')
                print(f"✅ Résultat: {result}")
                print("✅ Test réussi!")
                return True
            elif status.get('status') == 'FAILED':
                print(f"❌ Job échoué: {status.get('error')}")
                return False
            
            time.sleep(2)
        
        print("⚠️  Timeout: le job n'a pas terminé à temps")
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def run_all_tests():
    """Execute tous les tests."""
    print("="*60)
    print("🧪 TESTS DU SERVERLESS RUNPOD")
    print("="*60)
    
    if not RUNPOD_API_KEY or RUNPOD_API_KEY == 'VOTRE_CLE_API_ICI':
        print("\n❌ ERREUR: Configurez vos credentials!")
        print("\nDans le fichier .env, ajoutez:")
        print("RUNPOD_API_KEY=votre_clé_api")
        print("ENDPOINT_ID=votre_endpoint_id")
        print("\nOu modifiez directement ce script.")
        return
    
    if not ENDPOINT_ID or ENDPOINT_ID == 'VOTRE_ENDPOINT_ID_ICI':
        print("\n❌ ERREUR: Endpoint ID manquant!")
        print("Configurez ENDPOINT_ID dans .env ou dans ce script.")
        return
    
    print(f"\n📡 Endpoint ID: {ENDPOINT_ID}")
    print(f"🔑 API Key: {RUNPOD_API_KEY[:8]}...{RUNPOD_API_KEY[-4:]}")
    
    results = []
    
    # Exécuter les tests
    results.append(("Health Check", test_health()))
    results.append(("Echo", test_echo()))
    results.append(("Uppercase", test_uppercase()))
    results.append(("Reverse", test_reverse()))
    results.append(("Async", test_async()))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Résultat: {passed}/{total} tests réussis")
    print("="*60)
    
    if passed == total:
        print("\n🎉 Félicitations! Votre serverless fonctionne parfaitement!")
    elif passed > 0:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les logs dans RunPod.")
    else:
        print("\n❌ Tous les tests ont échoué. Vérifications à faire:")
        print("   1. L'endpoint est-il bien 'Active' dans RunPod?")
        print("   2. La clé API est-elle correcte?")
        print("   3. L'endpoint ID est-il correct?")
        print("   4. Des workers sont-ils actifs?")


if __name__ == "__main__":
    run_all_tests()
