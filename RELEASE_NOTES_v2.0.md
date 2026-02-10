# 🎉 AccessCentral v2.0 - Release Notes

## Sistema di Sicurezza e Backup Automatico

**Data Release**: 10 Febbraio 2026

Siamo entusiasti di annunciare AccessCentral v2.0, una release importante che introduce funzionalità avanzate di sicurezza, backup automatico e miglioramenti significativi all'esperienza utente.

---

## 🔐 Novità Sicurezza

### Master Password
- **Autenticazione Obbligatoria**: Protezione dell'accesso all'applicazione
- **Prima Configurazione**: Setup guidato con conferma password
- **Login**: Dialog di accesso con opzione mostra/nascondi password
- **3 Tentativi**: Dopo 3 errori, possibilità di recupero password

### Crittografia Password
- **AES-256 (Fernet)**: Tutte le password vengono criptate
- **PBKDF2HMAC**: Derivazione chiavi con 100.000 iterazioni
- **Compatibilità**: Le password esistenti vengono criptate automaticamente al primo salvataggio
- **Trasparente**: Crittografia/decrittografia automatica

### Generatore Password
- **Lunghezza Personalizzabile**: 8-64 caratteri
- **Opzioni Flessibili**:
  - Lettere Maiuscole (A-Z)
  - Numeri (0-9)
  - Simboli (!@#$%...)
- **Copia Rapida**: Pulsante per copiare negli appunti
- **Usa Direttamente**: Integrazione con form credenziali

### Sistema Recupero Password
- **Codice di Recupero**: Generato alla prima configurazione (XXXX-XXXX-XXXX-XXXX)
- **Mostrato Una Volta**: Viene visualizzato solo durante setup iniziale
- **Reset Password**: Permette di impostare nuova master password
- **Sicurezza**: Codice salvato come hash SHA-256

---

## 💾 Novità Backup

### Backup Automatico
- **Programmabile**: Configura intervallo in giorni (default: 1 giorno)
- **All'Avvio**: Verifica e crea backup se necessario
- **Non Invasivo**: Esecuzione silenziosa in background

### Gestione Completa Backup
- **Interfaccia Grafica**: Dialog dedicato con tabella backup
- **Informazioni Dettagliate**:
  - Data e ora backup
  - Dimensione file
  - Percorso completo
- **Azioni Disponibili**:
  - **Crea**: Backup manuale immediato
  - **Ripristina**: Ripristina database (con backup di sicurezza automatico)
  - **Elimina**: Rimuovi backup obsoleti
  - **Esporta**: Salva backup in posizione personalizzata

### Configurazione Backup
- **Abilita/Disabilita**: Toggle backup automatico
- **Intervallo**: Imposta giorni tra backup (1-365)
- **Limite Backup**: Numero massimo backup conservati (1-100)
- **Pulizia Automatica**: Rimozione backup più vecchi del limite

### File Backup
- **Formato**: `accesscentral_backup_YYYYMMDD_HHMMSS.db`
- **Directory**: `backups/` nella cartella applicazione
- **Naming**: Timestamp per identificazione facile

---

## 🔍 Novità Ricerca

### Ricerca Globale
- **Barra Ricerca**: Posizionata sopra l'albero clienti
- **Real-Time**: Filtra mentre digiti (minimo 2 caratteri)
- **Multi-Entità**:
  - **Clienti**: Ricerca per nome
  - **Servizi**: Ricerca per nome, tipo o link
  - **Credenziali**: Ricerca per username, host o note

### Smart Filter
- **Ricerca Cliente**: Mostra cliente + **TUTTI** i suoi servizi
- **Ricerca Servizio**: Mostra solo servizi che matchano
- **Ricerca Credenziale**: Mostra indicatore numero credenziali trovate
- **Espansione Automatica**: Albero espanso per mostrare risultati

### UX Ricerca
- **Reset**: Cancellando testo si ripristina vista completa
- **Evidenziazione**: Risultati mostrati in struttura gerarchica
- **Icone**: Emoji per identificazione rapida (👤 clienti, 🔑 credenziali)
- **No Results**: Messaggio chiaro se nessun risultato trovato

---

## 🎨 Novità Temi

### 3 Temi Disponibili

#### Tema Chiaro (Microsoft-style) - **DEFAULT**
- Design pulito e professionale
- Alto contrasto per leggibilità
- Stile moderno Windows 11
- Ideale per ambienti luminosi

#### Tema Dark
- Sfondo scuro per ridurre affaticamento visivo
- Contrasto ottimizzato
- Perfetto per lavoro notturno
- Riduce emissioni luce blu

#### Tema Colorato
- Accenti vivaci e colorati
- Design originale con gradienti
- Personalità distintiva
- Per chi ama il colore

### Gestione Temi
- **Menu Visualizza → Temi**: Accesso rapido
- **Cambio Istantaneo**: Applicazione immediata
- **Persistenza**: Tema salvato in `config.json`
- **Ricordato**: Tema scelto viene riapplicato all'avvio

---

## 🔧 Miglioramenti

### VPN e Directory
- **Fix Apertura Directory**: Ora apre correttamente la directory impostata
- **Supporto File**: Se è un file, apre la cartella e lo seleziona
- **Normalizzazione Path**: Gestione corretta percorsi Windows
- **Validazione**: Verifica esistenza before apertura

### Layout VPN
- **Griglia 2x2**: Bottoni VPN organizzati in griglia
- **Stile Inline**: Styling moderno applicato direttamente
- **Spazio Ottimizzato**: Uso efficiente dello spazio
- **Icone Chiare**: Emoji per riconoscimento immediato

### Verifica Password
- **Fix Critico**: Non accettava più password errate (bug v1.x)
- **Verifica Corretta**: Confronto hash prima dell'inizializzazione
- **3 Tentativi**: Implementazione corretta del sistema a tentativi
- **Recovery Flow**: Proposta recupero dopo tentativi esauriti

### Ricerca Attributi
- **Fix Attributi**: Corretti attributi non esistenti
  - `servizio.url` → `servizio.link`
  - `credenziale.email` → `credenziale.host`
  - `credenziale.descrizione` → `credenziale.note`
- **Fix TypeError**: Risolto errore tuple vs dict nella selezione

---

## 📦 File Nuovi

### Moduli Core
```
utils/
├── crypto_manager.py (184 righe)
│   ├── CryptoManager: Classe principale crittografia
│   ├── genera_chiave_da_password(): PBKDF2HMAC
│   ├── inizializza_con_password(): Setup cipher
│   ├── cripta() / decripta(): Encrypt/decrypt password
│   ├── genera_password_sicura(): Generatore password
│   ├── genera_recovery_code(): Codice recupero 16 char
│   └── calcola_hash_password(): SHA-256 hashing
│
└── backup_manager.py (230 righe)
    ├── BackupManager: Classe gestione backup
    ├── crea_backup(): Crea nuovo backup
    ├── ripristina_backup(): Ripristina da backup
    ├── ottieni_lista_backup(): Lista backup disponibili
    ├── pulisci_vecchi_backup(): Pulizia automatica
    ├── necessita_backup(): Verifica se serve backup
    └── esporta_backup(): Esporta in posizione custom
```

### Dialog UI
```
views/
├── security_dialogs.py (400+ righe)
│   ├── MasterPasswordDialog: Login/setup master password
│   ├── GeneratorePasswordDialog: Generatore password UI
│   └── RecoveryCodeDialog: Inserimento codice recupero
│
└── backup_dialog.py (260 righe)
    └── BackupDialog: Gestione completa backup
        ├── Tabella backup con sorting
        ├── Configurazione (abilita, intervallo, max)
        ├── Azioni (crea, ripristina, elimina)
        └── Statistiche backup
```

### File Configurazione
```
security_config.json (gitignored)
├── salt: Sale per derivazione chiave (hex)
├── password_hash: Hash SHA-256 master password
└── recovery_code_hash: Hash SHA-256 codice recupero

backup_config.json (gitignored)
├── abilitato: true/false
├── intervallo_giorni: 1-365
├── max_backup: 1-100
└── ultimo_backup: timestamp ISO

config.json (gitignored)
└── tema: "chiaro" | "dark" | "colorato"
```

---

## 🔄 Modifiche File Esistenti

### main.py
- Aggiunto sistema autenticazione completo
- Gestione prima esecuzione con setup
- Verifica password con tentativi
- Flow recupero password integrato
- Inizializzazione backup manager
- Auto-backup all'avvio

### views/main_window.py
- Aggiunta barra ricerca globale
- Implementata funzione `ricerca_globale()`
- Menu Sicurezza (genera password, cambia master)
- Menu Backup (4 opzioni)
- Menu Temi (3 opzioni)
- Metodi gestione backup (7 metodi)
- Fix apertura directory VPN
- Aggiornato titolo finestra: "AccessCentral v2.0"

### controllers/credenziale_controller.py
- Integrazione CryptoManager
- Crittografia password in `crea_credenziale()`
- Crittografia password in `modifica_credenziale()`
- Decrittografia password in `ottieni_credenziali_servizio()`
- Decrittografia password in `ottieni_credenziale()`
- Backward compatibility per password esistenti

### .gitignore
- Aggiunto `security_config.json`
- Aggiunto `backup_config.json`
- Aggiunto `config.json`
- Aggiunto `backups/`

---

## 📋 Requisiti

### Software
- **Python**: 3.8 o superiore
- **Sistema Operativo**: Windows 10/11 (per VPN/RDP)
- **Spazio Disco**: ~50MB per app + backup

### Dipendenze Python
```bash
PyQt5>=5.15.0              # GUI framework
cryptography>=41.0.0       # Crittografia (NUOVA DIPENDENZA)
```

### Installazione Dipendenze
```bash
pip install -r requirements.txt
```

---

## ⚠️ Note Importanti

### Prima Installazione
1. **Backup Database**: Se hai già dati, fai backup di `credenziali_suite.db`
2. **Master Password**: Scegli una password forte e memorabile
3. **Codice Recupero**: Salvalo in un posto sicuro (es. password manager)
4. **File Sensibili**: `security_config.json` e database non devono essere condivisi

### Aggiornamento da v1.x
1. **Backup Automatico**: Al primo avvio, fai backup manuale
2. **Master Password**: Ti verrà chiesto di impostarla
3. **Password Esistenti**: Verranno criptate al primo salvataggio/modifica
4. **Compatibilità**: Le credenziali esistenti continuano a funzionare

### Recupero Password Dimenticata
1. Avvia applicazione
2. Sbaglia password 3 volte
3. Clicca "Sì" quando chiede se non ricordi password
4. Inserisci codice recupero salvato
5. Imposta nuova master password
6. **Se perdi codice recupero**: Non è possibile recuperare accesso

---

## 🐛 Bug Fix

### Critici
- ✅ **Verifica Password**: Non bloccava più accessi con password errata
- ✅ **Apertura Directory VPN**: Apriva directory sbagliate

### Funzionali
- ✅ **Ricerca attributi**: Usava attributi inesistenti (url, email, descrizione)
- ✅ **Selezione ricerca**: TypeError con tuple invece di dict
- ✅ **Filtro cliente**: Non mostrava tutti i servizi del cliente

---

## 🚀 Come Usare le Nuove Funzionalità

### Setup Iniziale (Solo Prima Volta)
```
1. Avvia AccessCentral
2. Imposta Master Password (min 6 caratteri)
3. Conferma Password
4. SALVA IL CODICE DI RECUPERO mostrato
5. Clicca OK
```

### Ricerca Rapida
```
1. Digita nella barra ricerca in alto
2. Vedi risultati in tempo reale
3. Clicca su risultato per visualizzare dettagli
4. Cancella testo per ripristinare vista completa
```

### Generare Password Sicura
```
1. Menu Sicurezza → Genera Password
2. Imposta lunghezza (8-64)
3. Seleziona tipi caratteri
4. Clicca "Genera"
5. Clicca "Usa Password" per applicare
```

### Backup Manuale
```
1. Menu Backup → Crea Backup
2. Conferma
3. Backup salvato in backups/
```

### Ripristino da Backup
```
1. Menu Backup → Gestisci Backup
2. Seleziona backup dalla tabella
3. Clicca "Ripristina"
4. Conferma (verrà creato backup corrente)
5. Riavvia applicazione
```

### Cambiare Tema
```
1. Menu Visualizza → Temi
2. Seleziona tema desiderato
3. Applicazione immediata
```

---

## 📊 Statistiche Release

- **Commit**: 2
- **File Modificati**: 13
- **File Aggiunti**: 4 (+ 3 config)
- **Righe Codice Aggiunte**: ~2100
- **Righe Documentazione**: ~300
- **Tempo Sviluppo**: ~15 ore
- **Bug Fix**: 5

---

## 🙏 Ringraziamenti

Grazie per aver scelto AccessCentral. Questa release rappresenta un importante passo avanti nella sicurezza e usabilità dell'applicazione.

Per bug report, feature request o domande:
- **GitHub Issues**: https://github.com/dgtech93/AccessCentral/issues
- **Repository**: https://github.com/dgtech93/AccessCentral

---

## 📅 Prossime Release

### Roadmap v2.1 (In Pianificazione)
- 🔄 Auto-lock dopo inattività
- 📝 Logging attività utente
- 🔍 Ricerca avanzata con filtri
- 📊 Dashboard statistiche
- 🔒 2FA autenticazione
- 🌐 Export/Import credenziali (formato sicuro)

---

**AccessCentral v2.0** - Sicurezza e Backup per le tue credenziali 🔐💾
