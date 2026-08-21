#!/bin/bash

echo "==========================================="
echo " Setting up .ac AI Assistant Environment"
echo " for Samsung DeX (Termux)"
echo "==========================================="

# Update packages
echo "[1/4] Updating package list..."
pkg update -y && pkg upgrade -y

# Install Python and essential tools
echo "[2/4] Installing Python, clang, and dependencies..."
pkg install python python-pip clang make libffi openssl -y

# Install pip requirements
echo "[3/4] Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Create necessary directories
echo "[4/4] Creating data directories..."
mkdir -p data/vector_db
mkdir -p data/knowledge_base

echo "==========================================="
echo " Setup Complete! 🎉"
echo ""
echo " Next Steps:"
echo " 1. Make sure you have Ollama installed or running."
echo " 2. Put some markdown/code files in 'data/knowledge_base'"
echo " 3. Run: python src/ingest.py"
echo " 4. Run: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo " 5. Open http://localhost:8000 in your browser to access the Chat UI."
echo "==========================================="
