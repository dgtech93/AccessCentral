"""
Gestione del database SQLite per l'applicazione
"""

import sqlite3
import os
from typing import List, Tuple, Optional


class DatabaseManager:
    """Gestisce tutte le operazioni sul database SQLite"""
    
    def __init__(self, db_path: str = "credenziali_suite.db"):
        """
        Inizializza il gestore del database
        
        Args:
            db_path: Percorso del file database
        """
        self.db_path = db_path
        self.connection = None
        self.initialize_database()
    
    def connect(self) -> sqlite3.Connection:
        """Crea una connessione al database"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Chiude la connessione al database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Crea le tabelle del database se non esistono"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Tabella PM (Project Manager)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pm (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                email TEXT,
                telefono TEXT,
                cellulare TEXT,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella Consulenti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consulenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                email TEXT,
                telefono TEXT,
                cellulare TEXT,
                competenza TEXT,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella Clienti (con pm_id)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clienti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descrizione TEXT,
                vpn_exe_path TEXT,
                vpn_windows_name TEXT,
                pm_id INTEGER,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pm_id) REFERENCES pm(id) ON DELETE SET NULL
            )
        """)
        
        # Tabella associativa Clienti-Consulenti (many-to-many)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clienti_consulenti (
                cliente_id INTEGER NOT NULL,
                consulente_id INTEGER NOT NULL,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (cliente_id, consulente_id),
                FOREIGN KEY (cliente_id) REFERENCES clienti(id) ON DELETE CASCADE,
                FOREIGN KEY (consulente_id) REFERENCES consulenti(id) ON DELETE CASCADE
            )
        """)
        
        # Tabella Contatti (Rubrica per ogni cliente)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                cellulare TEXT,
                ruolo TEXT,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clienti(id) ON DELETE CASCADE
            )
        """)
        
        # Tabella Servizi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servizi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                descrizione TEXT,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clienti(id) ON DELETE CASCADE,
                UNIQUE(cliente_id, nome)
            )
        """)
        
        # Tabella Credenziali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credenziali (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                servizio_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                host TEXT,
                porta INTEGER,
                note TEXT,
                creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (servizio_id) REFERENCES servizi(id) ON DELETE CASCADE
            )
        """)
        
        # Indici per migliorare le performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_contatti_cliente 
            ON contatti(cliente_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_servizi_cliente 
            ON servizi(cliente_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_credenziali_servizio 
            ON credenziali(servizio_id)
        """)
        
        conn.commit()
        
        # Migrazione: aggiungi colonne mancanti alle tabelle esistenti
        self.migrate_database()
        
        # Crea indice pm_id dopo la migrazione
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clienti_pm 
            ON clienti(pm_id)
        """)
        
        conn.commit()
    
    def migrate_database(self):
        """Esegue migrazioni per aggiornare database esistenti"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Controlla se la colonna pm_id esiste nella tabella clienti
            cursor.execute("PRAGMA table_info(clienti)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'pm_id' not in columns:
                # Aggiungi la colonna pm_id
                cursor.execute("ALTER TABLE clienti ADD COLUMN pm_id INTEGER")
                print("Migrazione: Aggiunta colonna pm_id alla tabella clienti")
            
            # Controlla se la colonna rdp_configurata esiste nella tabella credenziali
            cursor.execute("PRAGMA table_info(credenziali)")
            cred_columns = [row[1] for row in cursor.fetchall()]
            
            if 'rdp_configurata' not in cred_columns:
                # Aggiungi la colonna rdp_configurata (default 0 = false)
                cursor.execute("ALTER TABLE credenziali ADD COLUMN rdp_configurata INTEGER DEFAULT 0")
                print("Migrazione: Aggiunta colonna rdp_configurata alla tabella credenziali")
            
            # Controlla se la colonna link esiste nella tabella servizi
            cursor.execute("PRAGMA table_info(servizi)")
            servizi_columns = [row[1] for row in cursor.fetchall()]
            
            if 'link' not in servizi_columns:
                # Aggiungi la colonna link
                cursor.execute("ALTER TABLE servizi ADD COLUMN link TEXT")
                print("Migrazione: Aggiunta colonna link alla tabella servizi")
            
            # Controlla e aggiungi i nuovi campi VPN nella tabella clienti
            cursor.execute("PRAGMA table_info(clienti)")
            clienti_columns = [row[1] for row in cursor.fetchall()]
            
            if 'vpn_server' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_server TEXT")
                print("Migrazione: Aggiunta colonna vpn_server alla tabella clienti")
            
            if 'vpn_username' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_username TEXT")
                print("Migrazione: Aggiunta colonna vpn_username alla tabella clienti")
            
            if 'vpn_password' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_password TEXT")
                print("Migrazione: Aggiunta colonna vpn_password alla tabella clienti")
            
            if 'vpn_port' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_port INTEGER")
                print("Migrazione: Aggiunta colonna vpn_port alla tabella clienti")
            
            if 'vpn_config_dir' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_config_dir TEXT")
                print("Migrazione: Aggiunta colonna vpn_config_dir alla tabella clienti")
            
            if 'vpn_procedure_dir' not in clienti_columns:
                cursor.execute("ALTER TABLE clienti ADD COLUMN vpn_procedure_dir TEXT")
                print("Migrazione: Aggiunta colonna vpn_procedure_dir alla tabella clienti")
            
            conn.commit()
        except Exception as e:
            print(f"Errore durante la migrazione: {e}")
            conn.rollback()
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Esegue una query SELECT e restituisce i risultati
        
        Args:
            query: Query SQL da eseguire
            params: Parametri per la query
            
        Returns:
            Lista di risultati
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """
        Esegue una query di modifica (INSERT, UPDATE, DELETE)
        
        Args:
            query: Query SQL da eseguire
            params: Parametri per la query
            
        Returns:
            ID dell'ultima riga inserita o numero di righe modificate
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
