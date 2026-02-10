@echo off
chcp 65001 > nul
title AccessCentral v2.0 - Build Installer PyInstaller
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║      AccessCentral v2.0 - Build Installer Windows       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato!
    echo    Installa Python 3.8+ da https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python trovato
echo.

REM Verifica se siamo nel virtual environment
if not defined VIRTUAL_ENV (
    echo 🔍 Attivazione virtual environment...
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
        echo ✓ Virtual environment attivato
    ) else (
        echo ⚠️  Virtual environment non trovato
        echo    Usando Python globale...
    )
)
echo.

REM Installa PyInstaller se necessario
echo 📦 Verifica PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyInstaller non installato
    echo    Installazione in corso...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Errore installazione PyInstaller
        pause
        exit /b 1
    )
    echo ✓ PyInstaller installato
)
echo.

REM Esegui script di build
echo 🔨 Avvio build installer...
echo.
python build_installer.py

REM Controlla risultato
if %errorlevel% equ 0 (
    echo.
    echo ════════════════════════════════════════════════════════════
    echo ✅ BUILD COMPLETATA CON SUCCESSO!
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 📦 L'installer è stato creato nella cartella:
    echo    installer_AccessCentral_v2.0.0\
    echo.
    echo 📦 Archivio ZIP creato:
    echo    AccessCentral_v2.0.0_Windows_Installer.zip
    echo.
    echo 🚀 Pronto per la distribuzione!
    echo.
    
    REM Apri cartella installer
    echo 📂 Apertura cartella installer...
    explorer installer_AccessCentral_v2.0.0
    
) else (
    echo.
    echo ════════════════════════════════════════════════════════════
    echo ❌ BUILD FALLITA
    echo ════════════════════════════════════════════════════════════
    echo.
    echo Controlla gli errori sopra riportati
    echo.
)

echo.
echo Premi un tasto per chiudere...
pause >nul
