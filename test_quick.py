"""
Test rapide de l'API Talking Head avec gTTS
"""

from handler import handler
import json

# Test avec URL d'image
event = {
    'input': {
        'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
        'text': 'Bonjour, ceci est un test de synthèse vocale.',
        'language': 'fr'
    },
    'id': 'test-quick'
}

print("Test de l'API Talking Head")
print("="*60)
print(f"Image: {event['input']['image'][:50]}...")
print(f"Texte: {event['input']['text']}")
print("="*60)

result = handler(event)
print("\nRésultat:")
print(json.dumps(result, indent=2, ensure_ascii=False))
