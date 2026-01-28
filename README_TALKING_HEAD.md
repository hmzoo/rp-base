# API Talking Head - RunPod Serverless

Génère des vidéos où une personne sur une image "lit" un texte fourni (avatar parlant / digital human).

## 🎯 Fonctionnalité

**Input:**
- Une image (photo d'une personne)
- Un texte à faire lire

**Output:**
- Une vidéo où la personne "lit" le texte avec mouvements de bouche synchronisés

## 📋 Architecture

```
Image + Texte
    ↓
1. Text-to-Speech (TTS) → Audio
    ↓
2. Wav2Lip/SadTalker → Vidéo avec lip-sync
    ↓
3. Upload S3 → URL publique
```

## 🚀 Installation rapide

### Option 1: Version simple avec gTTS

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances de base
pip install gTTS requests Pillow

# Tester
python test_talking_head.py
```

### Option 2: Version complète avec Wav2Lip (GPU requis)

```bash
# 1. Cloner Wav2Lip
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip

# 2. Télécharger le modèle pré-entraîné
wget 'https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth' -O 'models/wav2lip_gan.pth'

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Retourner au projet
cd ..
```

## 🎬 Utilisation

### Format de l'API

```json
{
  "input": {
    "image": "https://example.com/photo.jpg",  // ou base64
    "text": "Bonjour, je suis un avatar virtuel.",
    "language": "fr",  // optionnel: fr, en, es, etc.
    "voice": "default"  // optionnel
  }
}
```

### Exemple Python

```python
import runpod

runpod.api_key = "votre-clé-api"
endpoint = runpod.Endpoint("votre-endpoint-id")

result = endpoint.run_sync({
    "input": {
        "image": "https://example.com/photo.jpg",
        "text": "Bonjour, je suis un avatar créé avec RunPod.",
        "language": "fr"
    }
})

print(f"Vidéo: {result['video_url']}")
```

### Exemple avec image base64

```python
import base64

with open('photo.jpg', 'rb') as f:
    image_b64 = base64.b64encode(f.read()).decode('utf-8')

result = endpoint.run_sync({
    "input": {
        "image": f"data:image/jpeg;base64,{image_b64}",
        "text": "Test avec image locale."
    }
})
```

## 🔧 Configuration des services

### 1. Text-to-Speech (TTS)

Choisissez un service TTS selon vos besoins:

#### Option A: gTTS (Gratuit, basique)
```bash
pip install gTTS
```
✅ Gratuit  
❌ Qualité basique  
❌ Voix limitées

#### Option B: ElevenLabs (Recommandé, payant)
```bash
pip install elevenlabs
```
```python
# Dans handler_talking_head.py, modifiez text_to_speech():
from elevenlabs import generate, set_api_key

set_api_key(os.environ.get('ELEVENLABS_API_KEY'))
audio = generate(text=text, voice="Bella")
```
✅ Excellente qualité  
✅ Voix naturelles  
💰 Payant (~$0.30/1K caractères)

#### Option C: Azure TTS (Professionnel)
```bash
pip install azure-cognitiveservices-speech
```
✅ Qualité professionnelle  
✅ Multi-langues  
💰 Payant (~$1/1M caractères)

#### Option D: Coqui TTS (Open source)
```bash
pip install TTS
```
✅ Open source  
✅ Bonne qualité  
⚠️ Nécessite GPU

### 2. Modèle Talking Head

#### Option A: Wav2Lip (Recommandé)

**Avantages:**
- Lip-sync précis
- Rapide
- Modèle mature

**Installation:**
```bash
# Cloner le repo
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip

# Télécharger le modèle
wget 'https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth' \
  -O 'checkpoints/wav2lip_gan.pth'

# Installer
pip install -r requirements.txt
```

**Intégration dans handler_talking_head.py:**
```python
import sys
sys.path.append('./Wav2Lip')
from inference import main as wav2lip_inference

def generate_talking_head(image_path, audio_path, output_path):
    wav2lip_inference(
        checkpoint_path='Wav2Lip/checkpoints/wav2lip_gan.pth',
        face=image_path,
        audio=audio_path,
        outfile=output_path,
        static=False,
        fps=25,
        resize_factor=1
    )
    return output_path
```

#### Option B: SadTalker (Meilleure qualité)

**Avantages:**
- Mouvements de tête naturels
- Expressions faciales
- Meilleure qualité visuelle

**Installation:**
```bash
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt

# Télécharger les modèles (automatique au premier run)
```

**Plus exigeant en ressources (GPU puissant recommandé)**

#### Option C: D-ID API (Cloud, le plus simple)

```bash
pip install requests
```

```python
import requests

def generate_talking_head(image_url, audio_url, output_path):
    response = requests.post(
        'https://api.d-id.com/talks',
        headers={
            'Authorization': f'Basic {D_ID_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'source_url': image_url,
            'script': {
                'type': 'audio',
                'audio_url': audio_url
            }
        }
    )
    # Récupérer la vidéo une fois prête
    video_url = response.json()['result_url']
    return video_url
```

✅ Très simple  
✅ Qualité professionnelle  
💰 Payant (~$0.10/vidéo)

## 🐳 Déploiement Docker

### 1. Construire l'image

```bash
# Build avec GPU support
docker build -f Dockerfile.talking_head -t talking-head-api .

# Tag pour votre registry
docker tag talking-head-api votre-username/talking-head-api:latest

# Push
docker push votre-username/talking-head-api:latest
```

### 2. Déployer sur RunPod

1. Allez sur [RunPod Serverless](https://www.runpod.io/console/serverless)
2. Créez un nouveau endpoint
3. Configuration:
   - **Image Docker:** `votre-username/talking-head-api:latest`
   - **GPU:** RTX 3090 ou mieux (pour Wav2Lip/SadTalker)
   - **Idle Timeout:** 30s
   - **Max Workers:** 3-10 selon votre budget

### 3. Variables d'environnement

Configurez dans RunPod:
```bash
ELEVENLABS_API_KEY=votre-clé     # Si vous utilisez ElevenLabs
AWS_ACCESS_KEY_ID=votre-clé       # Pour upload S3
AWS_SECRET_ACCESS_KEY=votre-secret
S3_BUCKET_NAME=votre-bucket
```

## 💰 Coûts estimés

### Par vidéo (30 secondes):

**Option économique (gTTS + Wav2Lip):**
- TTS: Gratuit
- Génération vidéo: ~$0.02 (GPU RunPod)
- Storage S3: ~$0.001
- **Total: ~$0.02/vidéo**

**Option premium (ElevenLabs + Wav2Lip):**
- TTS: ~$0.03
- Génération vidéo: ~$0.02
- Storage S3: ~$0.001
- **Total: ~$0.05/vidéo**

**Option cloud (D-ID):**
- Tout inclus: ~$0.10/vidéo

## 🧪 Tests

### Test local (sans modèle)
```bash
python test_talking_head.py
```

### Test avec vraie image
```bash
# Ajoutez une photo
cp votre-photo.jpg test_image.jpg

# Modifiez test_talking_head.py pour décommenter les tests complets
python test_talking_head.py
```

## 📊 Performance

### Temps de génération typiques:

| Configuration | Temps (30s vidéo) | Coût |
|--------------|------------------|------|
| gTTS + Wav2Lip (RTX 3090) | ~15s | $0.02 |
| ElevenLabs + Wav2Lip (RTX 3090) | ~20s | $0.05 |
| ElevenLabs + SadTalker (A100) | ~45s | $0.10 |
| D-ID API | ~60s | $0.10 |

## 🎨 Cas d'usage

- **E-learning:** Avatars pour cours en ligne
- **Marketing:** Vidéos personnalisées à grande échelle
- **Accessibilité:** Traduction vidéo avec lip-sync
- **Réseaux sociaux:** Contenu automatisé
- **Service client:** Avatars virtuels 24/7
- **Actualités:** Présentateurs virtuels

## ⚠️ Limitations et considérations

### Techniques:
- Qualité dépend de la photo d'entrée (visage bien visible)
- Mouvements de tête limités avec Wav2Lip
- Cold start: 10-30s la première fois

### Éthiques:
- ⚠️ **Deepfakes:** Utilisez cette technologie de manière responsable
- Obtenez le consentement avant d'utiliser une photo
- Ajoutez des watermarks pour indiquer le contenu synthétique
- Respectez les lois sur l'usurpation d'identité

### Légales:
- Vérifiez les droits d'utilisation des photos
- Conformité RGPD si données personnelles
- Certains pays régulent strictement les deepfakes

## 🔗 Ressources

- [Wav2Lip GitHub](https://github.com/Rudrabha/Wav2Lip)
- [SadTalker GitHub](https://github.com/OpenTalker/SadTalker)
- [D-ID API](https://www.d-id.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [RunPod Documentation](https://docs.runpod.io/)

## 🆘 Support

Pour les questions et problèmes:
1. Vérifiez les logs dans le dashboard RunPod
2. Testez localement avec `test_talking_head.py`
3. Consultez la documentation des modèles

## 📝 TODO / Améliorations futures

- [ ] Support multi-visages
- [ ] Gestion du cache des modèles
- [ ] Optimisation du cold start
- [ ] Support des émotions personnalisées
- [ ] API de preview (aperçu sans génération complète)
- [ ] Batch processing (plusieurs vidéos en parallèle)
- [ ] Watermarking automatique
