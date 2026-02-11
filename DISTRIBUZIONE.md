# 📦 Guida alla Distribuzione di AccessCentral v2.0

AccessCentral offre **due modalità di distribuzione** per soddisfare diverse esigenze.

---

## 🎯 Quale Metodo Scegliere?

| Caratteristica | PyInstaller (ZIP) | Inno Setup (Installer) |
|---------------|-------------------|------------------------|
| **Installazione** | ❌ Non richiesta | ✅ Wizard di installazione |
| **Portabilità** | ✅✅ Alta (basta estrarre) | ❌ Installa in Program Files |
| **Disinstallazione** | ❌ Manuale | ✅ Pannello di Controllo |
| **Integrazione Windows** | ❌ Nessuna | ✅ Menu Start, icone |
| **Dimensione** | ~40 MB (ZIP) | ~45 MB (Setup.exe) |
| **Aggiornamenti** | Manuale (sostituisci EXE) | Installa nuova versione |
| **Velocità Setup** | ⚡ Istantanea | 🐢 2-3 minuti |

### 📌 Raccomandazioni

- **👨‍💼 Utenti finali / Aziende**: Usa **Inno Setup Installer** (professionale, integrato)
- **🚀 Distribuzione rapida / Test**: Usa **PyInstaller ZIP** (veloce, portabile)
- **💻 Utilizzo personale**: Entrambi vanno bene (ZIP è più semplice)

---

## 📦 Metodo 1: PyInstaller (ZIP Standalone)

### ✅ Vantaggi
- **Nessuna installazione richiesta**
- **Portabile**: copia la cartella dove vuoi
- **Setup istantaneo**: estrai e lancia
- **Perfetto per test e sviluppo**

### 📥 Come Creare

1. **Esegui lo script di build:**
   ```batch
   BUILD_PYINSTALLER.bat
   ```
   Oppure:
   ```bash
   python build_installer.py
   ```

2. **Output generato:**
   ```
   📁 installer_AccessCentral_v2.0.0/
      ├── AccessCentral.exe         (eseguibile principale)
      ├── README.md                  (documentazione)
      ├── RELEASE_NOTES_v2.0.md     (note di rilascio)
      ├── ISTRUZIONI.txt            (guida rapida)
      └── Avvia_AccessCentral.bat   (launcher)
   
   📦 AccessCentral_v2.0.0_Windows_Installer.zip
   ```

### 🚀 Come Distribuire

1. **Invia agli utenti:**
   - `AccessCentral_v2.0.0_Windows_Installer.zip`

2. **Istruzioni per l'utente:**
   - Estrai lo ZIP in una cartella (es: `C:\AccessCentral`)
   - Doppio click su `AccessCentral.exe`
   - (Opzionale) Crea collegamento sul Desktop

### 🗑️ Come Disinstallare

- Elimina semplicemente la cartella estratta

---

## 🏗️ Metodo 2: Inno Setup (Installer Professionale)

### ✅ Vantaggi
- **Installer classico Windows** con wizard
- **Integrazione completa**: Start Menu, icone, disinstallazione
- **Professionale**: come Office, Chrome, ecc.
- **Gestione dipendenze automatica**

### 📥 Come Creare

#### **Prerequisito: Installa Inno Setup**

1. Scarica da: https://jrsoftware.org/isdl.php
2. Installa Inno Setup 6 (percorso default: `C:\Program Files (x86)\Inno Setup 6\`)

#### **Build dell'Installer**

**Metodo Automatico (Raccomandato):**
```batch
BUILD_INNOSETUP.bat
```

**Metodo Manuale:**
1. Genera prima l'eseguibile con PyInstaller:
   ```batch
   BUILD_PYINSTALLER.bat
   ```

2. Compila con Inno Setup:
   - Apri `installer.iss` con Inno Setup Compiler
   - Clicca **Build → Compile** (o premi `F9`)
   - Attendi compilazione (~30 secondi)

3. **Output generato:**
   ```
   📁 Output/
      └── AccessCentral_v2.0_Setup.exe   (~45 MB)
   ```

### 🚀 Come Distribuire

1. **Invia agli utenti:**
   - `Output\AccessCentral_v2.0_Setup.exe`

2. **Istruzioni per l'utente:**
   - Doppio click su `AccessCentral_v2.0_Setup.exe`
   - Segui il wizard di installazione
   - L'applicazione si installa in `C:\Program Files\AccessCentral v2.0\`
   - Icona nel Menu Start: "AccessCentral v2.0"

### 🗑️ Come Disinstallare

- **Pannello di Controllo** → Programmi e funzionalità → AccessCentral v2.0 → Disinstalla

**Opzioni durante disinstallazione:**
- Puoi scegliere se eliminare tutti i dati (database, backup, configurazioni)
- Oppure mantenerli per reinstallazioni future

---

## 🔧 Script di Build Disponibili

| Script | Descrizione | Output |
|--------|-------------|--------|
| `BUILD_PYINSTALLER.bat` | Build standalone con PyInstaller | ZIP portabile |
| `BUILD_INNOSETUP.bat` | Build installer con Inno Setup | Setup.exe |
| `build_installer.py` | Script Python per PyInstaller | ZIP portabile |
| `installer.iss` | Script Inno Setup | Setup.exe |

---

## 📋 Workflow Completo di Release

### 1️⃣ Preparazione
```bash
# Aggiorna versione in tutti i file necessari
# - main_window.py (setWindowTitle)
# - installer.iss (MyAppVersion)
# - build_installer.py (VERSION)
```

### 2️⃣ Build Applicazione
```batch
# Genera eseguibile standalone
BUILD_PYINSTALLER.bat
```

### 3️⃣ Build Installer (Opzionale)
```batch
# Genera installer Windows
BUILD_INNOSETUP.bat
```

### 4️⃣ Test
- **Testa ZIP**: Estrai e verifica funzionamento
- **Testa Setup**: Installa su macchina pulita

### 5️⃣ Commit e Tag
```bash
git add .
git commit -m "release: v2.0.1"
git tag -a v2.0.1 -m "Release v2.0.1"
git push origin main --tags
```

### 6️⃣ GitHub Release
1. Vai su: https://github.com/YOUR-REPO/releases/new
2. Seleziona tag: `v2.0.1`
3. Titolo: "AccessCentral v2.0.1"
4. Descrizione: Copia da `RELEASE_NOTES_v2.0.md`
5. **Carica file:**
   - `AccessCentral_v2.0.1_Windows_Installer.zip`
   - `AccessCentral_v2.0.1_Setup.exe` (se creato)
6. Pubblica release

---

## 🐛 Troubleshooting

### ❌ "PyInstaller non trovato"
```bash
.venv\Scripts\pip install pyinstaller
```

### ❌ "Inno Setup non trovato"
- Installa da: https://jrsoftware.org/isdl.php
- Verifica percorso: `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`

### ❌ "dist\AccessCentral.exe non trovato"
- Prima esegui `BUILD_PYINSTALLER.bat`
- Poi esegui `BUILD_INNOSETUP.bat`

### ❌ "Errore durante compilazione Inno Setup"
- Verifica che `installer.iss` non contenga errori
- Controlla che tutti i file sorgente esistano
- Apri `installer.iss` con Inno Setup IDE per vedere errori dettagliati

---

## 📝 Note Importanti

### 🔐 Sicurezza
- **IMPORTANTE**: I file `security_config.json` e `backup_config.json` **NON** sono inclusi nell'installer
- Vengono creati al primo avvio quando l'utente imposta la Master Password
- Questo garantisce che ogni installazione abbia credenziali uniche

### 💾 Database
- Il file `credenziali_suite.db` **NON** è incluso nell'installer
- Viene creato automaticamente al primo avvio
- Durante disinstallazione, l'utente può scegliere se mantenerlo o eliminarlo

### 📦 Dipendenze
- L'installer include **tutte** le dipendenze necessarie
- Non richiede Python installato sul sistema target
- Funziona su Windows 10/11 (64-bit)

---

## 🎯 Best Practices

1. **Testa sempre su macchina pulita** prima di distribuire
2. **Mantieni sincronizzate le versioni** in tutti i file
3. **Documenta i cambiamenti** in `RELEASE_NOTES`
4. **Usa Git tags** per ogni release
5. **Carica entrambi i formati** su GitHub Release (ZIP + Setup.exe)
6. **Includi checksum** per verificare integrità download

---

## 📞 Supporto

Per problemi durante la distribuzione:
1. Verifica i prerequisiti (Python, PyInstaller, Inno Setup)
2. Controlla i log di build per errori
3. Consulta `BUILD_README.md` per troubleshooting dettagliato
4. Apri una issue su GitHub se il problema persiste

---

**🚀 AccessCentral v2.0 - Secure Access Management**  
*© 2026 - Distribuzione semplificata per ogni esigenza*
