"""
Exemple d'utilisation de l'API RunPod pour appeler votre serverless
=====================================================================
Ce script montre comment appeler votre fonction serverless déployée sur RunPod.
"""

import runpod
import os
import json
import time

# Définir votre clé API RunPod
# Option 1: Variable d'environnement (recommandé)
runpod.api_key = os.environ.get("RUNPOD_API_KEY")

# Option 2: Directement dans le code (non recommandé pour la production)
# runpod.api_key = "votre-clé-api-ici"

# L'ID de votre endpoint serverless (à obtenir depuis le dashboard RunPod)
ENDPOINT_ID = "votre-endpoint-id"


def run_sync_job():
    """
    Exécute un job synchrone (attend le résultat).
    Utilisez cette méthode pour des tâches rapides (< 60 secondes).
    """
    print("\n=== Exemple: Job Synchrone ===")
    
    endpoint = runpod.Endpoint(ENDPOINT_ID)
    
    try:
        result = endpoint.run_sync({
            "input": {
                "message": "Hello from RunPod API!",
                "operation": "uppercase"
            }
        }, timeout=60)  # timeout en secondes
        
        print(f"Résultat: {json.dumps(result, indent=2)}")
        return result
    except TimeoutError:
        print("Le job a dépassé le timeout")
    except Exception as e:
        print(f"Erreur: {e}")


def run_async_job():
    """
    Exécute un job asynchrone (ne bloque pas).
    Utilisez cette méthode pour des tâches longues.
    """
    print("\n=== Exemple: Job Asynchrone ===")
    
    endpoint = runpod.Endpoint(ENDPOINT_ID)
    
    try:
        # Soumettre le job
        run_request = endpoint.run({
            "input": {
                "message": "Traitement asynchrone",
                "operation": "reverse"
            }
        })
        
        job_id = run_request.job_id
        print(f"Job soumis avec l'ID: {job_id}")
        
        # Attendre le résultat
        print("Attente du résultat...")
        while True:
            status = endpoint.status(run_request)
            print(f"Statut: {status['status']}")
            
            if status['status'] == 'COMPLETED':
                result = status['output']
                print(f"Résultat: {json.dumps(result, indent=2)}")
                return result
            elif status['status'] == 'FAILED':
                print(f"Le job a échoué: {status.get('error', 'Erreur inconnue')}")
                return None
            
            time.sleep(2)  # Attendre 2 secondes avant de vérifier à nouveau
            
    except Exception as e:
        print(f"Erreur: {e}")


def run_stream_job():
    """
    Exécute un job avec streaming (reçoit les résultats progressifs).
    Utilisez cette méthode pour des tâches qui produisent des résultats intermédiaires.
    """
    print("\n=== Exemple: Job avec Streaming ===")
    
    endpoint = runpod.Endpoint(ENDPOINT_ID)
    
    try:
        for output in endpoint.run_sync({
            "input": {
                "iterations": 5
            }
        }, timeout=120):
            print(f"Résultat intermédiaire: {json.dumps(output, indent=2)}")
            
    except Exception as e:
        print(f"Erreur: {e}")


def health_check():
    """
    Vérifie si l'endpoint est disponible.
    """
    print("\n=== Health Check ===")
    
    endpoint = runpod.Endpoint(ENDPOINT_ID)
    
    try:
        health = endpoint.health()
        print(f"Santé de l'endpoint: {json.dumps(health, indent=2)}")
        return health
    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Exemples d'utilisation de l'API RunPod")
    print("=" * 60)
    
    if not runpod.api_key:
        print("\n⚠️  ATTENTION: Vous devez définir votre clé API RunPod!")
        print("   Définissez la variable d'environnement RUNPOD_API_KEY")
        print("   ou modifiez ce fichier pour ajouter votre clé.")
    else:
        # Décommentez les exemples que vous voulez tester
        # health_check()
        # run_sync_job()
        # run_async_job()
        # run_stream_job()
        pass
