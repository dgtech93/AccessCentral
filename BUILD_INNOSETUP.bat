@echo off
REM ============================================================
REM AccessCentral v2.0 - Build Installer con Inno Setup
REM ============================================================

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║ AccessCentral v2.0 - Build Installer Inno Setup        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verifica se Inno Setup è installato
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo ❌ Inno Setup non trovato!
    echo.
    echo 📥 Scarica e installa Inno Setup da:
    echo    https://jrsoftware.org/isdl.php
    echo.
    echo Posizioni cercate:
    echo    - C:\Program Files (x86)\Inno Setup 6\ISCC.exe
    echo.
    pause
    exit /b 1
)

echo ✓ Inno Setup trovato
echo.

REM Verifica che dist\AccessCentral.exe esista
if not exist "dist\AccessCentral.exe" (
    echo ❌ Eseguibile non trovato!
    echo.
    echo 🔨 Prima di creare l'installer, devi generare l'eseguibile:
    echo    1. Esegui: BUILD_PYINSTALLER.bat
    echo    2. Oppure: python build_installer.py
    echo.
    pause
    exit /b 1
)

echo ✓ Eseguibile trovato: dist\AccessCentral.exe
echo.

REM Compila l'installer con Inno Setup
echo 🔨 Compilazione installer con Inno Setup...
echo    Questo potrebbe richiedere alcuni secondi...
echo.

"%INNO_PATH%" "installer.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║        ✅ INSTALLER CREATO CON SUCCESSO!                 ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo 📦 File creato in: Output\AccessCentral_v2.0_Setup.exe
    echo.
    echo 🚀 Puoi ora distribuire il file Setup.exe agli utenti!
    echo.
    
    REM Apri la cartella Output se esiste
    if exist "Output\" (
        echo 📂 Apertura cartella Output...
        start "" "Output\"
    )
) else (
    echo.
    echo ❌ Errore durante la compilazione!
    echo    Controlla il file installer.iss per eventuali errori.
    echo.
)

echo.
pause
