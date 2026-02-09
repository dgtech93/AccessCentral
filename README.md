# AccessCentral v2.0

Applicazione desktop completa per la gestione di credenziali, servizi, risorse e contatti aziendali.

## 🌟 Caratteristiche Principali

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

## Architettura

Il progetto segue il pattern **MVC (Model-View-Controller)**:

```
CredenzialiSuite/
├── main.py                 # Entry point dell'applicazione
├── requirements.txt        # Dipendenze Python
├── models/                 # Modelli dati (Database)
│   ├── database.py        # Gestione database SQLite
│   ├── cliente.py         # Modello Cliente
│   ├── servizio.py        # Modello Servizio
│   └── credenziale.py     # Modello Credenziale
├── views/                  # Interfaccia grafica (PyQt5)
│   └── main_window.py     # Finestra principale e dialogs
├── controllers/            # Logica business
│   ├── cliente_controller.py
│   └── credenziale_controller.py
└── utils/                  # Utility
    ├── vpn_launcher.py    # Gestione VPN
    └── rdp_launcher.py    # Gestione connessioni RDP
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

3. Avvia l'applicazione:
```bash
python main.py
```

## Utilizzo

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

## Sicurezza

⚠️ **IMPORTANTE**:

- Il database SQLite salva le password in **chiaro**
- Per un ambiente di produzione, considera di implementare la crittografia
- Il file database (`credenziali_suite.db`) contiene dati sensibili
- Non condividere il file database
- Considera backup regolari del database

### Miglioramenti Futuri per la Sicurezza

- Implementare crittografia AES per le password
- Aggiungere autenticazione con password master
- Implementare auto-lock dopo inattività
- Aggiungere logging delle attività

## Tecnologie Utilizzate

- **Python 3**: Linguaggio di programmazione
- **PyQt5**: Framework GUI
- **SQLite**: Database embedded
- **MVC Pattern**: Architettura del software

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

## Licenza

Questo progetto è fornito "as-is" per uso personale o aziendale.

## Contributi

Per bug, suggerimenti o miglioramenti, apri una issue o una pull request.

## Note per Windows

- Le funzionalità VPN Windows utilizzano `rasdial` e PowerShell
- RDP utilizza `mstsc.exe` (incluso in Windows)
- Assicurati di avere i permessi necessari per eseguire questi comandi
