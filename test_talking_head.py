"""
Script de test pour l'API Talking Head
======================================
Teste la génération de vidéos avec une personne parlant.
"""

import json
import base64
from handler_talking_head import handler


def test_with_url():
    """Test avec une image depuis une URL."""
    print("\n" + "="*60)
    print("Test 1: Image depuis URL")
    print("="*60)
    
    event = {
        'input': {
            'image': 'https://example.com/photo.jpg',  # Remplacer par une vraie URL
            'text': 'Bonjour, je suis un avatar virtuel créé avec RunPod.',
            'language': 'fr',
            'voice': 'default'
        },
        'id': 'test-job-1'
    }
    
    print(f"Input: {json.dumps(event['input'], indent=2, ensure_ascii=False)}")
    result = handler(event)
    print(f"\nOutput: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def test_with_base64():
    """Test avec une image en base64."""
    print("\n" + "="*60)
    print("Test 2: Image en base64")
    print("="*60)
    
    # Pour tester avec une vraie image:
    # with open('photo.jpg', 'rb') as f:
    #     image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Simulation pour le test
    image_data = "data:image/jpeg;base64,/9j/4AAQSkZJRg..."  # Base64 tronqué
    
    event = {
        'input': {
            'image': image_data,
            'text': 'Ceci est un test de synthèse vocale et de génération vidéo.',
            'language': 'fr'
        },
        'id': 'test-job-2'
    }
    
    print(f"Input: image=<base64>, text='{event['input']['text']}'")
    result = handler(event)
    print(f"\nOutput: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def test_english():
    """Test avec texte en anglais."""
    print("\n" + "="*60)
    print("Test 3: Texte en anglais")
    print("="*60)
    
    event = {
        'input': {
            'image': 'https://example.com/photo.jpg',
            'text': 'Hello, I am a virtual avatar powered by AI.',
            'language': 'en',
            'voice': 'default'
        },
        'id': 'test-job-3'
    }
    
    print(f"Input: {json.dumps(event['input'], indent=2, ensure_ascii=False)}")
    result = handler(event)
    print(f"\nOutput: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def test_long_text():
    """Test avec un texte long."""
    print("\n" + "="*60)
    print("Test 4: Texte long")
    print("="*60)
    
    long_text = """
    Bienvenue sur cette démonstration de génération de vidéo avec avatar parlant.
    Cette technologie combine la synthèse vocale et l'animation faciale
    pour créer des vidéos personnalisées à partir d'une simple photo.
    Les applications sont nombreuses: e-learning, marketing, accessibilité,
    et bien d'autres domaines encore.
    """
    
    event = {
        'input': {
            'image': 'https://example.com/photo.jpg',
            'text': long_text.strip(),
            'language': 'fr'
        },
        'id': 'test-job-4'
    }
    
    print(f"Input: texte de {len(long_text)} caractères")
    result = handler(event)
    print(f"\nOutput: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    return result


def test_missing_fields():
    """Test avec champs manquants."""
    print("\n" + "="*60)
    print("Test 5: Validation des champs requis")
    print("="*60)
    
    # Test sans image
    event1 = {
        'input': {
            'text': 'Test sans image'
        },
        'id': 'test-job-5a'
    }
    
    print("Test 5a: Sans image")
    result1 = handler(event1)
    print(f"Output: {json.dumps(result1, indent=2, ensure_ascii=False)}")
    assert 'error' in result1, "Devrait retourner une erreur"
    print("✓ Erreur correctement détectée")
    
    # Test sans texte
    event2 = {
        'input': {
            'image': 'https://example.com/photo.jpg'
        },
        'id': 'test-job-5b'
    }
    
    print("\nTest 5b: Sans texte")
    result2 = handler(event2)
    print(f"Output: {json.dumps(result2, indent=2, ensure_ascii=False)}")
    assert 'error' in result2, "Devrait retourner une erreur"
    print("✓ Erreur correctement détectée")


def test_real_image_local():
    """
    Test avec une vraie image locale.
    Créez un fichier 'test_image.jpg' dans le répertoire pour tester.
    """
    print("\n" + "="*60)
    print("Test 6: Image locale (si disponible)")
    print("="*60)
    
    import os
    
    if os.path.exists('test_image.jpg'):
        with open('test_image.jpg', 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        event = {
            'input': {
                'image': f'data:image/jpeg;base64,{image_data}',
                'text': 'Test avec une vraie image locale.',
                'language': 'fr'
            },
            'id': 'test-job-6'
        }
        
        print("Image chargée depuis test_image.jpg")
        result = handler(event)
        print(f"\nOutput: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    else:
        print("ℹ️  Pas de fichier test_image.jpg trouvé. Test ignoré.")
        print("   Pour tester avec une vraie image, ajoutez 'test_image.jpg'")


if __name__ == "__main__":
    print("=" * 60)
    print("Tests de l'API Talking Head - RunPod Serverless")
    print("=" * 60)
    
    try:
        # Tests de base
        test_missing_fields()
        
        # Note: Les tests suivants nécessitent l'implémentation complète
        # du TTS et du modèle talking head
        print("\n" + "="*60)
        print("TESTS COMPLETS (nécessitent TTS et modèle)")
        print("="*60)
        
        # Décommentez quand vous avez configuré TTS et le modèle:
        # test_with_url()
        # test_with_base64()
        # test_english()
        # test_long_text()
        # test_real_image_local()
        
        print("\n" + "="*60)
        print("ℹ️  Pour les tests complets:")
        print("   1. Installez gTTS: pip install gTTS")
        print("   2. Configurez Wav2Lip ou SadTalker")
        print("   3. Décommentez les tests ci-dessus")
        print("="*60)
        
        print("\n✓ Tests de validation terminés avec succès!")
        
    except Exception as e:
        print(f"\n✗ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
