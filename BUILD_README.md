# 🔨 Guida Build Installer - AccessCentral v2.0

Istruzioni per creare un installer standalone di AccessCentral per Windows.

---

## 📋 Prerequisiti

### Software Necessario

- **Python 3.8+** installato
- **Virtual Environment** attivo (consigliato)
- Connessione internet per scaricare dipendenze

### Dipendenze Python

```bash
# Installa dipendenze di sviluppo
pip install -r requirements-dev.txt
```

Dipendenze chiave:
- `PyInstaller>=5.13.0`: Per creare eseguibile standalone
- `cryptography>=41.0.0`: Libreria crittografia
- `PyQt5>=5.15.9`: Framework GUI

---

## 🚀 Metodo 1: Build Automatica (Consigliato)

### Windows - Doppio Click

1. **Doppio click** su `BUILD_PYINSTALLER.bat`
2. Attendi completamento build
3. L'installer sarà creato automaticamente

Lo script:
- ✅ Verifica dipendenze
- ✅ Installa PyInstaller se mancante
- ✅ Crea eseguibile standalone
- ✅ Crea package installer
- ✅ Crea archivio ZIP distribuibile

### Output

```
📦 installer_AccessCentral_v2.0.0/
   ├── AccessCentral.exe           (Eseguibile standalone ~50MB)
   ├── ISTRUZIONI.txt              (Guida utente)
   ├── README.md                   (Documentazione)
   ├── RELEASE_NOTES_v2.0.md       (Note di rilascio)
   └── Avvia_AccessCentral.bat     (Launcher rapido)

📦 AccessCentral_v2.0.0_Windows_Installer.zip  (Archivio distribuibile)
```

---

## 🔧 Metodo 2: Build Manuale

### Passo 1: Preparazione

```bash
# Attiva virtual environment
.venv\Scripts\activate

# Verifica dipendenze
pip list
```

### Passo 2: Esegui Script Python

```bash
python build_installer.py
```

### Passo 3: Verifica Output

```bash
# Verifica eseguibile creato
dir dist\AccessCentral.exe

# Verifica package installer
dir installer_AccessCentral_v2.0.0
```

---

## 📦 Struttura Build

### File Generati Durante Build

```
CredenzialiSuite/
├── build/                      # File temporanei build (cancellato)
├── dist/                       # Eseguibile finale
│   └── AccessCentral.exe
├── AccessCentral.spec          # File configurazione PyInstaller
├── version_info.txt            # Info versione Windows
└── installer_AccessCentral_v2.0.0/  # Package distribuibile
```

### File Esclusi (gitignore)

- `build/` - Directory temporanea
- `dist/` - Output build
- `*.spec` - File configurazione
- `installer_*/` - Package installer
- `*.zip` - Archivi

---

## ⚙️ Configurazione Avanzata

### Modifica File .spec

Se necessario personalizzare la build, modifica `AccessCentral.spec`:

```python
# Esempio: Aggiungere file extra
datas=[
    ('icon.ico', '.'),
    ('extra_file.txt', 'resources/'),
],

# Esempio: Escludere moduli
excludes=[
    'unnecessary_module',
],
```

### Ottimizzazioni

**Ridurre dimensione eseguibile:**

```python
# In AccessCentral.spec
excludes=[
    'matplotlib',  # Se non usato
    'pandas.plotting',  # Submoduli pandas non necessari
    'numpy.testing',
],

# Abilitare UPX compression
upx=True,
upx_exclude=['vcruntime140.dll'],
```

**Debug mode:**

```python
# In AccessCentral.spec
exe = EXE(
    ...
    console=True,  # Mostra console per debug
    debug=True,    # Abilita output debug
)
```

---

## 🧪 Testing Installer

### Test Eseguibile

1. **Esegui da directory dist:**
   ```bash
   cd dist
   AccessCentral.exe
   ```

2. **Verifica funzionalità:**
   - Login con master password
   - Creazione cliente/servizio/credenziale
   - Backup automatico
   - Generatore password
   - Ricerca globale
   - Cambio tema

3. **Test su PC pulito:**
   - Copia `installer_AccessCentral_v2.0.0/` su PC senza Python
   - Verifica che funzioni standalone

### Test Ambiente Pulito

Usa virtual environment separato:

```bash
# Crea nuovo venv
python -m venv test_env

# Attiva
test_env\Scripts\activate

# NON installare dipendenze (eseguibile deve essere standalone)

# Esegui
dist\AccessCentral.exe
```

---

## 🐛 Troubleshooting

### Errore: ModuleNotFoundError

**Causa**: Modulo non incluso in build

**Soluzione**: Aggiungi a `hiddenimports` in .spec file:

```python
hiddenimports=[
    'missing_module_name',
],
```

### Errore: FileNotFoundError per icon.ico

**Causa**: File icona mancante

**Soluzione**: 
- Crea icon.ico nella root del progetto, oppure
- Rimuovi `icon='icon.ico'` da .spec file

### Eseguibile non si avvia

**Debugging:**

1. Esegui con console abilitata:
   ```python
   # In .spec
   console=True,
   ```

2. Controlla dipendenze:
   ```bash
   pyinstaller --clean AccessCentral.spec
   ```

3. Verifica path file:
   ```python
   # In main.py, usa path relativi a __file__
   import os
   base_path = os.path.dirname(__file__)
   ```

### Build lenta

**Ottimizzazioni:**

1. Usa `--clean` solo quando necessario
2. Disabilita UPX se non serve compression
3. Escludi moduli non necessari
4. Usa disco SSD per build directory

---

## 📊 Dimensione Eseguibile

### Dimensioni Tipiche

- **Base (PyQt5 + Python)**: ~40-50 MB
- **Con Cryptography**: +10-15 MB
- **Con Pandas/Excel**: +20-30 MB
- **Totale atteso**: ~70-90 MB

### Compressione UPX

UPX può ridurre dimensione del 30-50%:

```python
# In .spec
upx=True,
upx_exclude=[
    'qwindows.dll',
    'Qt5Core.dll',
    'Qt5Gui.dll',
],
```

**Trade-off**: 
- ✅ File più piccolo
- ❌ Avvio leggermente più lento
- ❌ Alcuni antivirus potrebbero segnalare false positive

---

## 🚀 Distribuzione

### Checklist Pre-Rilascio

- [ ] Test su Windows 10
- [ ] Test su Windows 11
- [ ] Verifica dimensione file (< 100MB)
- [ ] Test primo avvio (setup master password)
- [ ] Test funzionalità principali
- [ ] Verifica ISTRUZIONI.txt chiare
- [ ] README.md aggiornato
- [ ] Release notes complete

### Canali Distribuzione

1. **GitHub Release**
   - Upload `AccessCentral_v2.0.0_Windows_Installer.zip`
   - Tag: `v2.0.0`
   - Release notes da RELEASE_NOTES_v2.0.md

2. **Download Diretto**
   - Hosting su server/cloud
   - Link diretto al ZIP

3. **Intranet Aziendale**
   - Copia package su share aziendale
   - Notifica utenti via email

### File da Distribuire

**Minimo (Solo Eseguibile):**
```
AccessCentral.exe
ISTRUZIONI.txt
```

**Consigliato (Package Completo):**
```
installer_AccessCentral_v2.0.0.zip  (contiene tutto)
```

**Opzionale (Documentazione Extra):**
```
README.md
RELEASE_NOTES_v2.0.md
```

---

## 🔄 Aggiornamento Versione

Per rilasciare una nuova versione:

1. **Aggiorna versione in build_installer.py:**
   ```python
   VERSION = "2.1.0"  # Nuova versione
   ```

2. **Aggiorna titolo finestra in views/main_window.py:**
   ```python
   self.setWindowTitle("AccessCentral v2.1 - Gestione Accessi")
   ```

3. **Crea tag Git:**
   ```bash
   git tag -a v2.1.0 -m "Release v2.1.0"
   git push origin v2.1.0
   ```

4. **Rebuild installer:**
   ```bash
   python build_installer.py
   ```

---

## 📝 Note Importanti

### Antivirus e SmartScreen

**Possibili Problemi:**
- Windows SmartScreen potrebbe bloccare eseguibile non firmato
- Alcuni antivirus potrebbero segnalare falsi positivi (specialmente con UPX)

**Soluzioni:**
1. **Code Signing Certificate** (consigliato per distribuzione commerciale)
   - Firma digitale eseguibile con certificato valido
   - Elimina avvisi SmartScreen
   - Costa ~100-300€/anno

2. **Whitelist manuale**
   - Istruisci utenti ad aggiungere eccezione
   - Include istruzioni in ISTRUZIONI.txt

3. **Build senza UPX**
   ```python
   upx=False,  # Riduce falsi positivi
   ```

### Compatibilità

- **Windows 10**: ✅ Completamente supportato
- **Windows 11**: ✅ Completamente supportato
- **Windows 8.1**: ⚠️ Potrebbe funzionare (non testato)
- **Windows 7**: ❌ Non supportato (manca supporto Qt)

### Licenze

Verifica licenze librerie incluse:
- PyQt5: GPL / Commercial
- Cryptography: Apache 2.0 / BSD
- Assicurati di rispettare termini licenza nella distribuzione

---

## 🆘 Supporto

### Problemi Build

1. Pulisci e ricostruisci:
   ```bash
   rmdir /s /q build dist
   python build_installer.py
   ```

2. Verifica requisiti:
   ```bash
   pip list
   ```

3. Controlla log PyInstaller:
   ```
   build/AccessCentral/warn-AccessCentral.txt
   ```

### Risorse Utili

- **PyInstaller Docs**: https://pyinstaller.org/en/stable/
- **PyQt5 Deployment**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **Windows Code Signing**: https://docs.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-cert-manage

### Contatti

- **GitHub Issues**: https://github.com/dgtech93/AccessCentral/issues
- **Repository**: https://github.com/dgtech93/AccessCentral

---

**Buona Build! 🚀**

*AccessCentral v2.0 - Build Guide - Febbraio 2026*
