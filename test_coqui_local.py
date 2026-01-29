"""
Test local de Coqui TTS pour debug
"""
import sys
print(f"Python version: {sys.version}")

try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA version: {torch.version.cuda}")
except Exception as e:
    print(f"❌ PyTorch error: {e}")

try:
    from TTS.api import TTS
    print("✅ Coqui TTS importé")
    
    # Test du modèle
    print("\n🔄 Chargement du modèle XTTS_v2...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    print("✅ Modèle chargé")
    
    # Test de génération
    import tempfile
    import os
    
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "test.wav")
    
    print("\n🎤 Test de synthèse...")
    tts.tts_to_file(
        text="Bonjour, ceci est un test de Coqui TTS.",
        speaker="Claribel Dervla",
        language="fr",
        file_path=output_path
    )
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"✅ Audio généré: {output_path} ({size} bytes)")
    else:
        print("❌ Fichier audio non créé")
        
except Exception as e:
    print(f"❌ Erreur TTS: {e}")
    import traceback
    traceback.print_exc()
