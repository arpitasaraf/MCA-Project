@echo off
title KPI Insight Backend Server
cd kpi-insight\kpi-insight-backend
echo Starting KPI Insight Backend Server...
npm start
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to start the backend server.
    echo Please make sure Node.js is installed.
    pause
)
