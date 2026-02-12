# 📋 Istruzioni Creazione Release v2.2.0 su GitHub

## File Preparati
✅ Codice committato e pushato su main
✅ Tag v2.2.0 creato e pushato
✅ Release notes RELEASE_NOTES_v2.2.md creato
✅ Installer ZIP creato: AccessCentral_v2.2.0_Windows_Installer.zip (39.5 MB)

## Procedura Creazione Release

### 1. Accedi a GitHub
Vai su: https://github.com/dgtech93/AccessCentral

### 2. Naviga alla Sezione Releases
- Click su "Releases" nella sidebar destra
- Oppure vai direttamente a: https://github.com/dgtech93/AccessCentral/releases

### 3. Crea Nuova Release
- Click su "Draft a new release"

### 4. Compila i Campi

**Tag:**
- Seleziona tag esistente: `v2.2.0`
- Oppure digita: `v2.2.0` (se disponibile nell'elenco)

**Release Title:**
```
AccessCentral v2.2.0 - Template Cliente e Gestione Allegati
```

**Description:**
Copia e incolla il contenuto di `RELEASE_NOTES_v2.2.md` oppure usa questo sommario:

```markdown
## 🎉 AccessCentral v2.2 - Template Cliente e Allegati

### ✨ Novità Principali

**👥 Template Cliente**
- Sistema completo per clienti ricorrenti
- Crea cliente + N servizi in 1 click
- Dialog gestione completa con associazione servizi
- Workflow semplificato e produttivo

**📎 Gestione Allegati**
- Upload documenti, contratti, immagini per cliente
- Organizzazione in cartella dedicata per cliente
- Azioni: Apri, Download, Elimina
- Context menu "Gestisci Allegati..."

**📋 Template Servizi Semplificato**
- Rimossa gestione credenziali predefinite
- Focus su configurazione servizio
- Più chiaro e user-friendly

### 🗄️ Database
- +3 tabelle: template_cliente, template_cliente_servizi, allegati
- +3 modelli completi
- +20 metodi controller
- Migrazione automatica

### 🎨 UI
- 5 nuovi dialog completi
- Menu "Gestione Template Cliente"
- Pulsante "📋 Da Template"
- Context menu "Gestisci Allegati..."

### 🐛 Bug Fix
- Fix campi allegati (creato_il, dimensione_kb)
- Fix gestione template semplificata
- 10+ correzioni varie

### 📦 Download
Scarica `AccessCentral_v2.2.0_Windows_Installer.zip` qui sotto

### 🚀 Installazione
1. Estrai ZIP in cartella desiderata
2. Esegui `Avvia_AccessCentral.bat` o `AccessCentral.exe`
3. (Opzionale) Crea collegamento desktop

### ⚠️ Aggiornamento da v2.0/v2.1
1. **BACKUP** database: copia `access_central.db`
2. Sostituisci eseguibile con v2.2.0
3. Al primo avvio: migrazione automatica database

### 📚 Documentazione Completa
Vedi `RELEASE_NOTES_v2.2.md` per dettagli completi.

---

**Data Release**: 11 Febbraio 2026
**Codice**: +1676 righe | 11 file modificati | 5 file nuovi
```

### 5. Upload File Installer

**File da caricare:**
- Nome: `AccessCentral_v2.2.0_Windows_Installer.zip`
- Percorso: `C:\Users\d.giotta\Desktop\CredenzialiSuite\AccessCentral_v2.2.0_Windows_Installer.zip`
- Dimensione: 39.5 MB

**Come caricare:**
1. Nella sezione "Attach binaries" clicca "Attach files by dragging & dropping, selecting or pasting them"
2. Trascina il file ZIP o selezionalo dal file browser
3. Aspetta il completamento upload (barra progresso)
4. Verifica che appaia nell'elenco asset

### 6. Configurazione Opzionale

**Pre-release:**
- ☐ Non spuntare (release stabile)

**Latest release:**
- ☑ Spunta "Set as the latest release"

**Create a discussion:**
- ☐ Opzionale: crea discussion per feedback community

### 7. Pubblica Release
- Click su "Publish release" (pulsante verde)
- Attendi conferma pubblicazione
- Verifica release visibile in: https://github.com/dgtech93/AccessCentral/releases

## Verifica Post-Pubblicazione

### 1. Check Release Page
- [ ] Titolo corretto: "AccessCentral v2.2.0 - Template Cliente e Gestione Allegati"
- [ ] Tag: v2.2.0
- [ ] Descrizione formattata correttamente
- [ ] Asset ZIP presente e scaricabile
- [ ] Badge "Latest" visibile

### 2. Test Download
- [ ] Download ZIP da release page
- [ ] Estrai contenuto
- [ ] Verifica eseguibile funzionante
- [ ] Test funzionalità base

### 3. Aggiorna README (Se Necessario)
Se il README principale ha sezione "Installation":
- Aggiorna link download alla v2.2.0
- Aggiorna badge versione (se presente)

## Link Utili

**Repository**: https://github.com/dgtech93/AccessCentral
**Releases**: https://github.com/dgtech93/AccessCentral/releases
**Issues**: https://github.com/dgtech93/AccessCentral/issues
**Tag v2.2.0**: https://github.com/dgtech93/AccessCentral/releases/tag/v2.2.0

## Note

- Il tag v2.2.0 è già stato creato e pushato
- Il codice v2.2 è già su branch main
- Il file ZIP è pronto per l'upload
- Le release notes complete sono in RELEASE_NOTES_v2.2.md

---

**Creato**: 11 Febbraio 2026
**Versione**: v2.2.0
**Build**: AccessCentral_v2.2.0_Windows_Installer.zip
