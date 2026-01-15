@echo off
echo --- Installing Backend Dependencies ---
pip install -r backend/requirements.txt
echo.
echo --- Starting FastAPI Server ---
cd backend
python main.py
pause
