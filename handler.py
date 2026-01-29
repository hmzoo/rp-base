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

# Initialisation globale des modèles (chargés une seule fois)
TTS_MODEL = None
WAV2LIP_MODEL = None

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


def init_wav2lip_model():
    """Initialise le modèle Wav2Lip pour génération vidéo"""
    global WAV2LIP_MODEL
    
    if WAV2LIP_MODEL is None:
        print("\n🎬 Chargement du modèle Wav2Lip...")
        import sys
        sys.path.append('/app/Wav2Lip')
        
        try:
            from models import Wav2Lip as Wav2LipModel
            import mediapipe as mp
            
            checkpoint_path = '/app/Wav2Lip/checkpoints/wav2lip_gan.pth'
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"   📱 Device: {device}")
            
            # Télécharger le modèle s'il n'existe pas
            if not os.path.exists(checkpoint_path):
                print(f"   📥 Téléchargement du modèle Wav2Lip (~145 MB)...")
                import urllib.request
                model_url = 'https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth'
                try:
                    urllib.request.urlretrieve(model_url, checkpoint_path)
                    print(f"   ✅ Modèle téléchargé avec succès")
                except Exception as e:
                    print(f"   ⚠️  Tentative URL alternative...")
                    # URL alternative sur Google Drive ou autre CDN
                    alt_url = 'https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?download=1'
                    urllib.request.urlretrieve(alt_url, checkpoint_path)
                    print(f"   ✅ Modèle téléchargé (URL alternative)")
            
            # Charger le modèle
            print(f"   ⏳ Chargement du checkpoint Wav2Lip...")
            model = Wav2LipModel()
            checkpoint = torch.load(checkpoint_path, map_location=device)
            
            # Charger les poids du modèle
            s = checkpoint["state_dict"]
            new_s = {}
            for k, v in s.items():
                new_s[k.replace('module.', '')] = v
            model.load_state_dict(new_s)
            
            model = model.to(device)
            model.eval()
            
            # Initialiser MediaPipe Face Detection
            mp_face_detection = mp.solutions.face_detection
            face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
            
            WAV2LIP_MODEL = {'model': model, 'device': device, 'face_detector': face_detector}
            print("   ✅ Modèle Wav2Lip chargé avec succès")
            
        except Exception as e:
            print(f"   ❌ ERREUR chargement Wav2Lip: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    return WAV2LIP_MODEL


def generate_talking_head(image_path, audio_path, output_path):
    """
    Génère la vidéo talking head avec Wav2Lip.
    
    Args:
        image_path: Chemin vers l'image
        audio_path: Chemin vers l'audio
        output_path: Chemin de sortie pour la vidéo
    
    Returns:
        str: Chemin vers la vidéo générée
    """
    import sys
    sys.path.append('/app/Wav2Lip')
    
    import cv2
    import numpy as np
    from os import path
    import audio as wav2lip_audio
    import mediapipe as mp
    
    print("   🎬 Initialisation Wav2Lip...")
    
    # Charger le modèle
    wav2lip_data = init_wav2lip_model()
    model = wav2lip_data['model']
    device = wav2lip_data['device']
    face_detector = wav2lip_data['face_detector']
    
    # Paramètres
    mel_step_size = 16
    img_size = 96
    fps = 25
    batch_size = 128
    pads = [0, 10, 0, 0]  # top, bottom, left, right
    
    print("   📸 Détection du visage...")
    
    # Charger l'image
    if not path.isfile(image_path):
        raise ValueError(f'Image non trouvée: {image_path}')
    
    # Créer une vidéo statique à partir de l'image
    frame = cv2.imread(image_path)
    
    if frame is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    # Charger l'audio et calculer les mel spectrograms
    print("   🎵 Traitement de l'audio...")
    wav = wav2lip_audio.load_wav(audio_path, 16000)
    mel = wav2lip_audio.melspectrogram(wav)
    
    # Calculer le nombre de frames nécessaires
    mel_chunks = []
    mel_idx_multiplier = 80. / fps
    i = 0
    while True:
        start_idx = int(i * mel_idx_multiplier)
        if start_idx + mel_step_size > len(mel[0]):
            mel_chunks.append(mel[:, len(mel[0]) - mel_step_size:])
            break
        mel_chunks.append(mel[:, start_idx: start_idx + mel_step_size])
        i += 1
    
    print(f"   📊 Génération de {len(mel_chunks)} frames...")
    
    # Créer les frames de l'image répétées
    full_frames = [frame.copy() for _ in range(len(mel_chunks))]
    
    # Détecter les visages avec MediaPipe
    print("   👤 Détection des visages...")
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb_frame)
    
    if not results.detections:
        raise ValueError("Aucun visage détecté dans l'image")
    
    # Utiliser le premier visage détecté
    detection = results.detections[0]
    bboxC = detection.location_data.relative_bounding_box
    ih, iw, _ = frame.shape
    
    # Convertir les coordonnées relatives en pixels
    x1 = int(bboxC.xmin * iw)
    y1 = int(bboxC.ymin * ih)
    w = int(bboxC.width * iw)
    h = int(bboxC.height * ih)
    x2 = x1 + w
    y2 = y1 + h
    
    # Appliquer les paddings
    y1 = max(0, y1 - pads[0])
    y2 = min(ih, y2 + pads[1])
    x1 = max(0, x1 - pads[2])
    x2 = min(iw, x2 + pads[3])
    
    # Extraire la région du visage
    face_rect = frame[y1:y2, x1:x2]
    
    # Créer face_det_results pour chaque frame (même visage)
    coords = (y1, y2, x1, x2)
    face_det_results = [(face_rect.copy(), coords) for _ in range(len(full_frames))]
    
    print("   🎭 Génération du lip-sync...")
    
    # Générer la vidéo avec lip-sync
    gen = datagen(full_frames.copy(), mel_chunks, face_det_results, img_size, batch_size)
    
    frame_h, frame_w = full_frames[0].shape[:-1]
    out = cv2.VideoWriter(output_path, 
                         cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_w, frame_h))
    
    for i, (img_batch, mel_batch, frames, coords) in enumerate(gen):
        img_batch = torch.FloatTensor(np.transpose(img_batch, (0, 3, 1, 2))).to(device)
        mel_batch = torch.FloatTensor(np.transpose(mel_batch, (0, 3, 1, 2))).to(device)
        
        with torch.no_grad():
            pred = model(mel_batch, img_batch)
        
        pred = pred.cpu().numpy().transpose(0, 2, 3, 1) * 255.
        
        for p, f, c in zip(pred, frames, coords):
            y1, y2, x1, x2 = c
            p = cv2.resize(p.astype(np.uint8), (x2 - x1, y2 - y1))
            f[y1:y2, x1:x2] = p
            out.write(f)
    
    out.release()
    print(f"   ✅ Vidéo générée: {output_path}")
    
    return output_path


def datagen(frames, mels, face_det_results, img_size, batch_size):
    """Générateur de batches pour Wav2Lip"""
    img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []
    
    for i, m in enumerate(mels):
        idx = i % len(frames)
        frame_to_save = frames[idx].copy()
        face, coords = face_det_results[idx].copy()
        
        face = cv2.resize(face, (img_size, img_size))
        
        img_batch.append(face)
        mel_batch.append(m)
        frame_batch.append(frame_to_save)
        coords_batch.append(coords)
        
        if len(img_batch) >= batch_size:
            img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)
            img_batch = (img_batch / 255.) * 2 - 1
            mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], 80, -1])
            
            yield img_batch, mel_batch, frame_batch, coords_batch
            img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []
    
    if len(img_batch) > 0:
        img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)
        img_batch = (img_batch / 255.) * 2 - 1
        mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], 80, -1])
        
        yield img_batch, mel_batch, frame_batch, coords_batch


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
        
        # Encoder l'audio en base64
        with open(audio_path, 'rb') as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
            audio_size = os.path.getsize(audio_path)
        
        print(f"   ✓ Audio encodé: {audio_size} bytes")
        
        # Étape 3: Générer la vidéo talking head avec Wav2Lip
        print("3️⃣ Génération de la vidéo talking head (Wav2Lip)...")
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "output_video.mp4")
        
        try:
            generate_talking_head(image_path, audio_path, output_path)
            print(f"   ✓ Vidéo générée: {output_path}")
            
            # Encoder la vidéo en base64
            with open(output_path, 'rb') as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
                video_size = os.path.getsize(output_path)
            
            print(f"   ✓ Vidéo encodée: {video_size} bytes")
            
            # Nettoyage
            import shutil
            shutil.rmtree(image_temp_dir, ignore_errors=True)
            shutil.rmtree(audio_temp_dir, ignore_errors=True)
            shutil.rmtree(output_dir, ignore_errors=True)
            
            return {
                'success': True,
                'video_base64': video_base64,
                'video_size_bytes': video_size,
                'audio_base64': audio_base64,
                'audio_size_bytes': audio_size,
                'tts_engine': 'Coqui TTS XTTS_v2',
                'video_engine': 'Wav2Lip GAN',
                'speaker': voice,
                'language': language,
                'text_length': len(text),
                'format': 'mp4'
            }
            
        except Exception as video_error:
            # Si erreur Wav2Lip, retourner juste l'audio
            print(f"   ⚠️  Erreur génération vidéo: {video_error}")
            import traceback
            traceback.print_exc()
            
            # Nettoyage
            import shutil
            shutil.rmtree(image_temp_dir, ignore_errors=True)
            shutil.rmtree(audio_temp_dir, ignore_errors=True)
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir, ignore_errors=True)
            
            return {
                'success': False,
                'error': 'Vidéo non générée (voir logs)',
                'error_details': str(video_error),
                'audio_generated': True,
                'audio_base64': audio_base64,
                'audio_size_bytes': audio_size,
                'tts_engine': 'Coqui TTS XTTS_v2',
                'speaker': voice,
                'language': language
            }
        
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
