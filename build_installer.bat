@echo off
echo ============================================
echo  AccessCentral - Creazione Installer
echo ============================================
echo.

REM Verifica che l'eseguibile esista
if not exist "dist\CredenzialiSuite.exe" (
    echo ERRORE: Eseguibile non trovato in dist\CredenzialiSuite.exe
    echo Esegui prima build_exe.bat per creare l'eseguibile
    echo.
    pause
    exit /b 1
)

REM Verifica se Inno Setup è installato
set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_PATH% (
    set INNO_PATH="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %INNO_PATH% (
    echo.
    echo ============================================
    echo  Inno Setup non trovato!
    echo ============================================
    echo.
    echo Per creare l'installer, devi prima installare Inno Setup:
    echo.
    echo 1. Scarica Inno Setup da: https://jrsoftware.org/isdl.php
    echo 2. Installa Inno Setup (versione 6 o superiore)
    echo 3. Esegui nuovamente questo script
    echo.
    echo ALTERNATIVA: Apri il file installer.iss con Inno Setup
    echo e compila manualmente (Build ^> Compile)
    echo.
    pause
    exit /b 1
)

echo Inno Setup trovato!
echo Creazione installer in corso...
echo.

REM Crea la cartella output se non esiste
if not exist "installer_output" mkdir installer_output

REM Compila l'installer
%INNO_PATH% "installer.iss"

if errorlevel 1 (
    echo.
    echo ERRORE durante la creazione dell'installer!
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Installer creato con successo!
echo ============================================
echo.
echo L'installer si trova in: installer_output\CredenzialiSuite_Setup.exe
echo.
echo Puoi distribuire questo file per installare il programma
echo su qualsiasi PC Windows.
echo.
pause
