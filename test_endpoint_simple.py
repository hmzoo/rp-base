"""
Test simple de l'endpoint Coqui TTS
"""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def test_health():
    """Test si l'endpoint répond"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/health"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print(f"🔍 Test de santé de l'endpoint...")
    print(f"   URL: {url}\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📄 Réponse: {response.text}\n")
        
        if response.status_code == 200:
            print("✅ Endpoint opérationnel!")
            return True
        else:
            print("⚠️ Endpoint non disponible")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout - l'endpoint ne répond pas")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_run():
    """Teste l'endpoint avec une requête simple"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://picsum.photos/400/600",
            "text": "Ceci est un test rapide de Coqui TTS.",
            "language": "fr"
        }
    }
    
    print(f"\n🚀 Envoi d'une requête de test...")
    print(f"   URL: {url}")
    print(f"   Texte: {payload['input']['text']}\n")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        print(f"📊 Statut HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Requête acceptée!")
            print(f"📝 Job ID: {data.get('id', 'N/A')}")
            print(f"⏱️  Status: {data.get('status', 'N/A')}")
            
            if data.get('status') == 'IN_QUEUE':
                print(f"\n⏳ Job en queue, attente du résultat...")
                return check_status(data.get('id'))
            elif data.get('status') == 'IN_PROGRESS':
                print(f"\n🔄 Job en cours d'exécution...")
                return check_status(data.get('id'))
            else:
                print(f"\n📄 Réponse complète: {data}")
                
        else:
            print(f"❌ Erreur: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout après 120s")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def check_status(job_id, max_wait=90):
    """Vérifie le statut d'un job"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'UNKNOWN')
                
                print(f"   Status: {status} ({int(time.time() - start_time)}s)")
                
                if status == 'COMPLETED':
                    print(f"\n✅ Job terminé!")
                    output = data.get('output', {})
                    if 'audio_size_bytes' in output:
                        print(f"   Audio généré: {output['audio_size_bytes']} bytes")
                    return True
                    
                elif status == 'FAILED':
                    print(f"\n❌ Job échoué!")
                    print(f"   Erreur: {data.get('error', 'Unknown')}")
                    return False
                    
                elif status in ['IN_QUEUE', 'IN_PROGRESS']:
                    time.sleep(5)
                    continue
                    
        except Exception as e:
            print(f"   Erreur check: {e}")
            
        time.sleep(5)
    
    print(f"\n⏱️ Timeout après {max_wait}s")
    return False

if __name__ == "__main__":
    print("="*70)
    print("🧪 Test de l'endpoint Coqui TTS")
    print("="*70)
    
    # Test de santé
    if test_health():
        # Test d'exécution
        test_run()
    else:
        print("\n💡 L'endpoint est probablement en cours de build.")
        print("   Retentez dans quelques minutes.")
