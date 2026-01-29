"""
Test de téléchargement d'audio depuis l'API RunPod
"""
import os
import base64
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
ENDPOINT_ID = os.getenv('ENDPOINT_ID')

def test_audio_download():
    """Test de génération et téléchargement d'audio"""
    
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            "text": "Bonjour ! Je teste la génération d'audio avec RunPod.",
            "language": "fr"
        }
    }
    
    print("🚀 Envoi de la requête à RunPod...")
    print(f"Endpoint: {ENDPOINT_ID}")
    
    response = requests.post(url, json=payload, headers=headers, timeout=120)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Réponse reçue!")
        print(f"Status: {result.get('status')}")
        
        output = result.get('output', {})
        
        if 'audio_base64' in output:
            # Décoder et sauvegarder l'audio
            audio_data = base64.b64decode(output['audio_base64'])
            output_file = "downloaded_audio.wav"
            
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"\n🎵 Audio téléchargé: {output_file}")
            print(f"Taille: {len(audio_data)} octets ({output.get('audio_size_bytes')} bytes attendus)")
            print(f"\n🎧 Écoutez avec: mpv {output_file}")
        else:
            print("\n⚠️  Pas d'audio dans la réponse")
            print("Output:", output)
    else:
        print(f"\n❌ Erreur {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_audio_download()
