"""
Script de surveillance des logs RunPod
Affiche le statut de l'endpoint et les logs récents
"""
import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RUNPOD_API_KEY")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

def get_endpoint_status():
    """Récupère le statut de l'endpoint via API REST v2"""
    try:
        url = f"https://api.runpod.io/v2/{ENDPOINT_ID}/status"
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur récupération endpoint: {e}")
        return None

def display_status(data):
    """Affiche le statut de l'endpoint"""
    if not data:
        return
    
    print("\n" + "="*70)
    print(f"📊 Statut de l'endpoint: {ENDPOINT_ID}")
    print("="*70)
    
    # Workers info
    jobs = data.get('jobs', {})
    workers = data.get('workers', {})
    
    print(f"\n👷 Workers:")
    print(f"   ▫️ Idle: {workers.get('idle', 0)}")
    print(f"   ▫️ Running: {workers.get('running', 0)}")
    print(f"   ▫️ Throttled: {workers.get('throttled', 0)}")
    
    print(f"\n📋 Jobs:")
    print(f"   ▫️ In Queue: {jobs.get('inQueue', 0)}")
    print(f"   ▫️ In Progress: {jobs.get('inProgress', 0)}")
    print(f"   ▫️ Completed: {jobs.get('completed', 0)}")
    print(f"   ▫️ Failed: {jobs.get('failed', 0)}")
    
    # Status indicators
    idle = workers.get('idle', 0)
    running = workers.get('running', 0)
    total = idle + running
    
    if total > 0:
        print(f"\n✅ Endpoint ACTIF - {total} workers opérationnels")
        if idle == 0 and running > 0:
            print(f"⚠️  Tous les workers sont occupés")
        elif idle > 0:
            print(f"🟢 {idle} workers disponibles")
    else:
        print(f"\n🔄 Endpoint en démarrage ou BUILD EN COURS")
        print(f"💡 Les workers vont apparaître une fois le build terminé")

def monitor_loop(interval=30):
    """Surveillance en boucle"""
    print(f"\n🔄 Surveillance de l'endpoint toutes les {interval}s")
    print(f"   (Ctrl+C pour arrêter)\n")
    
    try:
        while True:
            endpoint = get_endpoint_status()
            display_status(endpoint)
            
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Prochaine vérification dans {interval}s...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Surveillance arrêtée")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "loop":
        # Mode surveillance continue
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor_loop(interval)
    else:
        # Mode vérification unique
        endpoint = get_endpoint_status()
        display_status(endpoint)
        
        print("\n💡 Pour surveiller en continu:")
        print(f"   python monitor_runpod.py loop [interval_secondes]")
