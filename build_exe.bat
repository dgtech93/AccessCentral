@echo off
echo ============================================
echo  AccessCentral - Build Eseguibile
echo ============================================
echo.

REM Verifica se PyInstaller è installato
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller non trovato. Installazione in corso...
    pip install pyinstaller
    echo.
)

echo Creazione dell'eseguibile in corso...
echo.

REM Crea l'eseguibile
pyinstaller --name="CredenzialiSuite" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "credenziali_suite.db;." ^
    --hidden-import=PyQt5 ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --noconsole ^
    main.py

echo.
echo ============================================
echo Build completata!
echo L'eseguibile si trova in: dist\CredenzialiSuite.exe
echo ============================================
echo.
pause
