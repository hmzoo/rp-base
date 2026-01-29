"""
Test du temps de réponse de l'API RunPod
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
ENDPOINT_ID = os.getenv('ENDPOINT_ID')

def test_api_with_timing(text, voice='default', language='fr'):
    """Test l'API et mesure le temps de réponse"""
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            "text": text,
            "voice": voice,
            "language": language
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Test: voice={voice}, language={language}")
    print(f"Texte: {text[:50]}...")
    print(f"{'='*60}")
    
    # Mesure du temps
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n⏱️  Temps de réponse: {elapsed_time:.2f} secondes")
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            output = result.get('output', {})
            
            print(f"✅ Status: {status}")
            
            if 'audio_base64' in output:
                audio_size = output.get('audio_size_bytes', 0)
                print(f"🎵 Audio généré: {audio_size} bytes ({audio_size/1024:.1f} KB)")
            
            if 'error' in output:
                print(f"⚠️  Message: {output.get('message', output.get('error'))}")
            
            return {
                'success': True,
                'elapsed_time': elapsed_time,
                'status': status,
                'audio_size': output.get('audio_size_bytes', 0)
            }
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(response.text[:200])
            return {
                'success': False,
                'elapsed_time': elapsed_time,
                'error': response.status_code
            }
            
    except requests.exceptions.Timeout:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"⏱️  Timeout après {elapsed_time:.2f} secondes")
        return {'success': False, 'elapsed_time': elapsed_time, 'error': 'timeout'}
    
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"❌ Erreur: {e}")
        return {'success': False, 'elapsed_time': elapsed_time, 'error': str(e)}

def main():
    print("\n🚀 Test de performance de l'API RunPod")
    print(f"Endpoint: {ENDPOINT_ID}")
    
    tests = [
        {
            'text': "Bonjour, je teste le temps de réponse de l'API.",
            'voice': 'france',
            'language': 'fr'
        },
        {
            'text': "Hello, I am testing the API response time.",
            'voice': 'uk',
            'language': 'en'
        },
        {
            'text': "Voici un texte un peu plus long pour tester le temps de génération audio avec une phrase plus conséquente.",
            'voice': 'canada',
            'language': 'fr'
        }
    ]
    
    results = []
    
    for i, test_params in enumerate(tests, 1):
        print(f"\n\n{'#'*60}")
        print(f"Test {i}/{len(tests)}")
        print(f"{'#'*60}")
        
        result = test_api_with_timing(**test_params)
        results.append(result)
        
        # Pause entre les tests
        if i < len(tests):
            print("\n⏳ Pause de 2 secondes...")
            time.sleep(2)
    
    # Résumé
    print(f"\n\n{'='*60}")
    print("📊 RÉSUMÉ DES PERFORMANCES")
    print(f"{'='*60}")
    
    successful_tests = [r for r in results if r['success']]
    
    if successful_tests:
        times = [r['elapsed_time'] for r in successful_tests]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n✅ Tests réussis: {len(successful_tests)}/{len(results)}")
        print(f"\n⏱️  Temps de réponse:")
        print(f"   • Moyen:  {avg_time:.2f}s")
        print(f"   • Min:    {min_time:.2f}s")
        print(f"   • Max:    {max_time:.2f}s")
        
        total_audio = sum(r.get('audio_size', 0) for r in successful_tests)
        print(f"\n🎵 Audio total généré: {total_audio/1024:.1f} KB")
    else:
        print("\n❌ Aucun test réussi")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
