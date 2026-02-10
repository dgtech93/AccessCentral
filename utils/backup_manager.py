"""
Gestore backup automatico del database
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path


class BackupManager:
    """Gestisce i backup automatici del database"""
    
    def __init__(self, db_path: str, backup_dir: str = None):
        """
        Inizializza il gestore backup
        
        Args:
            db_path: Percorso del database da backuppare
            backup_dir: Directory dove salvare i backup (default: ./backups)
        """
        self.db_path = db_path
        self.backup_dir = backup_dir or os.path.join(os.path.dirname(db_path), "backups")
        self.config_file = os.path.join(os.path.dirname(db_path), "backup_config.json")
        
        # Crea directory backup se non esiste
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Carica configurazione
        self.config = self.carica_config()
    
    def carica_config(self) -> dict:
        """Carica la configurazione dei backup"""
        default_config = {
            "abilitato": True,
            "intervallo_giorni": 1,
            "max_backup": 10,
            "ultimo_backup": None
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                return default_config
        
        return default_config
    
    def salva_config(self):
        """Salva la configurazione dei backup"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def necessita_backup(self) -> bool:
        """
        Verifica se è necessario effettuare un backup
        
        Returns:
            True se servono backup
        """
        if not self.config["abilitato"]:
            return False
        
        ultimo_backup = self.config.get("ultimo_backup")
        if not ultimo_backup:
            return True
        
        try:
            data_ultimo = datetime.fromisoformat(ultimo_backup)
            giorni_passati = (datetime.now() - data_ultimo).days
            return giorni_passati >= self.config["intervallo_giorni"]
        except:
            return True
    
    def crea_backup(self) -> tuple:
        """
        Crea un backup del database
        
        Returns:
            Tupla (successo, percorso_backup, messaggio)
        """
        try:
            # Verifica che il database esista
            if not os.path.exists(self.db_path):
                return False, None, "Database non trovato"
            
            # Nome file backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"accesscentral_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copia il database
            shutil.copy2(self.db_path, backup_path)
            
            # Aggiorna configurazione
            self.config["ultimo_backup"] = datetime.now().isoformat()
            self.salva_config()
            
            # Pulisci vecchi backup
            self.pulisci_vecchi_backup()
            
            return True, backup_path, f"Backup creato: {backup_filename}"
        
        except Exception as e:
            return False, None, f"Errore durante il backup: {str(e)}"
    
    def pulisci_vecchi_backup(self):
        """Elimina i backup più vecchi se superano il limite"""
        try:
            # Ottieni lista backup ordinata per data
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("accesscentral_backup_") and file.endswith(".db"):
                    file_path = os.path.join(self.backup_dir, file)
                    mtime = os.path.getmtime(file_path)
                    backups.append((file_path, mtime))
            
            # Ordina per data (più recente prima)
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Elimina backup in eccesso
            max_backup = self.config["max_backup"]
            for file_path, _ in backups[max_backup:]:
                os.remove(file_path)
        
        except Exception as e:
            print(f"Errore pulizia backup: {e}")
    
    def ottieni_lista_backup(self) -> list:
        """
        Ottiene la lista dei backup disponibili
        
        Returns:
            Lista di tuple (percorso, data, dimensione)
        """
        backups = []
        
        try:
            for file in os.listdir(self.backup_dir):
                if file.startswith("accesscentral_backup_") and file.endswith(".db"):
                    file_path = os.path.join(self.backup_dir, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    size = os.path.getsize(file_path)
                    backups.append((file_path, mtime, size))
            
            # Ordina per data (più recente prima)
            backups.sort(key=lambda x: x[1], reverse=True)
        
        except Exception as e:
            print(f"Errore lettura backup: {e}")
        
        return backups
    
    def ripristina_backup(self, backup_path: str) -> tuple:
        """
        Ripristina un backup
        
        Args:
            backup_path: Percorso del backup da ripristinare
            
        Returns:
            Tupla (successo, messaggio)
        """
        try:
            if not os.path.exists(backup_path):
                return False, "File di backup non trovato"
            
            # Crea backup del database corrente prima di sovrascriverlo
            if os.path.exists(self.db_path):
                backup_corrente = f"{self.db_path}.before_restore"
                shutil.copy2(self.db_path, backup_corrente)
            
            # Ripristina il backup
            shutil.copy2(backup_path, self.db_path)
            
            return True, "Backup ripristinato con successo. Riavvia l'applicazione."
        
        except Exception as e:
            return False, f"Errore durante il ripristino: {str(e)}"
    
    def esporta_backup(self, destinazione: str) -> tuple:
        """
        Esporta un backup manuale in una posizione specifica
        
        Args:
            destinazione: Percorso dove salvare il backup
            
        Returns:
            Tupla (successo, messaggio)
        """
        try:
            if not os.path.exists(self.db_path):
                return False, "Database non trovato"
            
            shutil.copy2(self.db_path, destinazione)
            return True, f"Backup esportato in: {destinazione}"
        
        except Exception as e:
            return False, f"Errore durante l'esportazione: {str(e)}"
    
    def aggiorna_impostazioni(self, abilitato: bool = None, 
                             intervallo_giorni: int = None, 
                             max_backup: int = None):
        """
        Aggiorna le impostazioni dei backup
        
        Args:
            abilitato: Abilita/disabilita backup automatici
            intervallo_giorni: Giorni tra un backup e l'altro
            max_backup: Numero massimo di backup da mantenere
        """
        if abilitato is not None:
            self.config["abilitato"] = abilitato
        if intervallo_giorni is not None:
            self.config["intervallo_giorni"] = intervallo_giorni
        if max_backup is not None:
            self.config["max_backup"] = max_backup
        
        self.salva_config()
    
    def formato_dimensione(self, bytes: int) -> str:
        """
        Formatta la dimensione in MB/KB
        
        Args:
            bytes: Dimensione in bytes
            
        Returns:
            Stringa formattata
        """
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f} KB"
        else:
            return f"{bytes / (1024 * 1024):.1f} MB"
