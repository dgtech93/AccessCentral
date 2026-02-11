# AccessCentral v2.0

Applicazione desktop completa per la gestione di credenziali, servizi, risorse e contatti aziendali con **sistema di sicurezza avanzato** e **backup automatico**.

## 🌟 Caratteristiche Principali

### 🔐 Sicurezza (NEW v2.0)
- **Master Password**: Protezione accesso all'applicazione con autenticazione
- **Crittografia AES**: Tutte le password vengono criptate con Fernet (AES-256)
- **Generatore Password**: Crea password sicure con opzioni personalizzabili
- **Sistema Recupero**: Codice di recupero per reset password dimenticata
- **3 Tentativi**: Limite di tentativi di accesso con blocco automatico
- **PBKDF2HMAC**: Derivazione chiavi con 100.000 iterazioni

### 💾 Backup e Ripristino (NEW v2.0)
- **Backup Automatico**: Backup programmato del database
- **Gestione Completa**: Crea, ripristina, esporta ed elimina backup
- **Configurabile**: Imposta intervallo e numero massimo di backup
- **Pulizia Automatica**: Rimozione backup obsoleti
- **Backup di Sicurezza**: Creazione automatica prima del ripristino

### 🔍 Ricerca Globale (NEW v2.0)
- **Barra Ricerca**: Ricerca in tempo reale
- **Multi-Entità**: Cerca tra clienti, servizi e credenziali
- **Smart Filter**: Mostra tutti i servizi quando si filtra per cliente
- **Evidenziazione**: Risultati evidenziati nella struttura ad albero

### Gestione Clienti Avanzata
- **Organizzazione Clienti**: Gestisci i tuoi clienti con descrizioni dettagliate
- **PM di Riferimento**: Associa un Project Manager responsabile ad ogni cliente
- **Consulenti**: Assegna multipli consulenti a ciascun cliente con competenze specifiche
- **Rubrica Contatti**: Ogni cliente ha una rubrica dedicata con contatti completi

### Gestione Risorse
- **Project Manager (PM)**:
  - Nome, Email, Telefono, Cellulare
  - Visualizza clienti associati
  - Gestione completa da menu dedicato

- **Consulenti**:
  - Nome, Email, Telefono, Cellulare, Competenza
  - Associazione many-to-many con clienti
  - Tracciamento clienti gestiti

- **Contatti (Rubrica Cliente)**:
  - Nome, Email, Telefono, Cellulare, Ruolo
  - Organizzati per cliente
  - Gestione rapida e intuitiva

### Gestione Servizi e Credenziali
- **Servizi**: RDP, CRM, Web, Database, SSH, FTP, Altro
- **Credenziali Multiple**: Ogni servizio può avere N credenziali
- **Copia Password**: Doppio click per copiare password negli appunti

### Integrazione VPN e RDP
- **VPN EXE**: Lancia file VPN personalizzati (.exe)
- **VPN Windows Native**: Auto-detect e connessione a VPN configurate in Windows
- **RDP Diretto**: Connessione automatica a Remote Desktop

## 📊 Struttura Database

### Tabelle Principali
- **pm**: Project Manager con dati di contatto
- **consulenti**: Consulenti con competenze
- **clienti**: Clienti con PM riferimento e VPN
- **clienti_consulenti**: Associazione many-to-many clienti-consulenti
- **contatti**: Rubrica contatti per ogni cliente
- **servizi**: Servizi per cliente (tipizzati)
- **credenziali**: Credenziali per ogni servizio

### Relazioni
```
pm (1) ----< (N) clienti
clienti (N) ----< (N) consulenti
clienti (1) ----< (N) contatti
clienti (1) ----< (N) servizi
servizi (1) ----< (N) credenziali
```

## 🏗️ Architettura

Il progetto segue il pattern **MVC (Model-View-Controller)**:

```
CredenzialiSuite/
├── main.py                      # Entry point con sistema autenticazione
├── requirements.txt             # Dipendenze Python
├── .gitignore                   # Esclude file sensibili
│
├── models/                      # Modelli dati (Database)
│   ├── database.py             # Gestione database SQLite
│   ├── cliente.py              # Modello Cliente
│   ├── servizio.py             # Modello Servizio
│   ├── credenziale.py          # Modello Credenziale
│   ├── pm.py                   # Modello Project Manager
│   ├── consulente.py           # Modello Consulente
│   └── contatto.py             # Modello Contatto
│
├── views/                       # Interfaccia grafica (PyQt5)
│   ├── main_window.py          # Finestra principale e dialogs
│   ├── cliente_dialogs.py      # Dialog gestione clienti
│   ├── risorse_dialogs.py      # Dialog PM/Consulenti/Contatti
│   ├── security_dialogs.py     # 🆕 Dialog sicurezza (master password, generatore, recovery)
│   └── backup_dialog.py        # 🆕 Dialog gestione backup
│
├── controllers/                 # Logica business
│   ├── cliente_controller.py   # Controller clienti/servizi
│   ├── credenziale_controller.py # Controller credenziali (con crittografia)
│   └── risorse_controller.py   # Controller PM/Consulenti/Contatti
│
└── utils/                       # Utility
    ├── vpn_launcher.py         # Gestione VPN
    ├── rdp_launcher.py         # Gestione connessioni RDP
    ├── crypto_manager.py       # 🆕 Crittografia password (Fernet, PBKDF2, SHA256)
    └── backup_manager.py       # 🆕 Backup automatico e gestione

File Configurazione:
├── security_config.json         # Salt + hash master password + recovery code
├── backup_config.json          # Config backup automatico
└── credenziali_suite.db        # Database SQLite con password criptate
```

### Flusso Autenticazione (v2.0)

```
1. Avvio app → main.py
2. Verifica prima esecuzione
3. Se prima volta:
   ├── Master Password Dialog
   ├── Genera salt + deriva chiave
   ├── Genera codice recupero
   └── Salva in security_config.json
4. Se esistente:
   ├── Carica security_config.json
   ├── Master Password Dialog (3 tentativi)
   ├── Verifica hash password
   ├── Se ≥3 errori → Recovery Dialog
   └── Inizializza CryptoManager
5. Verifica backup necessario
6. Avvia MainWindow
```

## Installazione

### Prerequisiti

- Python 3.8 o superiore
- Windows (per funzionalità VPN e RDP native)

### Passi

1. Clona o scarica il progetto

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

**Dipendenze principali:**
- PyQt5 >= 5.15
- cryptography >= 41.0.0 (per crittografia password)

3. Avvia l'applicazione:
```bash
python main.py
```

### Prima Configurazione (v2.0)

Al primo avvio, ti verrà chiesto di:

1. **Impostare una Master Password**
   - Minimo 6 caratteri
   - Protegge l'accesso all'applicazione
   - Conferma la password

2. **Salvare il Codice di Recupero**
   - Formato: XXXX-XXXX-XXXX-XXXX
   - ⚠️ **IMPORTANTE**: Salvalo in un posto sicuro!
   - Necessario per recuperare accesso se dimentichi la password
   - Verrà mostrato **solo una volta**

3. **Configurare Backup Automatico** (opzionale)
   - Dal menu `Backup → Gestisci Backup`
   - Imposta intervallo (default: 1 giorno)
   - Numero massimo backup (default: 10)

## Utilizzo

### Accesso all'Applicazione (v2.0)

1. Inserisci la **Master Password** al login
2. Hai **3 tentativi** disponibili
3. Se dimentichi la password:
   - Clicca "Sì" quando richiesto
   - Inserisci il **Codice di Recupero**
   - Imposta una nuova password

### Ricerca Globale (v2.0)

1. Usa la **barra di ricerca** in alto
2. Digita almeno 2 caratteri
3. La ricerca filtra in tempo reale:
   - **Clienti**: Per nome
   - **Servizi**: Per nome, tipo o link
   - **Credenziali**: Per username, host o note
4. Filtrando per cliente vengono mostrati **tutti i suoi servizi**

### Sicurezza (v2.0)

**Generatore Password:**
1. Menu **Sicurezza → Genera Password**
2. Imposta:
   - Lunghezza (8-64 caratteri)
   - Maiuscole, Numeri, Simboli
3. Clicca **Genera** per nuova password
4. **Copia** o **Usa Password**

**Cambio Master Password:**
1. Menu **Sicurezza → Cambia Master Password**
2. Inserisci password corrente
3. Inserisci nuova password (minimo 6 caratteri)
4. Riavvia l'applicazione

### Backup (v2.0)

**Backup Manuale:**
1. Menu **Backup → Crea Backup**
2. Il backup viene salvato in `backups/`

**Gestione Backup:**
1. Menu **Backup → Gestisci Backup**
2. Visualizza lista backup con data/ora/dimensione
3. Azioni disponibili:
   - **Ripristina**: Ripristina database (backup automatico prima)
   - **Elimina**: Rimuovi backup obsoleti
   - **Crea Nuovo**: Backup manuale immediato

**Esporta Backup:**
1. Menu **Backup → Esporta Backup**
2. Scegli destinazione
3. Salva copia del database

**Configurazione:**
- Abilita/Disabilita backup automatico
- Imposta intervallo giorni (default: 1)
- Numero massimo backup (default: 10)

### Gestione Clienti

1. Clicca su **"➕ Nuovo Cliente"** per aggiungere un cliente
2. Compila i campi:
   - **Nome**: Nome del cliente (obbligatorio)
   - **Descrizione**: Descrizione opzionale
   - **VPN EXE**: Percorso del file .exe VPN (opzionale)
   - **VPN Windows**: Nome della VPN configurata in Windows (opzionale)

### Gestione Servizi

1. Seleziona un cliente
2. Click destro → **"Nuovo Servizio"**
3. Specifica:
   - **Nome**: Nome del servizio
   - **Tipo**: RDP, CRM, Web, Database, SSH, FTP, Altro
   - **Descrizione**: Informazioni aggiuntive

### Gestione Credenziali

1. Seleziona un servizio
2. Clicca **"➕ Nuova Credenziale"**
3. Inserisci:
   - **Username**: Nome utente (obbligatorio)
   - **Password**: Password (obbligatoria)
   - **Host/IP**: Indirizzo del server
   - **Porta**: Porta del servizio
   - **Note**: Note aggiuntive

### Funzionalità Avanzate

- **Copia Password**: Doppio click su una credenziale per copiare la password negli appunti
- **Lancia VPN**: Seleziona un cliente con VPN configurata e clicca sui bottoni VPN
- **Connetti RDP**: Seleziona una credenziale di un servizio RDP e clicca **"🖥️ Connetti RDP"**
- **Menu Contestuale**: Click destro su clienti/servizi per azioni rapide

## 🔒 Sicurezza

### Implementazioni v2.0

✅ **IMPLEMENTATE**:

- ✅ **Crittografia AES-256**: Tutte le password vengono criptate con Fernet
- ✅ **Master Password**: Autenticazione obbligatoria con hash SHA-256
- ✅ **Derivazione Chiavi**: PBKDF2HMAC con 100.000 iterazioni
- ✅ **Sistema Recupero**: Codice di recupero per password dimenticata
- ✅ **Limite Tentativi**: Blocco dopo 3 tentativi falliti
- ✅ **Generatore Password**: Crea password sicure personalizzabili
- ✅ **Backup Automatico**: Protezione dati con backup programmati

### Architettura Sicurezza

**Crittografia Password:**
```
Password in chiaro → Fernet.encrypt() → Base64 → Database
```

**Master Password:**
```
Password utente → PBKDF2HMAC (100k iter) → Chiave AES → Fernet cipher
Password utente → SHA-256 → Hash salvato in security_config.json
```

**Codice Recupero:**
```
16 caratteri alfanumerici → SHA-256 → Hash salvato in security_config.json
```

### Best Practices

⚠️ **IMPORTANTE**:

- 🔑 **Master Password**: Usa una password forte e memorabile
- 📝 **Codice Recupero**: Salvalo in un posto sicuro (cassaforte, password manager)
- 💾 **Backup Regolari**: Configura backup automatico giornaliero
- 🔒 **File Sensibili**: Non condividere `credenziali_suite.db` e `security_config.json`
- 🚫 **Git**: I file sensibili sono esclusi da .gitignore
- 🔄 **Password Esistenti**: Vengono criptate al primo salvataggio dopo aggiornamento

### File Sensibili

```
📁 CredenzialiSuite/
├── credenziali_suite.db      # Database criptato (gitignored)
├── security_config.json      # Config sicurezza (gitignored)
├── backup_config.json        # Config backup (gitignored)
└── backups/                  # Directory backup (gitignored)
    ├── accesscentral_backup_20260210_143022.db
    └── ...
```

## 🛠️ Tecnologie Utilizzate

- **Python 3.8+**: Linguaggio di programmazione
- **PyQt5 5.15+**: Framework GUI avanzato
- **SQLite 3**: Database embedded relazionale
- **cryptography**: Libreria crittografia (Fernet, PBKDF2HMAC) 🆕
- **MVC Pattern**: Architettura software modulare

### Dipendenze Chiave

```python
PyQt5>=5.15.0                  # GUI Framework
cryptography>=41.0.0           # Crittografia AES-256
```

### Algoritmi Crittografici (v2.0)

- **Fernet**: Crittografia simmetrica (AES-128 in CBC mode)
- **PBKDF2-HMAC-SHA256**: Key derivation (100.000 iterazioni)
- **SHA-256**: Hashing master password e recovery code
- **Base64**: Encoding chiavi e dati criptati

## Struttura Database

### Tabella `clienti`
- `id`: ID univoco
- `nome`: Nome cliente (unique)
- `descrizione`: Descrizione
- `vpn_exe_path`: Percorso VPN .exe
- `vpn_windows_name`: Nome VPN Windows
- Timestamps: `creato_il`, `modificato_il`

### Tabella `servizi`
- `id`: ID univoco
- `cliente_id`: FK a clienti
- `nome`: Nome servizio
- `tipo`: Tipo servizio
- `descrizione`: Descrizione
- Timestamps: `creato_il`, `modificato_il`

### Tabella `credenziali`
- `id`: ID univoco
- `servizio_id`: FK a servizi
- `username`: Nome utente
- `password`: Password
- `host`: Host/IP
- `porta`: Porta
- `note`: Note
- Timestamps: `creato_il`, `modificato_il`

## 📝 Changelog

### v2.0.0 (Febbraio 2026)

**🔐 Sicurezza**
- ✨ Sistema master password con autenticazione obbligatoria
- ✨ Crittografia AES-256 per tutte le password salvate
- ✨ Generatore password sicure con opzioni personalizzabili
- ✨ Sistema recupero password con codice di sicurezza (16 caratteri)
- ✨ Limite 3 tentativi con possibilità di recupero
- 🔧 PBKDF2HMAC con 100.000 iterazioni per derivazione chiavi
- 🔧 SHA-256 per hashing master password

**💾 Backup e Ripristino**
- ✨ Sistema backup automatico configurabile
- ✨ Gestione completa backup (crea, ripristina, esporta, elimina)
- ✨ Dialog gestione con tabella backup e dimensioni
- 🔧 Pulizia automatica backup obsoleti
- 🔧 Backup di sicurezza prima del ripristino
- 🔧 Configurazione intervallo e numero massimo backup

**🔍 Ricerca e UX**
- ✨ Barra ricerca globale in tempo reale
- ✨ Ricerca multi-entità (clienti, servizi, credenziali)
- ✨ Smart filter: mostra tutti i servizi quando si cerca un cliente
- 🔧 Ricerca case-insensitive con minimo 2 caratteri

**🎨 Interfaccia**
- 🔧 Layout VPN ridisegnato in griglia 2x2
- 🔧 Design moderno e professionale
- 🔧 Colori codificati per azioni (Blu=Nuovo, Rosso=Elimina, etc.)

**🐛 Bug Fix**
- 🔧 Correzione apertura directory VPN in Esplora Risorse
- 🔧 Fix verifica password corretta (non accettava più password errate)
- 🔧 Correzione attributi nel sistema di ricerca (url→link, email→host)
- 🔧 Fix TypeError nella selezione elementi ricerca (tuple→dict)

**📦 File Aggiunti**
- `utils/crypto_manager.py`: Gestione crittografia completa
- `utils/backup_manager.py`: Gestione backup automatici
- `views/security_dialogs.py`: Dialog sicurezza (master password, generatore, recovery)
- `views/backup_dialog.py`: Interfaccia gestione backup

**🔧 Dipendenze**
- ➕ `cryptography>=41.0.0`: Richiesta per funzionalità crittografia

### v1.x (Precedenti)
- Gestione clienti, servizi, credenziali
- Integrazione VPN e RDP
- Gestione PM, consulenti, contatti
- Database SQLite relazionale

## 📋 Licenza

Questo progetto è fornito "as-is" per uso personale o aziendale.

## Contributi

Per bug, suggerimenti o miglioramenti, apri una issue o una pull request.

## Note per Windows

- Le funzionalità VPN Windows utilizzano `rasdial` e PowerShell
- RDP utilizza `mstsc.exe` (incluso in Windows)
- Assicurati di avere i permessi necessari per eseguire questi comandi
