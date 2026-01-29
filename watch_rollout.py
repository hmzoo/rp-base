#!/usr/bin/env python3
"""
Surveillance automatique du rollout RunPod
"""
import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def check_health():
    """Vérifie l'état de santé de l'endpoint"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/health"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def display_status(data):
    """Affiche le statut formaté"""
    if not data:
        print("❌ Impossible de récupérer le statut")
        return
    
    workers = data.get('workers', {})
    jobs = data.get('jobs', {})
    
    print(f"\n{'='*70}")
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*70}")
    
    # Workers
    print(f"\n👷 WORKERS:")
    print(f"   🟢 Ready:        {workers.get('ready', 0)}")
    print(f"   🏃 Running:      {workers.get('running', 0)}")
    print(f"   😴 Idle:         {workers.get('idle', 0)}")
    print(f"   🔄 Initializing: {workers.get('initializing', 0)}")
    print(f"   ⏸️  Throttled:    {workers.get('throttled', 0)}")
    print(f"   🔴 Unhealthy:    {workers.get('unhealthy', 0)}")
    
    # Jobs
    print(f"\n📋 JOBS:")
    print(f"   ⏳ In Queue:     {jobs.get('inQueue', 0)}")
    print(f"   🔄 In Progress:  {jobs.get('inProgress', 0)}")
    print(f"   ✅ Completed:    {jobs.get('completed', 0)}")
    print(f"   ❌ Failed:       {jobs.get('failed', 0)}")
    
    # Status global
    ready = workers.get('ready', 0)
    idle = workers.get('idle', 0)
    initializing = workers.get('initializing', 0)
    unhealthy = workers.get('unhealthy', 0)
    
    total_operational = ready + idle
    
    print(f"\n📊 STATUS:")
    if total_operational > 0:
        print(f"   ✅ {total_operational} worker(s) opérationnel(s)")
        return True
    elif initializing > 0:
        print(f"   🔄 {initializing} worker(s) en démarrage...")
        print(f"   💡 Rollout en cours, patientez...")
        return False
    elif unhealthy > 0:
        print(f"   ⚠️  {unhealthy} worker(s) en erreur")
        print(f"   💡 Vérifiez les logs pour voir l'erreur")
        return False
    else:
        print(f"   ⏸️  Aucun worker actif")
        return False

def test_request():
    """Envoie une requête de test"""
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "image": "https://picsum.photos/400/600",
            "text": "Test de Coqui TTS après rollout.",
            "language": "fr"
        }
    }
    
    print(f"\n🧪 Test de génération audio...")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            output = data.get('output', {})
            
            if 'audio_size_bytes' in output:
                size_kb = output['audio_size_bytes'] / 1024
                print(f"   ✅ Audio généré: {size_kb:.1f} KB")
                print(f"   ⏱️  Temps de réponse inclus dans la requête")
                return True
            else:
                print(f"   ⚠️  Pas d'audio dans la réponse: {data}")
                return False
        else:
            print(f"   ❌ Erreur HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout après 90s")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def monitor(interval=20, auto_test=True):
    """Surveillance en boucle"""
    print(f"\n{'='*70}")
    print(f"🔍 SURVEILLANCE DU ROLLOUT RUNPOD")
    print(f"{'='*70}")
    print(f"\n⏱️  Vérification toutes les {interval}s")
    print(f"🧪 Test automatique: {'OUI' if auto_test else 'NON'}")
    print(f"\n💡 Ctrl+C pour arrêter\n")
    
    tested = False
    
    try:
        while True:
            data = check_health()
            operational = display_status(data)
            
            # Test automatique dès qu'un worker est prêt
            if operational and auto_test and not tested:
                print(f"\n🎉 Worker opérationnel détecté!")
                time.sleep(2)
                if test_request():
                    print(f"\n✅ SUCCÈS! L'endpoint fonctionne correctement.")
                    tested = True
                else:
                    print(f"\n⚠️  Le test a échoué, vérifiez les logs.")
            
            print(f"\n⏳ Prochaine vérification dans {interval}s...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\n👋 Surveillance arrêtée\n")

if __name__ == "__main__":
    monitor(interval=20, auto_test=True)
