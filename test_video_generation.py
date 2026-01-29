"""
Test de génération vidéo avec Wav2Lip
"""
import requests
import os
import base64
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def test_video_generation():
    """Teste la génération vidéo complète"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Charger l'image locale, la redimensionner et l'encoder en base64
    image_path = "/home/mrpink/perso/rp-base/medias/originale.png"
    img = Image.open(image_path)
    
    # Redimensionner à 512x512 pour Wav2Lip (recommandé)
    img = img.convert('RGB')
    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
    
    # Convertir en base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    image_data = buffer.getvalue()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        "input": {
            "image": f"data:image/jpeg;base64,{image_base64}",
            "text": "Bonjour, je suis un avatar parlant créé avec Wav2Lip et Coqui TTS. Cette vidéo démontre la synchronisation labiale en temps réel.",
            "voice": "Claribel Dervla",
            "language": "fr"
        }
    }
    
    print("="*70)
    print("🎬 TEST DE GÉNÉRATION VIDÉO WAV2LIP")
    print("="*70)
    print(f"\n📝 Texte: {payload['input']['text']}")
    print(f"🎤 Voix: {payload['input']['voice']}")
    print(f"🖼️  Image: medias/originale.png ({len(image_data)} bytes)")
    print(f"\n⏳ Envoi de la requête (peut prendre 30-60s)...\n")
    
    start = datetime.now()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            data = response.json()
            output = data.get('output', {})
            
            if output.get('success') and 'video_base64' in output:
                # Décoder et sauvegarder la vidéo
                video_data = base64.b64decode(output['video_base64'])
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_filename = f"video_wav2lip_{timestamp}.mp4"
                
                with open(video_filename, 'wb') as f:
                    f.write(video_data)
                
                # Sauvegarder aussi l'audio
                if 'audio_base64' in output:
                    audio_data = base64.b64decode(output['audio_base64'])
                    audio_filename = f"audio_coqui_{timestamp}.wav"
                    with open(audio_filename, 'wb') as f:
                        f.write(audio_data)
                    audio_size_kb = len(audio_data) / 1024
                else:
                    audio_filename = "N/A"
                    audio_size_kb = output.get('audio_size_bytes', 0) / 1024
                
                video_size_mb = len(video_data) / (1024 * 1024)
                
                print("✅ SUCCÈS!")
                print(f"\n📊 RÉSULTATS:")
                print(f"   ⏱️  Temps total: {elapsed:.1f}s")
                print(f"   🎬 Vidéo: {video_size_mb:.2f} MB → {video_filename}")
                print(f"   🎵 Audio: {audio_size_kb:.1f} KB → {audio_filename}")
                print(f"   🎙️  TTS Engine: {output.get('tts_engine', 'N/A')}")
                print(f"   🎭 Video Engine: {output.get('video_engine', 'N/A')}")
                print(f"   🗣️  Speaker: {output.get('speaker', 'N/A')}")
                print(f"\n💡 Pour voir la vidéo: vlc {video_filename}")
                print(f"💡 Pour écouter l'audio: aplay {audio_filename}")
                
                return True
                
            elif output.get('audio_generated'):
                print("⚠️  Vidéo non générée, mais audio disponible")
                print(f"   Erreur: {output.get('error', 'Unknown')}")
                print(f"   Détails: {output.get('error_details', 'N/A')}")
                
                # Sauvegarder l'audio quand même
                if 'audio_base64' in output:
                    audio_data = base64.b64decode(output['audio_base64'])
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"audio_fallback_{timestamp}.wav"
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    print(f"   💾 Audio sauvegardé: {filename}")
                
                return False
                
            else:
                print(f"❌ Erreur dans la réponse: {output}")
                return False
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout après 180s")
        print(f"💡 Le build initial peut prendre plus de temps (téléchargement modèles)")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_video_generation()
    
    print(f"\n{'='*70}")
    if success:
        print("🎉 Test réussi - Vidéo générée avec succès!")
    else:
        print("⚠️  Test échoué - Vérifiez les logs RunPod")
    print(f"{'='*70}\n")
