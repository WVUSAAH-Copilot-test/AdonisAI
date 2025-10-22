#!/bin/bash

# AdonisAI Quick Start Script
# Dieses Skript hilft beim initialen Setup des Projekts

echo "╔═══════════════════════════════════════════════╗"
echo "║                                               ║"
echo "║          🤖  AdonisAI Setup  🤖               ║"
echo "║                                               ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Prüfe ob Python 3.10+ installiert ist
echo "🔍 Prüfe Python Version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "   Bitte installiere Python 3.10 oder höher"
    exit 1
fi

echo "✅ Python ${PYTHON_VERSION} gefunden"
echo ""

# Erstelle virtuelle Umgebung
echo "📦 Erstelle virtuelle Umgebung..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtuelle Umgebung erstellt"
else
    echo "ℹ️  Virtuelle Umgebung existiert bereits"
fi
echo ""

# Aktiviere virtuelle Umgebung
echo "🔧 Aktiviere virtuelle Umgebung..."
source venv/bin/activate
echo "✅ Virtuelle Umgebung aktiviert"
echo ""

# Installiere Dependencies
echo "📥 Installiere Abhängigkeiten..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Abhängigkeiten installiert"
echo ""

# Erstelle .env wenn nicht vorhanden
if [ ! -f ".env" ]; then
    echo "📝 Erstelle .env Datei..."
    cp .env.example .env
    echo "✅ .env Datei erstellt"
    echo ""
    echo "⚠️  WICHTIG: Bitte bearbeite die .env Datei und füge deinen Telegram Bot Token ein!"
    echo "   nano .env"
    echo ""
else
    echo "ℹ️  .env Datei existiert bereits"
    echo ""
fi

# Erstelle notwendige Verzeichnisse
echo "📁 Erstelle Verzeichnisse..."
mkdir -p data logs
echo "✅ Verzeichnisse erstellt"
echo ""

echo "╔═══════════════════════════════════════════════╗"
echo "║              Setup abgeschlossen! ✅          ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📋 Nächste Schritte:"
echo ""
echo "1. Telegram Bot Token holen:"
echo "   - Öffne Telegram und suche nach @BotFather"
echo "   - Sende /newbot und folge den Anweisungen"
echo "   - Kopiere den Token"
echo ""
echo "2. Token in .env eintragen:"
echo "   nano .env"
echo ""
echo "3. Bot starten:"
echo "   source venv/bin/activate  # Falls noch nicht aktiv"
echo "   python src/main.py"
echo ""
echo "📖 Weitere Informationen: README.md"
echo ""
