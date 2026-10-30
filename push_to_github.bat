@echo off
title Push to GitHub - Fake News Detection ML
echo ============================================================
echo   Pushing Project to GitHub:
echo   https://github.com/neeleshphani/Fakenews-Detection-using-ML
echo ============================================================
echo.

cd /d "C:\Users\Phani\OneDrive\Desktop\Fakenews_ml"
"C:\Users\Phani\AppData\Local\Programs\Git\cmd\git.exe" push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================================
    echo   SUCCESS! All project files are live on GitHub!
    echo   View: https://github.com/neeleshphani/Fakenews-Detection-using-ML
    echo ============================================================
) else (
    echo ============================================================
    echo   Authentication needed. If a browser window opened,
    echo   please click "Sign in with your browser" to authorize.
    echo ============================================================
)
echo.
pause
