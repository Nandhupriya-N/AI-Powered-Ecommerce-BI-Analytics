@echo off
title Launching MasterMind AI (Enterprise Decision Intelligence)...
echo ============================================================
echo   Starting MasterMind AI: Autonomous Decision Intelligence
echo   Accessible on Desktop, Tablet & Mobile Devices
echo ============================================================
cd /d "c:\Users\Nandhupriya\BI PROJECT"
py -3.13 -m streamlit run app.py --server.address=0.0.0.0
pause
