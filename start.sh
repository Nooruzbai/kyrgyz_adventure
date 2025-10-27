#!/bin/bash

echo "Attempting to start FastAPI application..."
echo "---------------------------------------------------------------------"
echo "IMPORTANT: Make sure your '.venv' virtual environment is active!"
echo "If not, open a NEW terminal and run: "
echo "  cd /path/to/your/tournament_project"
echo "  source .venv/bin/activate"
echo "Then, in THAT terminal, run: ./start.sh"
echo "---------------------------------------------------------------------"
echo

# This line directly tries to run uvicorn.
# If .venv is not active or uvicorn is not installed, THIS LINE will show an error,
# but the script itself won't 'exit' and close your terminal.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app

# This line will be reached if uvicorn stops (e.g., Ctrl+C) or if the uvicorn command above fails.
echo "FastAPI application process finished or failed to start."