"""
Script de test local pour le handler RunPod
===========================================
Ce script permet de tester votre handler localement avant de le déployer.
"""

import json
from handler import handler, advanced_handler


def test_echo_operation():
    """Test l'opération echo."""
    print("\n=== Test: Echo Operation ===")
    event = {
        'input': {
            'message': 'Bonjour RunPod!',
            'operation': 'echo'
        },
        'id': 'test-job-1'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    assert result['output'] == 'Bonjour RunPod!'
    print("✓ Test réussi")


def test_uppercase_operation():
    """Test l'opération uppercase."""
    print("\n=== Test: Uppercase Operation ===")
    event = {
        'input': {
            'message': 'hello world',
            'operation': 'uppercase'
        },
        'id': 'test-job-2'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    assert result['output'] == 'HELLO WORLD'
    print("✓ Test réussi")


def test_reverse_operation():
    """Test l'opération reverse."""
    print("\n=== Test: Reverse Operation ===")
    event = {
        'input': {
            'message': 'RunPod',
            'operation': 'reverse'
        },
        'id': 'test-job-3'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    assert result['output'] == 'doPnuR'
    print("✓ Test réussi")


def test_length_operation():
    """Test l'opération length."""
    print("\n=== Test: Length Operation ===")
    event = {
        'input': {
            'message': 'Serverless',
            'operation': 'length'
        },
        'id': 'test-job-4'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    assert result['output'] == 10
    print("✓ Test réussi")


def test_unknown_operation():
    """Test une opération inconnue."""
    print("\n=== Test: Unknown Operation ===")
    event = {
        'input': {
            'message': 'test',
            'operation': 'unknown'
        },
        'id': 'test-job-5'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    assert 'error' in result
    print("✓ Test réussi")


def test_advanced_handler():
    """Test le handler avancé avec streaming."""
    print("\n=== Test: Advanced Handler (Streaming) ===")
    event = {
        'input': {
            'iterations': 3
        },
        'id': 'test-job-6'
    }
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print("Output (streaming):")
    for result in advanced_handler(event):
        print(f"  → {json.dumps(result, indent=4)}")
    print("✓ Test réussi")


def test_error_handling():
    """Test la gestion des erreurs."""
    print("\n=== Test: Error Handling ===")
    event = {
        'input': {
            'message': 123,  # Devrait être une chaîne
            'operation': 'uppercase'
        },
        'id': 'test-job-7'
    }
    result = handler(event)
    print(f"Input: {json.dumps(event['input'], indent=2)}")
    print(f"Output: {json.dumps(result, indent=2)}")
    # Le handler devrait gérer l'erreur gracieusement
    print("✓ Test réussi")


if __name__ == "__main__":
    print("=" * 60)
    print("Tests du handler RunPod Serverless")
    print("=" * 60)
    
    try:
        test_echo_operation()
        test_uppercase_operation()
        test_reverse_operation()
        test_length_operation()
        test_unknown_operation()
        test_advanced_handler()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("✓ Tous les tests sont passés avec succès!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
