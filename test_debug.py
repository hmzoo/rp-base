#!/usr/bin/env python3
"""Test avec logs détaillés"""
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
        'text': 'Test.',
        'voice': 'Claribel Dervla',
        'language': 'fr'
    }
}

print('🧪 Test debug...\n')

response = requests.post(url, json=payload, headers=headers, timeout=120)
result = response.json()

# Afficher toute la réponse
print(json.dumps(result, indent=2))
