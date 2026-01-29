#!/bin/bash
# Script pour ouvrir les logs RunPod dans le navigateur

ENDPOINT_ID="3vsf8k28xyy0ki"

echo "🌐 Ouverture des logs RunPod..."
echo ""
echo "📋 Endpoints:"
echo "   https://www.runpod.io/console/serverless/user/endpoints"
echo ""
echo "📊 Endpoint spécifique (logs):"
echo "   https://www.runpod.io/console/serverless/user/endpoint/${ENDPOINT_ID}"
echo ""
echo "💡 Dans l'interface:"
echo "   1. Cliquez sur l'endpoint 'API Talking Head Coqui'"
echo "   2. Allez dans l'onglet 'Logs'"
echo "   3. Regardez les logs de démarrage des workers"
echo ""
echo "🔍 Ce qu'on cherche:"
echo "   - Logs Python au démarrage"
echo "   - Messages d'erreur d'import"
echo "   - Problèmes de dépendances"
echo ""

# Tentative d'ouverture automatique (si xdg-open disponible)
if command -v xdg-open &> /dev/null; then
    read -p "Ouvrir dans le navigateur? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "https://www.runpod.io/console/serverless/user/endpoint/${ENDPOINT_ID}"
    fi
fi
