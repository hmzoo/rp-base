"""
Test rapide sans attente
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "image": "https://picsum.photos/400/600",
        "text": "Test rapide de Coqui TTS.",
        "language": "fr"
    }
}

print("🚀 Test rapide...")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        output = data.get('output', {})
        
        if 'audio_base64' in output:
            size_kb = output['audio_size_bytes'] / 1024
            print(f"✅ SUCCÈS!")
            print(f"   Audio: {size_kb:.1f} KB")
            print(f"   Engine: {output.get('tts_engine', 'N/A')}")
            print(f"   Speaker: {output.get('speaker', 'N/A')}")
        elif 'error' in output:
            print(f"❌ Erreur: {output['error']}")
        else:
            print(f"⚠️  Réponse inattendue: {data}")
    else:
        print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
