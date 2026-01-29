#!/usr/bin/env python3
"""Test simple avec URL d'image"""
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

url = f'https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

payload = {
    'input': {
        'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=512&h=512&fit=crop',
        'text': 'Bonjour, ceci est un test rapide.',
        'voice': 'Claribel Dervla',
        'language': 'fr'
    }
}

print('🧪 Test avec URL d\'image...')
print(f'Image: {payload["input"]["image"]}')
print(f'Texte: {payload["input"]["text"]}\n')

try:
    response = requests.post(url, json=payload, headers=headers, timeout=120)
    print(f'Status HTTP: {response.status_code}\n')
    
    result = response.json()
    
    if 'output' in result:
        output = result['output']
        print('✅ Réponse reçue:')
        print(f'  success: {output.get("success")}')
        print(f'  tts_engine: {output.get("tts_engine")}')
        print(f'  video_engine: {output.get("video_engine", "N/A")}')
        print(f'  audio_size: {output.get("audio_size_bytes", 0)} bytes')
        print(f'  video_size: {output.get("video_size_bytes", 0)} bytes')
        
        if output.get('error'):
            print(f'\n❌ Erreur: {output.get("error")}')
            print(f'  Détails: {output.get("error_details", "N/A")}')
    else:
        print('❌ Pas de output dans la réponse')
        print(json.dumps(result, indent=2)[:1000])
        
except Exception as e:
    print(f'❌ Exception: {e}')
