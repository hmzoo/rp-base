"""
RunPod Serverless Handler
========================
Ce fichier contient le handler principal pour votre fonction serverless RunPod.

Le handler reçoit un événement (job) avec un input et doit retourner un résultat.
"""

import runpod
import json


def handler(event):
    """
    Handler principal pour la fonction serverless RunPod.
    
    Args:
        event (dict): L'événement contenant les données d'entrée
            - input: Les données d'entrée fournies par l'utilisateur
            - id: L'ID unique du job
            
    Returns:
        dict: Le résultat de la fonction
    """
    try:
        # Récupérer l'input de l'événement
        job_input = event.get('input', {})
        
        # Exemple: traitement simple
        message = job_input.get('message', 'Hello from RunPod!')
        operation = job_input.get('operation', 'echo')
        
        # Logique de traitement selon l'opération
        if operation == 'echo':
            result = {
                'output': message,
                'operation': operation
            }
        elif operation == 'uppercase':
            result = {
                'output': message.upper(),
                'operation': operation
            }
        elif operation == 'reverse':
            result = {
                'output': message[::-1],
                'operation': operation
            }
        elif operation == 'length':
            result = {
                'output': len(message),
                'operation': operation,
                'message': message
            }
        else:
            result = {
                'error': f'Opération inconnue: {operation}',
                'available_operations': ['echo', 'uppercase', 'reverse', 'length']
            }
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'type': type(e).__name__
        }


def advanced_handler(event):
    """
    Handler avancé avec support du streaming et des générateurs.
    Utile pour les tâches de longue durée qui nécessitent des mises à jour progressives.
    
    Args:
        event (dict): L'événement contenant les données d'entrée
        
    Yields:
        dict: Résultats intermédiaires pour le streaming
    """
    job_input = event.get('input', {})
    iterations = job_input.get('iterations', 5)
    
    for i in range(iterations):
        # Simuler un traitement
        yield {
            'progress': (i + 1) / iterations * 100,
            'step': i + 1,
            'total_steps': iterations,
            'message': f'Étape {i + 1} sur {iterations}'
        }
    
    # Résultat final
    yield {
        'status': 'completed',
        'total_iterations': iterations
    }


if __name__ == "__main__":
    # Démarrer le worker RunPod avec le handler simple
    # Pour utiliser le handler avancé avec streaming, utilisez:
    # runpod.serverless.start({"handler": advanced_handler, "return_aggregate_stream": True})
    
    runpod.serverless.start({"handler": handler})
