@echo off
echo Pulizia cache icone Windows...
echo.

REM Termina Explorer
taskkill /f /im explorer.exe

REM Elimina i file di cache delle icone
cd /d %userprofile%\AppData\Local
del IconCache.db /a /f

cd /d %userprofile%\AppData\Local\Microsoft\Windows\Explorer
del iconcache*.db /a /f
del thumbcache*.db /a /f

REM Riavvia Explorer
start explorer.exe

echo.
echo Cache icone pulita! Riavvia il PC per completare.
pause
