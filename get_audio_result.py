"""
Récupère et sauvegarde le dernier audio généré
"""
import requests
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

# Test avec runsync pour obtenir immédiatement le résultat
url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "image": "https://picsum.photos/400/600",
        "text": "Bonjour, ceci est un test de la synthèse vocale avec Coqui TTS. La qualité audio est-elle satisfaisante ?",
        "voice": "Claribel Dervla",
        "language": "fr"
    }
}

print("🚀 Test de génération audio avec Coqui TTS...")
print(f"📝 Texte: {payload['input']['text']}")
print(f"🎤 Voix: {payload['input']['voice']}")
print(f"\n⏳ Envoi de la requête...\n")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        output = data.get('output', {})
        
        if 'audio_base64' in output:
            # Décoder et sauvegarder l'audio
            audio_data = base64.b64decode(output['audio_base64'])
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_coqui_{timestamp}.wav"
            
            with open(filename, 'wb') as f:
                f.write(audio_data)
            
            size_kb = len(audio_data) / 1024
            
            print("✅ SUCCÈS!")
            print(f"   📊 Taille: {size_kb:.1f} KB")
            print(f"   🎵 Format: WAV")
            print(f"   🎙️  Engine: {output.get('tts_engine', 'N/A')}")
            print(f"   🗣️  Speaker: {output.get('speaker', 'N/A')}")
            print(f"   💾 Fichier: {filename}")
            print(f"\n💡 Pour écouter: vlc {filename}")
            
        else:
            print(f"❌ Pas d'audio dans la réponse")
            print(f"Réponse: {data}")
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        print(f"Réponse: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
