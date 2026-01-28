# RunPod Serverless - Projet d'apprentissage

Ce projet est un template de base pour apprendre à créer et déployer des fonctions serverless sur RunPod.

## 📋 Structure du projet

```
rp-base/
├── handler.py           # Handler principal pour la fonction serverless
├── test_local.py        # Tests locaux du handler
├── test_api.py          # Exemples d'utilisation de l'API RunPod
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Configuration Docker pour le déploiement
└── README.md           # Ce fichier
```

## 🚀 Démarrage rapide

### 1. Installation des dépendances locales

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Tester localement

```bash
# Exécuter les tests locaux
python test_local.py
```

### 3. Construire l'image Docker

```bash
# Construire l'image
docker build -t runpod-serverless-base .

# Tester l'image localement (optionnel)
docker run --rm runpod-serverless-base
```

### 4. Déployer sur RunPod

1. Créez un compte sur [RunPod](https://www.runpod.io/)
2. Poussez votre image Docker sur Docker Hub ou un autre registre:
   ```bash
   docker tag runpod-serverless-base votre-username/runpod-serverless-base
   docker push votre-username/runpod-serverless-base
   ```
3. Dans le dashboard RunPod:
   - Allez dans "Serverless" > "New Endpoint"
   - Entrez l'URL de votre image Docker
   - Configurez les ressources (GPU/CPU)
   - Déployez!

## 📚 Concepts clés

### Le Handler

Le handler est la fonction principale qui traite les requêtes. Il reçoit un événement avec un `input` et retourne un résultat:

```python
def handler(event):
    job_input = event.get('input', {})
    # Votre logique ici
    return {'output': 'résultat'}
```

### Types de handlers

1. **Handler simple**: Traite une requête et retourne un résultat
2. **Handler avec streaming**: Utilise un générateur pour retourner des résultats progressifs

### Format d'entrée

```json
{
  "input": {
    "message": "Votre message",
    "operation": "echo|uppercase|reverse|length"
  }
}
```

### Format de sortie

```json
{
  "output": "Résultat de l'opération",
  "operation": "echo"
}
```

## 🔧 Personnalisation

### Ajouter vos propres opérations

Modifiez [handler.py](handler.py) pour ajouter vos propres opérations:

```python
elif operation == 'ma_nouvelle_operation':
    result = {
        'output': votre_traitement(message),
        'operation': operation
    }
```

### Ajouter des dépendances

Ajoutez vos dépendances dans [requirements.txt](requirements.txt):

```txt
torch>=2.0.0
transformers>=4.30.0
```

### Utiliser un GPU

Si votre fonction nécessite un GPU (par exemple pour du ML/AI):

1. Modifiez le Dockerfile pour utiliser une image CUDA:
   ```dockerfile
   FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
   ```
2. Installez PyTorch ou TensorFlow selon vos besoins
3. Sélectionnez un GPU dans les paramètres de l'endpoint RunPod

## 🧪 Tests

### Tests locaux

```bash
python test_local.py
```

### Tests API (après déploiement)

1. Obtenez votre clé API depuis le dashboard RunPod
2. Définissez la variable d'environnement:
   ```bash
   export RUNPOD_API_KEY="votre-clé-api"
   ```
3. Modifiez [test_api.py](test_api.py) avec votre endpoint ID
4. Exécutez:
   ```bash
   python test_api.py
   ```

## 📖 Ressources

- [Documentation RunPod](https://docs.runpod.io/)
- [RunPod Python SDK](https://github.com/runpod/runpod-python)
- [Exemples de serverless RunPod](https://github.com/runpod-workers)

## 🎯 Prochaines étapes

1. ✅ Comprendre le fonctionnement de base du handler
2. ✅ Tester localement vos modifications
3. 🔄 Ajouter votre propre logique métier
4. 🔄 Déployer sur RunPod
5. 🔄 Tester avec l'API RunPod
6. 🔄 Optimiser les performances et les coûts

## 💡 Conseils

- **Gardez vos images Docker légères** pour des déploiements rapides
- **Testez toujours localement** avant de déployer
- **Utilisez des variables d'environnement** pour les secrets
- **Gérez les erreurs gracieusement** dans votre handler
- **Documentez votre API** pour faciliter l'utilisation

## 📝 License

Ce projet est un template d'apprentissage et peut être utilisé librement.