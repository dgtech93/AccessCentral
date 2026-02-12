# AccessCentral v2.2.1 - Release Notes

**Data rilascio**: 12 Febbraio 2026  
**Tipo**: Bugfix Release  
**Priorità**: Alta (funzionalità export Excel non funzionante in v2.2.0)

---

## 🐛 Bugfix Critici

### Export Excel Ripristinato

**Problema risolto**: In AccessCentral v2.2.0 l'export in formato Excel non funzionava a causa della mancata inclusione delle librerie `pandas` e `openpyxl` nel build PyInstaller.

**Comportamento precedente (v2.2.0)**:
- Click su "📊 Esporta Excel..." → Errore: "Errore: pandas e openpyxl non installati. Usa export CSV."
- Export Excel non disponibile nelle finestre Project Manager, Consulenti e Rubrica
- Workaround temporaneo: utilizzare export CSV

**Comportamento corretto (v2.2.1)**:
- ✅ Export Excel completamente funzionante
- ✅ Supporto per tutti i tipi di risorse (Clienti, Project Manager, Consulenti, Rubrica)
- ✅ File .xlsx generati correttamente con formattazione

**Modifiche tecniche**:
1. Aggiornato `build_installer.py`:
   - Rimosso `pandas` dalla lista `excludes` di PyInstaller
   - Aggiunto `pandas`, `openpyxl`, `openpyxl.cell`, `openpyxl.styles` agli `hiddenimports`
2. Ricompilato applicazione con librerie incluse
3. Dimensione eseguibile aumentata da 39.8 MB a 50.6 MB (+10.8 MB per supporto Excel)

---

## 📊 Impatto sulla Dimensione

| Componente | v2.2.0 | v2.2.1 | Differenza |
|------------|--------|--------|------------|
| Eseguibile standalone | 39.82 MB | 50.64 MB | +10.82 MB |
| ZIP Portable | 39.56 MB | 50.28 MB | +10.72 MB |
| Setup installer | 41.47 MB | 52.24 MB | +10.77 MB |

**Nota**: L'aumento di dimensione è dovuto all'inclusione delle librerie pandas e openpyxl necessarie per il supporto Excel.

---

## 🔧 Dettagli Tecnici

### Dipendenze Incluse

Le seguenti librerie Python sono ora correttamente incluse nell'eseguibile:

- **pandas** 3.0.0 - Libreria per manipolazione dati e export Excel
- **openpyxl** 3.1.5 - Engine per lettura/scrittura file .xlsx
- **numpy** 2.4.2 - Dipendenza di pandas per operazioni numeriche

### File Modificati

| File | Modifiche |
|------|-----------|
| `build_installer.py` | Aggiornato hiddenimports e excludes per PyInstaller |
| `installer.iss` | Versione aggiornata a 2.2.1 |

---

## 💾 Installazione

### Upgrade da v2.2.0

1. **Se hai installato v2.2.0 con installer**:
   - Esegui `AccessCentral_v2.2.1_Setup.exe`
   - L'installer sovrascriverà automaticamente la versione precedente
   - Database e configurazioni saranno preservati

2. **Se usi la versione portable v2.2.0**:
   - Estrai `AccessCentral_v2.2.1_Portable.zip` in una nuova cartella
   - Copia il file `credenziali_suite.db` dalla vecchia cartella alla nuova
   - Elimina la vecchia versione

**⚠️ Importante**: Il database è retrocompatibile. Non è necessaria alcuna migrazione.

---

## ✅ Test Consigliati Post-Installazione

Dopo l'upgrade, verifica il funzionamento dell'export Excel:

1. **Test Export Clienti**:
   - Vai a File → Esporta Excel...
   - Seleziona percorso di salvataggio
   - Verifica che il file .xlsx venga creato correttamente
   - Apri il file in Excel/LibreOffice per confermare i dati

2. **Test Export Rubrica**:
   - Vai a Risorse → Rubrica Cliente
   - Click su "📊 Export Excel"
   - Conferma che i Project Manager vengano esportati con tutte le colonne

3. **Test Export Consulenti**:
   - Vai a Risorse → Consulenti
   - Click su "📊 Export Excel"
   - Verifica l'esportazione con colonne: Nome, Email, Telefono, Azienda, Note

---

## 📦 Download

Sono disponibili due formati di distribuzione:

### 1. Setup Installer (Consigliato)
**File**: `AccessCentral_v2.2.1_Setup.exe` (52.24 MB)

**Caratteristiche**:
- Installazione guidata con wizard
- Desktop icon (opzionale)
- Voce nel menu Start
- Disinstallazione via Pannello di Controllo
- Aggiornamento automatico da v2.2.0

**Per chi?**: Utenti che desiderano un'installazione tradizionale Windows

### 2. Portable Edition
**File**: `AccessCentral_v2.2.1_Portable.zip` (50.28 MB)

**Caratteristiche**:
- Nessuna installazione richiesta
- Eseguibile standalone + batch di avvio
- Ideale per USB/cartelle di rete
- Database separato (portabile)

**Per chi?**: Utenti che preferiscono versioni no-install o deployment USB

---

## 🔗 Compatibilità

- **Windows**: 10, 11 (64-bit)
- **Python**: Non richiesto (eseguibile standalone)
- **Database**: SQLite 3.x (retrocompatibile con v2.0, v2.1, v2.2.0)
- **Excel**: File .xlsx compatibili con Microsoft Excel 2010+, LibreOffice Calc 6.0+, Google Sheets

---

## 📝 Note di Versione

### v2.2.1 (12 Feb 2026) - Bugfix
- **Bugfix**: Export Excel ora funzionante (inclusione pandas/openpyxl)
- **Build**: Dimensione aumentata per supporto librerie Excel

### v2.2.0 (11 Feb 2026) - Feature Release
- Template Cliente per strutture ricorrenti
- Gestione Allegati documenti per cliente
- Sistema template semplificato (rimossa gestione credenziali predefinite)

### v2.1.0 (Precedente)
- Sistema Template Servizi
- Import/Export CSV/Excel (funzionalità base)

### v2.0.0 (Precedente)
- Crittografia AES-256
- Gestione completa clienti, servizi, credenziali
- Ricerca globale avanzata

---

## 🆘 Supporto

Se riscontri problemi con v2.2.1:

1. **Verifica versione**: Apri AccessCentral → Info → Controlla che mostri "v2.2.1"
2. **Test export**: Prova export Excel su un database di test
3. **Issue GitHub**: Segnala problemi su https://github.com/dgtech93/AccessCentral/issues

---

## 🎯 Prossimi Sviluppi (Roadmap v2.3)

- Import Excel migliorato con validazione schemi
- Export template cliente su Excel (backup/restore strutture)
- Statistiche visuali su risorse e credenziali
- Auto-backup programmato

---

**Grazie per aver scelto AccessCentral!**

*Per la documentazione completa, consulta README.md e RELEASE_NOTES_v2.2.md*
