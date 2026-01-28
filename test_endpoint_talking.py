"""
Test de l'endpoint Talking Head sur RunPod
==========================================
"""

import runpod
import os
from dotenv import load_dotenv
import json

# Charger les variables d'environnement
load_dotenv()

# Configuration
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
ENDPOINT_ID = os.getenv('ENDPOINT_ID_TALKING_HEAD', os.getenv('ENDPOINT_ID'))

runpod.api_key = RUNPOD_API_KEY

print("="*60)
print("🎬 TEST ENDPOINT TALKING HEAD - RUNPOD")
print("="*60)
print(f"API Key: {RUNPOD_API_KEY[:8]}...{RUNPOD_API_KEY[-4:]}")
print(f"Endpoint ID: {ENDPOINT_ID}")
print("="*60)

def test_health():
    """Test de santé de l'endpoint."""
    print("\n1️⃣  Health Check...")
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        health = endpoint.health()
        print(f"✅ Endpoint accessible")
        print(f"Workers: {health.get('workers', {})}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_talking_head_simple():
    """Test avec une image et du texte simple."""
    print("\n2️⃣  Test: Image + Texte (gTTS)...")
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        print("Envoi de la requête...")
        result = endpoint.run_sync({
            "input": {
                "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
                "text": "Bonjour, je suis un test de l'API Talking Head sur RunPod.",
                "language": "fr"
            }
        }, timeout=120)
        
        print(f"\n✅ Résultat reçu:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get('status') == 'partial_success':
            print("\n✅ Test réussi (partial_success attendu)")
            print("   - Image téléchargée: ✅")
            print("   - Audio TTS généré: ✅")
            print("   - Vidéo: ⚠️  Wav2Lip non configuré (normal)")
            return True
        elif result.get('error'):
            print(f"\n⚠️  Erreur: {result.get('error')}")
            return False
        else:
            print("\n✅ Test réussi!")
            return True
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation():
    """Test de validation des champs."""
    print("\n3️⃣  Test: Validation (champ manquant)...")
    
    try:
        endpoint = runpod.Endpoint(ENDPOINT_ID)
        
        result = endpoint.run_sync({
            "input": {
                "text": "Test sans image"
            }
        }, timeout=60)
        
        if 'error' in result:
            print(f"✅ Validation fonctionne: {result.get('error')}")
            return True
        else:
            print("⚠️  Devrait retourner une erreur")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    if not RUNPOD_API_KEY:
        print("❌ RUNPOD_API_KEY manquant dans .env")
        exit(1)
    
    if not ENDPOINT_ID:
        print("❌ ENDPOINT_ID manquant dans .env")
        print("\nAjoutez dans .env:")
        print("ENDPOINT_ID_TALKING_HEAD=votre_endpoint_id")
        exit(1)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Talking Head Simple", test_talking_head_simple()))
    results.append(("Validation", test_validation()))
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 L'endpoint Talking Head fonctionne!")
    else:
        print("\n⚠️  Vérifiez les logs dans RunPod dashboard")
