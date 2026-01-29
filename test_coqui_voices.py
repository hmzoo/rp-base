"""
Test de Coqui TTS avec plusieurs voix
"""
import requests
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

# Liste de speakers à tester
SPEAKERS = [
    "Claribel Dervla",
    "Damien Black", 
    "Andrew Chipper",
    "Badr Odhiambo",
    "Dionisio Schuyler"
]

def test_voice(speaker, text, output_file):
    """Teste une voix spécifique"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://picsum.photos/400/600",
            "text": text,
            "voice": speaker,
            "language": "fr"
        }
    }
    
    print(f"\n{'='*60}")
    print(f"🎤 Speaker: {speaker}")
    print(f"📝 Texte: {text}")
    
    start = datetime.now()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=90)
        
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            data = response.json()
            output = data.get('output', {})
            
            if 'audio_base64' in output:
                # Sauvegarder l'audio
                audio_data = base64.b64decode(output['audio_base64'])
                with open(output_file, 'wb') as f:
                    f.write(audio_data)
                
                size_kb = output['audio_size_bytes'] / 1024
                print(f"   ✅ Audio: {size_kb:.1f} KB")
                print(f"   ⏱️  Temps: {elapsed:.2f}s")
                print(f"   💾 Fichier: {output_file}")
                return True
            else:
                print(f"   ❌ Pas d'audio: {data}")
                return False
        else:
            print(f"   ❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST DE DIFFÉRENTES VOIX COQUI TTS")
    print("="*60)
    
    text = "Bonjour, je teste la synthèse vocale avec Coqui TTS. La qualité est-elle meilleure qu'avec gTTS ?"
    
    os.makedirs("audio_tests_coqui", exist_ok=True)
    
    success_count = 0
    
    for i, speaker in enumerate(SPEAKERS, 1):
        output_file = f"audio_tests_coqui/voice_{i}_{speaker.replace(' ', '_')}.wav"
        
        if test_voice(speaker, text, output_file):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RÉSULTATS")
    print(f"{'='*60}")
    print(f"✅ Réussis: {success_count}/{len(SPEAKERS)}")
    print(f"\n💡 Écoutez les fichiers dans le dossier audio_tests_coqui/")
