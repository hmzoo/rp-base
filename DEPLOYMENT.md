# Déploiement RunPod Serverless depuis GitHub

## 🚀 Méthode simplifiée (sans Docker Hub)

RunPod peut builder votre serverless directement depuis GitHub.

### 1. Structure de votre repo

Votre repo doit contenir:
```
rp-base/
├── handler.py (ou handler_talking_head.py)
├── requirements.txt
├── Dockerfile (optionnel mais recommandé)
└── README.md
```

### 2. Configuration RunPod

#### Étape 1: Préparez votre repo GitHub
```bash
# Commitez vos changements
git add .
git commit -m "Serverless ready"
git push origin main
```

#### Étape 2: Créez l'endpoint dans RunPod

1. Allez sur https://www.runpod.io/console/serverless
2. Cliquez sur "New Endpoint"
3. Dans la section **"Container Image"**, choisissez:
   - **Option A**: Image Docker custom (si vous avez un Dockerfile)
   - **Option B**: Image de base Python

#### Option A: Avec Dockerfile (Recommandé)

Dans RunPod:
- **Container Image**: `runpod/base:0.4.0-cuda11.8.0` (ou votre image de base)
- Cochez "Use GitHub"
- **Repository**: `votre-username/rp-base`
- **Branch**: `main`
- **Start Command**: `python -u handler.py`

#### Option B: Sans Dockerfile (simple)

Dans RunPod:
- **Container Image**: `runpod/base:0.4.0-cuda11.8.0`
- Cochez "Use GitHub" 
- **Repository**: `votre-username/rp-base`
- **Branch**: `main`
- Ajoutez un **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: `python -u handler.py`

### 3. Configuration avancée

#### Variables d'environnement
```bash
RUNPOD_AI_API_KEY=votre-clé
AWS_ACCESS_KEY_ID=votre-clé-aws
```

#### GPU Selection
- **CPU Only**: Pour API simple (texte, etc.)
- **RTX 3090**: Pour AI/ML léger
- **A100**: Pour modèles lourds (LLM, Stable Diffusion)

### 4. Auto-déploiement avec webhook

RunPod peut redéployer automatiquement à chaque push GitHub:

1. Dans RunPod, allez dans les settings de votre endpoint
2. Activez **"Auto Deploy"**
3. Copiez le webhook URL
4. Dans GitHub:
   - Settings → Webhooks → Add webhook
   - Paste l'URL du webhook RunPod
   - Events: `push`

Maintenant, chaque `git push` redéploie automatiquement ! 🎉

### 5. Exemple complet

```bash
# 1. Modifiez votre code
vim handler.py

# 2. Testez localement
python test_local.py

# 3. Committez et pushez
git add .
git commit -m "Update handler"
git push origin main

# 4. RunPod redéploie automatiquement (si webhook configuré)
#    Sinon, cliquez sur "Redeploy" dans le dashboard
```

## 🎯 Quelle méthode choisir?

### GitHub directe (Recommandée pour vous)
✅ Simple et rapide à configurer  
✅ Pas besoin de Docker Hub  
✅ CI/CD automatique  
✅ Idéal pour le développement  
❌ Cold start un peu plus long

**Utilisez si:** Vous voulez la simplicité maximale

### Image Docker pré-buildée
✅ Cold start ultra-rapide  
✅ Environnement complètement contrôlé  
✅ Idéal pour production  
❌ Nécessite Docker Hub  
❌ Étape supplémentaire

**Utilisez si:** Performance critique ou environnement complexe

## 📊 Comparaison des temps

| Méthode | Build time | Cold start | Simplicité |
|---------|-----------|------------|------------|
| GitHub | 2-5 min | 15-30s | ⭐⭐⭐⭐⭐ |
| Docker | 0 | 5-10s | ⭐⭐⭐ |

## 🔧 Debugging

### Voir les logs de build
Dans RunPod dashboard → Votre endpoint → Logs

### Erreurs courantes

**"Module not found"**
→ Vérifiez que `requirements.txt` est correct

**"Handler not found"**
→ Vérifiez le Start Command: `python -u handler.py`

**"Build timeout"**
→ L'image de base ou les dépendances sont trop lourdes
→ Utilisez une image Docker pré-buildée

## 💡 Astuce Pro

Pour le meilleur des deux mondes:
1. **Développement**: Déployez depuis GitHub
2. **Production**: Buildez une image Docker optimisée

## 🆘 Support

Si problème avec GitHub:
1. Vérifiez que le repo est public (ou configurez les credentials)
2. Vérifiez le chemin du handler dans Start Command
3. Consultez les logs de build dans RunPod
