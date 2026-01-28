# Configuration du nouvel endpoint RunPod - API Talking Head

## 📋 Informations à saisir dans RunPod

### 1. Configuration de base

**Nom de l'endpoint:**
```
rp-talking-head
```

### 2. Container Configuration

**Container Image:**
```
runpod/base:0.6.2-cuda12.1.0
```

☑️ **Use GitHub** (cocher)

**GitHub Repository:**
```
hmzoo/rp-base
```

**Branch:**
```
main
```

### 3. Build & Start Commands

**Build Command:**
```bash
pip install --no-cache-dir -r requirements_talking_head.txt
```

**Start Command:**
```bash
python -u handler_talking_head.py
```

### 4. GPU Configuration ⚠️ IMPORTANT

**GPU Type:** 
- Pour développement: **RTX 3090** (24GB VRAM)
- Pour production: **RTX 4090** ou **A40** (meilleur performance/prix)

**Min Workers:** 0 (auto-scaling)
**Max Workers:** 3 (ajustez selon votre budget)

**Idle Timeout:** 30 secondes
**Execution Timeout:** 600 secondes (10 min pour les vidéos longues)

### 5. Variables d'environnement (optionnel)

Si vous utilisez des services externes:

```bash
# Pour ElevenLabs (TTS premium)
ELEVENLABS_API_KEY=votre_clé

# Pour S3 (upload vidéos)
AWS_ACCESS_KEY_ID=votre_clé
AWS_SECRET_ACCESS_KEY=votre_secret
S3_BUCKET_NAME=votre_bucket

# Pour D-ID (alternative talking head)
DID_API_KEY=votre_clé
```

### 6. Network & Storage

**Network Volume:** Aucun (pour l'instant)
**Template Volume:** Aucun

### 7. Advanced Settings

**Active Workers:** 
- Min: 0 (coût $0 quand pas utilisé)
- Max: 3

**Throttle Queue:** 25

**GPUs per Worker:** 1

## 🚀 Étapes de création

1. Allez sur https://www.runpod.io/console/serverless
2. Cliquez sur **"New Endpoint"**
3. Copiez-collez les valeurs ci-dessus
4. Cliquez sur **"Deploy"**
5. Attendez 2-5 minutes que le build se termine

## 💰 Coût estimé

**RTX 3090:**
- Idle: $0/heure (min workers = 0)
- Active: ~$0.24/heure
- Par vidéo (30s): ~$0.002

**RTX 4090:**
- Active: ~$0.36/heure
- Par vidéo (30s): ~$0.003

## ⚠️ Note importante

Pour l'instant, cette configuration utilise **uniquement gTTS** pour le TTS (qualité basique).

Pour une vraie implémentation avec Wav2Lip/SadTalker:
1. Créer une image Docker personnalisée avec les modèles
2. Ou utiliser une API cloud comme D-ID

Voir [README_TALKING_HEAD.md](README_TALKING_HEAD.md) pour plus de détails.

## 📊 Vérification

Une fois déployé:
1. Attendez que le statut soit "Active"
2. Vérifiez que des workers sont "Ready"
3. Récupérez le nouvel ENDPOINT_ID
4. Testez avec test_talking_head.py
