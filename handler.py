"""
RunPod Serverless - Talking Head API with Coqui TTS
===================================================
Génère une vidéo où une personne sur une image "lit" un texte.
Utilise Coqui TTS XTTS_v2 pour une qualité audio professionnelle.

Input:
    - image: URL ou base64 de l'image de la personne
    - text: Le texte à faire lire
    - voice: (optionnel) Nom du speaker ou fichier audio pour clonage
    - language: (optionnel) Langue du texte (default: 'fr')

Output:
    - audio_base64: Audio encodé en base64
    - audio_size_bytes: Taille de l'audio
"""

import runpod
import base64
import os
import tempfile
import requests
from pathlib import Path
import json
import torch
import sys
import subprocess

print(f"🚀 Démarrage du worker RunPod")
print(f"🐍 Python version: {sys.version}")
print(f"📍 Working directory: {os.getcwd()}")

# Vérifier les dépendances système
print(f"\n📦 Vérification des dépendances système...")
try:
    result = subprocess.run(['espeak-ng', '--version'], capture_output=True, text=True)
    print(f"✅ espeak-ng installé")
except Exception as e:
    print(f"⚠️ espeak-ng: {e}")

try:
    import soundfile
    print(f"✅ soundfile (libsndfile1) v{soundfile.__version__}")
except Exception as e:
    print(f"⚠️ soundfile: {e}")

print(f"\n📦 Import TTS...")
try:
    from TTS.api import TTS
    print("✅ TTS importé avec succès")
except Exception as e:
    print(f"❌ ERREUR import TTS: {e}")
    import traceback
    traceback.print_exc()
    raise

# Initialisation globale du modèle TTS (chargé une seule fois)
TTS_MODEL = None

def init_tts_model():
    """Initialise le modèle Coqui TTS XTTS_v2"""
    global TTS_MODEL
    
    if TTS_MODEL is None:
        print("\n🔄 Chargement du modèle Coqui TTS XTTS_v2...")
        from TTS.api import TTS
        
        # Vérifier si GPU disponible
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   📱 Device: {device}")
        if torch.cuda.is_available():
            print(f"   🎮 GPU: {torch.cuda.get_device_name(0)}")
            print(f"   💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        try:
            # Charger le modèle multilingue XTTS_v2
            print(f"   ⏳ Téléchargement/chargement du modèle (~2GB)...")
            TTS_MODEL = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            print("   ✅ Modèle chargé avec succès")
        except Exception as e:
            print(f"   ❌ ERREUR chargement modèle: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    return TTS_MODEL


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


def text_to_speech(text, language='fr', voice='Claribel Dervla'):
    """
    Convertit le texte en audio avec Coqui TTS XTTS_v2.
    
    Speakers disponibles par défaut:
    - Claribel Dervla (féminin, clair)
    - Daisy Studious (féminin, posé)
    - Gracie Wise (féminin, mature)
    - Tammie Ema (féminin, jeune)
    - Alison Dietlinde (féminin, professionnel)
    - Ana Florence (féminin, chaleureux)
    - Annmarie Nele (féminin, énergique)
    - Asya Anara (féminin, doux)
    - Brenda Stern (féminin, autoritaire)
    - Gitta Nikolina (féminin, amical)
    - Henriette Usha (féminin, calme)
    - Sofia Hellen (féminin, élégant)
    - Tammy Grit (féminin, dynamique)
    - Tanja Adelina (féminin, confiant)
    - Vjollca Johnnie (féminin, expressif)
    - Andrew Chipper (masculin, jeune)
    - Badr Odhiambo (masculin, grave)
    - Dionisio Schuyler (masculin, mature)
    - Royston Min (masculin, calme)
    - Viktor Eka (masculin, autoritaire)
    - Abrahan Mack (masculin, chaleureux)
    - Adde Michal (masculin, amical)
    - Baldur Sanjin (masculin, puissant)
    - Craig Gutsy (masculin, énergique)
    - Damien Black (masculin, sérieux)
    - Gilberto Mathias (masculin, professionnel)
    - Ilkin Urbano (masculin, confiant)
    - Kazuhiko Atallah (masculin, posé)
    - Ludvig Milivoj (masculin, doux)
    - Suad Qasim (masculin, expressif)
    
    Clonage de voix:
    - Passez l'URL ou le chemin d'un fichier audio de 3-10 secondes
    
    Args:
        text: Le texte à synthétiser
        language: Code langue (fr, en, es, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko, hi)
        voice: Nom du speaker ou URL/chemin audio pour clonage
    
    Returns:
        tuple: (audio_path, temp_dir)
    """
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "speech.wav")
    
    # Initialiser le modèle
    tts = init_tts_model()
    
    print(f"   🎤 Synthèse Coqui TTS: langue={language}, speaker={voice}")
    
    try:
        # Vérifier si c'est un clonage de voix (URL ou fichier)
        if voice.startswith('http://') or voice.startswith('https://') or os.path.isfile(voice):
            print(f"   🎭 Clonage de voix depuis: {voice}")
            # Télécharger l'audio de référence si c'est une URL
            if voice.startswith('http'):
                ref_audio = os.path.join(temp_dir, "reference_voice.wav")
                response = requests.get(voice)
                with open(ref_audio, 'wb') as f:
                    f.write(response.content)
                voice = ref_audio
            
            # Générer avec clonage
            tts.tts_to_file(
                text=text,
                speaker_wav=voice,
                language=language,
                file_path=audio_path
            )
        else:
            # Utiliser un speaker par défaut
            tts.tts_to_file(
                text=text,
                speaker=voice,
                language=language,
                file_path=audio_path
            )
        
        print(f"   ✓ Audio généré: {audio_path}")
        return audio_path, temp_dir
        
    except Exception as e:
        print(f"   ⚠️  Erreur TTS: {e}")
        # Fallback sur un speaker par défaut
        print(f"   🔄 Tentative avec speaker par défaut...")
        tts.tts_to_file(
            text=text,
            speaker="Claribel Dervla",
            language=language,
            file_path=audio_path
        )
        return audio_path, temp_dir


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
    return f"file://{video_path}"


def handler(event):
    """
    Handler principal pour l'API Talking Head avec Coqui TTS.
    
    Args:
        event: Événement RunPod contenant:
            - input.image: URL ou base64 de l'image
            - input.text: Texte à faire lire
            - input.voice: (optionnel) Speaker ou URL audio pour clonage (default: 'Claribel Dervla')
            - input.language: (optionnel) Langue (default: 'fr')
    
    Returns:
        dict: Résultat avec audio_base64 et métadonnées
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
        voice = job_input.get('voice', 'Claribel Dervla')
        
        print(f"📥 Traitement: texte='{text[:50]}...', langue={language}, voix={voice}")
        
        # Étape 1: Télécharger/décoder l'image
        print("1️⃣ Téléchargement de l'image...")
        image_path, image_temp_dir = download_image(image_input)
        print(f"   ✓ Image sauvegardée: {image_path}")
        
        # Étape 2: Générer l'audio (TTS)
        print("2️⃣ Génération de l'audio (Coqui TTS XTTS_v2)...")
        audio_path, audio_temp_dir = text_to_speech(text, language, voice)
        
        # Encoder l'audio en base64 pour le retour
        with open(audio_path, 'rb') as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
            audio_size = os.path.getsize(audio_path)
        
        print(f"   ✓ Audio encodé: {audio_size} bytes")
        
        # Pour l'instant, on retourne juste l'audio (talking head à implémenter)
        # Nettoyage
        import shutil
        shutil.rmtree(image_temp_dir, ignore_errors=True)
        shutil.rmtree(audio_temp_dir, ignore_errors=True)
        
        return {
            'success': True,
            'audio_base64': audio_base64,
            'audio_size_bytes': audio_size,
            'tts_engine': 'Coqui TTS XTTS_v2',
            'speaker': voice,
            'language': language,
            'text_length': len(text),
            'note': 'Audio généré avec succès. Génération vidéo à implémenter (Wav2Lip/SadTalker).'
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
        
    except Exception as e:
        import traceback
        print(f"❌ ERREUR: {e}")
        traceback.print_exc()
        return {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }


if __name__ == "__main__":
    # Mode développement: test local
    print("🚀 Démarrage du worker RunPod - Talking Head API (Coqui TTS)")
    print("=" * 60)
    
    # Démarrer le worker
    runpod.serverless.start({"handler": handler})
