@echo off
call conda activate zeejay_agents
cd /d "C:\Users\Zohaib\Documents\ZeejayAI"
streamlit run app.py
if %errorlevel% neq 0 (
    echo An error occurred while running the Streamlit app.
    exit /b %errorlevel%
)