"""
Test de l'API avec Coqui TTS XTTS_v2
"""
import os
import time
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
ENDPOINT_ID = os.getenv('ENDPOINT_ID')

def test_coqui_tts(speaker="Claribel Dervla"):
    """Test l'API avec Coqui TTS"""
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            "text": "Bonjour, je suis généré avec Coqui TTS XTTS version deux. Ma voix devrait être beaucoup plus naturelle et réaliste.",
            "voice": speaker,
            "language": "fr"
        }
    }
    
    print(f"\n{'='*60}")
    print(f"🎤 Test Coqui TTS XTTS_v2")
    print(f"Speaker: {speaker}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        print("\n⏳ Envoi de la requête (peut prendre 20-30s au premier appel)...")
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        
        elapsed = time.time() - start_time
        print(f"⏱️  Temps de réponse: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            output = result.get('output', {})
            
            print(f"\n✅ Status: {status}")
            print(f"TTS Engine: {output.get('tts_engine', 'N/A')}")
            print(f"Speaker: {output.get('speaker', 'N/A')}")
            
            if 'audio_base64' in output:
                # Sauvegarder l'audio
                audio_data = base64.b64decode(output['audio_base64'])
                filename = f"coqui_tts_{speaker.replace(' ', '_').lower()}.wav"
                
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                
                size_kb = len(audio_data) / 1024
                print(f"\n🎵 Audio sauvegardé: {filename}")
                print(f"Taille: {size_kb:.1f} KB")
                print(f"\n🎧 Écoutez avec: mpv {filename}")
                
                return True, elapsed, filename
            else:
                print(f"\n⚠️  Erreur: {output.get('error', 'Pas d\'audio dans la réponse')}")
                if 'traceback' in output:
                    print(f"\nTraceback:\n{output['traceback']}")
                return False, elapsed, None
        else:
            print(f"\n❌ Erreur HTTP {response.status_code}")
            print(response.text[:500])
            return False, elapsed, None
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"\n⏱️  Timeout après {elapsed:.2f}s")
        return False, elapsed, None
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Erreur: {e}")
        return False, elapsed, None

def main():
    print("\n🚀 Test de l'API avec Coqui TTS XTTS_v2")
    print(f"Endpoint: {ENDPOINT_ID}")
    print("\n⚠️  Note: Le premier appel peut prendre 20-30s (chargement du modèle 2GB)")
    print("     Les appels suivants seront plus rapides (2-5s)")
    
    # Test différents speakers
    speakers = [
        "Claribel Dervla",  # Féminin, clair
        "Andrew Chipper",    # Masculin, jeune
        "Damien Black"       # Masculin, sérieux
    ]
    
    results = []
    
    for i, speaker in enumerate(speakers, 1):
        print(f"\n\n{'#'*60}")
        print(f"Test {i}/{len(speakers)}")
        print(f"{'#'*60}")
        
        success, elapsed, filename = test_coqui_tts(speaker)
        results.append({
            'speaker': speaker,
            'success': success,
            'elapsed': elapsed,
            'filename': filename
        })
        
        if i < len(speakers) and success:
            print("\n⏳ Pause de 3 secondes...")
            time.sleep(3)
    
    # Résumé
    print(f"\n\n{'='*60}")
    print("📊 RÉSUMÉ")
    print(f"{'='*60}")
    
    successful = [r for r in results if r['success']]
    
    if successful:
        print(f"\n✅ Tests réussis: {len(successful)}/{len(results)}")
        
        times = [r['elapsed'] for r in successful]
        print(f"\n⏱️  Temps de réponse:")
        print(f"   • Moyen: {sum(times)/len(times):.2f}s")
        print(f"   • Min:   {min(times):.2f}s")
        print(f"   • Max:   {max(times):.2f}s")
        
        print(f"\n🎵 Fichiers audio générés:")
        for r in successful:
            if r['filename']:
                print(f"   • {r['filename']} ({r['speaker']})")
        
        print(f"\n💡 Comparez la qualité avec gTTS:")
        print(f"   mpv coqui_tts_*.wav")
    else:
        print("\n❌ Aucun test réussi")
        print("\n🔍 Vérifiez:")
        print("   1. Le rollout est complet (5/5 workers)")
        print("   2. L'image Docker s'est bien construite avec CUDA")
        print("   3. Les logs RunPod pour plus de détails")

if __name__ == "__main__":
    main()
