"""
Test de génération audio avec sauvegarde
"""

from gtts import gTTS
import os

# Texte à synthétiser
text = "Bonjour ! Je suis une intelligence artificielle qui parle français. Cette démo utilise la technologie de synthèse vocale Google Text-to-Speech."

# Générer l'audio
print("🎤 Génération de l'audio...")
tts = gTTS(text=text, lang='fr', slow=False)

# Sauvegarder
output_file = "test_audio_output.mp3"
tts.save(output_file)

print(f"✅ Audio sauvegardé: {output_file}")
print(f"📂 Chemin complet: {os.path.abspath(output_file)}")
print(f"\n🎧 Écoutez le fichier avec: mpv {output_file}")
print(f"   ou ouvrez-le dans votre explorateur de fichiers")
