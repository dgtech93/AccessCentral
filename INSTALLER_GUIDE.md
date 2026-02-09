# AccessCentral - Guida Installazione

## 📦 Creazione dell'Installer Windows

### Prerequisiti

1. **Inno Setup** (gratuito)
   - Scarica da: https://jrsoftware.org/isdl.php
   - Installa la versione 6 o superiore
   - Consigliato: Inno Setup 6.3.3 o successivo

### Procedura Automatica

1. Assicurati che l'eseguibile sia stato creato:
   ```
   build_exe.bat
   ```

2. Crea l'installer:
   ```
   build_installer.bat
   ```

3. L'installer sarà disponibile in:
   ```
   installer_output\CredenzialiSuite_Setup.exe
   ```

### Procedura Manuale

1. Apri `installer.iss` con Inno Setup
2. Click su **Build** → **Compile**
3. L'installer sarà creato in `installer_output\`

### Caratteristiche dell'Installer

✅ **Installazione guidata** in italiano
✅ **Icona sul desktop** (opzionale)
✅ **Menu Start** con collegamenti
✅ **Disinstallazione** completa
✅ **Registrazione** in Programmi e Funzionalità
✅ **Database preservato** durante aggiornamenti
✅ **Non richiede permessi amministratore**

### Distribuzione

Il file `CredenzialiSuite_Setup.exe` è completamente standalone e può essere:
- Condiviso via email
- Caricato su un server
- Distribuito su chiavetta USB
- Pubblicato su siti di download

L'utente finale dovrà semplicemente:
1. Eseguire `CredenzialiSuite_Setup.exe`
2. Seguire la procedura guidata
3. Avviare il programma dal Menu Start o dall'icona desktop

### Personalizzazione

Per modificare l'installer, edita `installer.iss`:
- **Nome applicazione**: Riga `#define MyAppName`
- **Versione**: Riga `#define MyAppVersion`
- **Editore**: Riga `#define MyAppPublisher`
- **Cartella predefinita**: Sezione `[Setup]` → `DefaultDirName`

### Build Completa

Per creare tutto in un colpo solo:

```batch
REM 1. Crea l'eseguibile
build_exe.bat

REM 2. Crea l'installer
build_installer.bat
```

Oppure esegui entrambi i comandi in sequenza.
