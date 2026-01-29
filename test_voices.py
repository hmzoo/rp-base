"""
Test des différentes voix disponibles avec gTTS
"""
from gtts import gTTS
import os

def test_voice(text, language, voice_name, tld, slow=False):
    """Génère un audio avec une voix spécifique"""
    filename = f"voice_{voice_name}.mp3"
    print(f"🎤 Génération: {voice_name} (lang={language}, tld={tld}, slow={slow})")
    
    tts = gTTS(text=text, lang=language, slow=slow, tld=tld)
    tts.save(filename)
    
    size = os.path.getsize(filename)
    print(f"   ✓ {filename} ({size} bytes)")
    return filename

def main():
    text_fr = "Bonjour, je suis une voix synthétique en français."
    text_en = "Hello, I am a synthetic voice in English."
    
    print("=" * 60)
    print("Test des voix françaises")
    print("=" * 60)
    
    # Voix françaises
    test_voice(text_fr, 'fr', 'france', 'fr')
    test_voice(text_fr, 'fr', 'canada', 'ca')
    test_voice(text_fr, 'fr', 'france_slow', 'fr', slow=True)
    
    print("\n" + "=" * 60)
    print("Test des voix anglaises")
    print("=" * 60)
    
    # Voix anglaises
    test_voice(text_en, 'en', 'us', 'com')
    test_voice(text_en, 'en', 'uk', 'co.uk')
    test_voice(text_en, 'en', 'australia', 'com.au')
    test_voice(text_en, 'en', 'india', 'co.in')
    test_voice(text_en, 'en', 'us_slow', 'com', slow=True)
    
    print("\n" + "=" * 60)
    print("Fichiers générés:")
    print("=" * 60)
    for f in sorted(os.listdir('.')):
        if f.startswith('voice_') and f.endswith('.mp3'):
            size = os.path.getsize(f)
            print(f"  {f:<25} {size:>8} bytes")
    
    print("\n💡 Écoutez les voix avec: mpv voice_*.mp3")
    print("\n📝 Pour utiliser dans l'API:")
    print('   {"voice": "uk"}      → voix britannique')
    print('   {"voice": "france"}  → voix française')
    print('   {"voice": "us_slow"} → voix US lente')

if __name__ == "__main__":
    main()
