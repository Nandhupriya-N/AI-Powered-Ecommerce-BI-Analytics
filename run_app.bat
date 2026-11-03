@echo off
title Launching AI E-Commerce BI Platform (Desktop & Mobile Ready)...
echo ============================================================
echo   Starting AI E-Commerce BI & Predictive Analytics Platform
echo   Accessible on Desktop, Tablet & Mobile Devices
echo ============================================================
cd /d "c:\Users\Nandhupriya\BI PROJECT"
py -3.13 -m streamlit run app.py --server.address=0.0.0.0
pause
