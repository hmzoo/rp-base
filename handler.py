"""
RunPod Serverless - Talking Head API
====================================
Génère une vidéo où une personne sur une image "lit" un texte.

Input:
    - image: URL ou base64 de l'image de la personne
    - text: Le texte à faire lire
    - voice: (optionnel) Type de voix pour la synthèse vocale
    - language: (optionnel) Langue du texte (default: 'fr')

Output:
    - video_url: URL de la vidéo générée
    - duration: Durée de la vidéo en secondes
"""

import runpod
import base64
import os
import tempfile
import requests
from pathlib import Path
import json


def download_image(image_input):
    """
    Télécharge ou décode l'image d'entrée.
    
    Args:
        image_input: URL ou base64 de l'image
    
    Returns:
        str: Chemin vers le fichier image temporaire
    """
    temp_dir = tempfile.mkdtemp()
    image_path = os.path.join(temp_dir, "input_image.jpg")
    
    if image_input.startswith('http://') or image_input.startswith('https://'):
        # Télécharger depuis URL
        response = requests.get(image_input)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            f.write(response.content)
    elif image_input.startswith('data:image'):
        # Décoder base64
        header, encoded = image_input.split(',', 1)
        image_data = base64.b64decode(encoded)
        with open(image_path, 'wb') as f:
            f.write(image_data)
    else:
        # Assumer que c'est du base64 sans header
        image_data = base64.b64decode(image_input)
        with open(image_path, 'wb') as f:
            f.write(image_data)
    
    return image_path, temp_dir


def text_to_speech(text, language='fr', voice='default'):
    """
    Convertit le texte en audio (TTS).
    
    Pour une implémentation complète, utilisez:
    - ElevenLabs API
    - Google Cloud TTS
    - Azure TTS
    - Coqui TTS (open source)
    
    Args:
        text: Le texte à synthétiser
        language: Langue du texte
        voice: Type de voix
    
    Returns:
        str: Chemin vers le fichier audio
    """
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "speech.wav")
    
    # TODO: Implémenter avec un vrai service TTS
    # Exemple avec gTTS (simple mais qualité basique):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_path)
        return audio_path, temp_dir
    except ImportError:
        # Fallback: créer un fichier audio vide pour le développement
        print("⚠️  gTTS non installé. Créez un vrai audio avec un service TTS.")
        # Retourner None pour indiquer qu'il faut implémenter un vrai TTS
        raise NotImplementedError(
            "Vous devez installer gTTS ou utiliser un service TTS: "
            "pip install gTTS"
        )


def generate_talking_head(image_path, audio_path, output_path):
    """
    Génère la vidéo talking head.
    
    Pour une implémentation complète, utilisez:
    - Wav2Lip: https://github.com/Rudrabha/Wav2Lip
    - SadTalker: https://github.com/OpenTalker/SadTalker
    - D-ID API (commercial)
    
    Args:
        image_path: Chemin vers l'image
        audio_path: Chemin vers l'audio
        output_path: Chemin de sortie pour la vidéo
    
    Returns:
        str: Chemin vers la vidéo générée
    """
    
    # TODO: Implémenter avec Wav2Lip ou SadTalker
    # Exemple avec Wav2Lip:
    """
    import cv2
    from wav2lip import Wav2Lip
    
    model = Wav2Lip()
    video = model.generate(
        face_path=image_path,
        audio_path=audio_path,
        outfile=output_path
    )
    """
    
    # Pour le développement: simuler la génération
    raise NotImplementedError(
        "Implémentation de Wav2Lip/SadTalker requise. "
        "Voir les instructions dans le README_TALKING_HEAD.md"
    )


def upload_to_storage(video_path):
    """
    Upload la vidéo vers un stockage (S3, etc.).
    
    Args:
        video_path: Chemin local de la vidéo
    
    Returns:
        str: URL publique de la vidéo
    """
    # TODO: Implémenter l'upload vers S3 ou autre
    # Exemple avec boto3:
    """
    import boto3
    s3 = boto3.client('s3')
    bucket_name = 'your-bucket'
    key = f'videos/{os.path.basename(video_path)}'
    
    s3.upload_file(video_path, bucket_name, key)
    url = f'https://{bucket_name}.s3.amazonaws.com/{key}'
    return url
    """
    
    # Pour le développement: retourner un chemin local
    return f"file://{video_path}"


def handler(event):
    """
    Handler principal pour l'API Talking Head.
    
    Args:
        event: Événement RunPod contenant:
            - input.image: URL ou base64 de l'image
            - input.text: Texte à faire lire
            - input.voice: (optionnel) Type de voix
            - input.language: (optionnel) Langue (default: 'fr')
    
    Returns:
        dict: Résultat avec video_url et métadonnées
    """
    try:
        job_input = event.get('input', {})
        
        # Validation des entrées
        if 'image' not in job_input:
            return {'error': 'Le champ "image" est requis (URL ou base64)'}
        
        if 'text' not in job_input:
            return {'error': 'Le champ "text" est requis'}
        
        image_input = job_input['image']
        text = job_input['text']
        language = job_input.get('language', 'fr')
        voice = job_input.get('voice', 'default')
        
        print(f"📥 Traitement: texte='{text[:50]}...', langue={language}")
        
        # Étape 1: Télécharger/décoder l'image
        print("1️⃣ Téléchargement de l'image...")
        image_path, image_temp_dir = download_image(image_input)
        print(f"   ✓ Image sauvegardée: {image_path}")
        
        # Étape 2: Générer l'audio (TTS)
        print("2️⃣ Génération de l'audio (TTS)...")
        try:
            audio_path, audio_temp_dir = text_to_speech(text, language, voice)
            print(f"   ✓ Audio généré: {audio_path}")
            
            # Encoder l'audio en base64 pour le retour
            with open(audio_path, 'rb') as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
                audio_size = os.path.getsize(audio_path)
            
        except NotImplementedError as e:
            return {
                'error': 'TTS non configuré',
                'message': str(e),
                'todo': 'Installer gTTS ou configurer un service TTS professionnel'
            }
        
        # Étape 3: Générer la vidéo talking head
        print("3️⃣ Génération de la vidéo talking head...")
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "output_video.mp4")
        
        try:
            generate_talking_head(image_path, audio_path, output_path)
            print(f"   ✓ Vidéo générée: {output_path}")
        except NotImplementedError as e:
            return {
                'error': 'Modèle talking head non configuré',
                'message': str(e),
                'todo': 'Implémenter Wav2Lip ou SadTalker (voir README)',
                'status': 'partial_success',
                'audio_generated': True,
                'audio_base64': audio_base64,
                'audio_size_bytes': audio_size,
                'image_processed': True
            }
        
        # Étape 4: Upload de la vidéo
        print("4️⃣ Upload de la vidéo...")
        video_url = upload_to_storage(output_path)
        print(f"   ✓ Vidéo disponible: {video_url}")
        
        # Nettoyage
        import shutil
        shutil.rmtree(image_temp_dir, ignore_errors=True)
        shutil.rmtree(audio_temp_dir, ignore_errors=True)
        shutil.rmtree(output_dir, ignore_errors=True)
        
        # Résultat
        return {
            'status': 'success',
            'video_url': video_url,
            'text': text,
            'language': language,
            'duration': None,  # TODO: calculer la durée réelle
            'message': 'Vidéo générée avec succès'
        }
        
    except Exception as e:
        import traceback
        return {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }


if __name__ == "__main__":
    # Mode développement: test local
    print("🚀 Démarrage du worker RunPod - Talking Head API")
    print("=" * 60)
    
    # Démarrer le worker
    runpod.serverless.start({"handler": handler})
