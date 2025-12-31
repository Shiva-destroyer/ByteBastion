#!/bin/bash
# Quick start script for ByteBastion

echo "Starting ByteBastion Security Suite..."
cd "$(dirname "$0")/src"
source ../venv/bin/activate
python main.py
