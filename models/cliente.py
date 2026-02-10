"""
Modello Cliente
"""

from typing import Optional, List
from .database import DatabaseManager


class Cliente:
    """Rappresenta un cliente con i suoi servizi e VPN"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", 
                 descrizione: str = "", vpn_exe_path: str = "", 
                 vpn_windows_name: str = "", pm_id: Optional[int] = None,
                 vpn_server: str = "", vpn_username: str = "", vpn_password: str = "",
                 vpn_port: Optional[int] = None, vpn_config_dir: str = "", 
                 vpn_procedure_dir: str = ""):
        self.id = id
        self.nome = nome
        self.descrizione = descrizione
        self.vpn_exe_path = vpn_exe_path
        self.vpn_windows_name = vpn_windows_name
        self.pm_id = pm_id
        self.vpn_server = vpn_server
        self.vpn_username = vpn_username
        self.vpn_password = vpn_password
        self.vpn_port = vpn_port
        self.vpn_config_dir = vpn_config_dir
        self.vpn_procedure_dir = vpn_procedure_dir
    
    @staticmethod
    def create(db: DatabaseManager, nome: str, descrizione: str = "", 
               vpn_exe_path: str = "", vpn_windows_name: str = "",
               pm_id: Optional[int] = None) -> int:
        """
        Crea un nuovo cliente nel database
        
        Args:
            db: Gestore del database
            nome: Nome del cliente
            descrizione: Descrizione opzionale
            vpn_exe_path: Percorso file .exe VPN
            vpn_windows_name: Nome VPN Windows
            pm_id: ID del PM di riferimento
            
        Returns:
            ID del cliente creato
        """
        query = """
            INSERT INTO clienti (nome, descrizione, vpn_exe_path, vpn_windows_name, pm_id)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (nome, descrizione, vpn_exe_path, 
                                         vpn_windows_name, pm_id))
    
    @staticmethod
    def get_all(db: DatabaseManager) -> List['Cliente']:
        """
        Recupera tutti i clienti dal database
        
        Args:
            db: Gestore del database
            
        Returns:
            Lista di clienti
        """
        query = "SELECT * FROM clienti ORDER BY nome"
        rows = db.execute_query(query)
        
        clienti = []
        for row in rows:
            cliente = Cliente(
                id=row['id'],
                nome=row['nome'],
                descrizione=row['descrizione'],
                vpn_exe_path=row['vpn_exe_path'],
                vpn_windows_name=row['vpn_windows_name'],
                pm_id=row['pm_id'] if 'pm_id' in row.keys() else None,
                vpn_server=row['vpn_server'] if 'vpn_server' in row.keys() else "",
                vpn_username=row['vpn_username'] if 'vpn_username' in row.keys() else "",
                vpn_password=row['vpn_password'] if 'vpn_password' in row.keys() else "",
                vpn_port=row['vpn_port'] if 'vpn_port' in row.keys() else None,
                vpn_config_dir=row['vpn_config_dir'] if 'vpn_config_dir' in row.keys() else "",
                vpn_procedure_dir=row['vpn_procedure_dir'] if 'vpn_procedure_dir' in row.keys() else ""
            )
            clienti.append(cliente)
        
        return clienti
    
    @staticmethod
    def get_by_id(db: DatabaseManager, cliente_id: int) -> Optional['Cliente']:
        """
        Recupera un cliente specifico per ID
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            
        Returns:
            Cliente trovato o None
        """
        query = "SELECT * FROM clienti WHERE id = ?"
        rows = db.execute_query(query, (cliente_id,))
        
        if rows:
            row = rows[0]
            return Cliente(
                id=row['id'],
                nome=row['nome'],
                descrizione=row['descrizione'],
                vpn_exe_path=row['vpn_exe_path'],
                vpn_windows_name=row['vpn_windows_name'],
                pm_id=row['pm_id'] if 'pm_id' in row.keys() else None,
                vpn_server=row['vpn_server'] if 'vpn_server' in row.keys() else "",
                vpn_username=row['vpn_username'] if 'vpn_username' in row.keys() else "",
                vpn_password=row['vpn_password'] if 'vpn_password' in row.keys() else "",
                vpn_port=row['vpn_port'] if 'vpn_port' in row.keys() else None,
                vpn_config_dir=row['vpn_config_dir'] if 'vpn_config_dir' in row.keys() else "",
                vpn_procedure_dir=row['vpn_procedure_dir'] if 'vpn_procedure_dir' in row.keys() else ""
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, cliente_id: int, nome: str, 
               descrizione: str = "", vpn_exe_path: str = "", 
               vpn_windows_name: str = "", pm_id: Optional[int] = None,
               vpn_server: str = "", vpn_username: str = "", vpn_password: str = "",
               vpn_port: Optional[int] = None, vpn_config_dir: str = "",
               vpn_procedure_dir: str = "") -> bool:
        """
        Aggiorna un cliente esistente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente da aggiornare
            nome: Nuovo nome
            descrizione: Nuova descrizione
            vpn_exe_path: Nuovo percorso VPN exe
            vpn_windows_name: Nuovo nome VPN Windows
            pm_id: ID del PM di riferimento
            vpn_server: Server VPN
            vpn_username: Username VPN
            vpn_password: Password VPN
            vpn_port: Porta VPN
            vpn_config_dir: Directory file configurazione
            vpn_procedure_dir: Directory procedura
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE clienti 
            SET nome = ?, descrizione = ?, vpn_exe_path = ?, 
                vpn_windows_name = ?, pm_id = ?,
                vpn_server = ?, vpn_username = ?, vpn_password = ?,
                vpn_port = ?, vpn_config_dir = ?, vpn_procedure_dir = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome, descrizione, vpn_exe_path, 
                                              vpn_windows_name, pm_id,
                                              vpn_server, vpn_username, vpn_password,
                                              vpn_port, vpn_config_dir, vpn_procedure_dir,
                                              cliente_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, cliente_id: int) -> bool:
        """
        Elimina un cliente (e tutti i servizi e credenziali associati)
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM clienti WHERE id = ?"
        rowcount = db.execute_update(query, (cliente_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"Cliente: {self.nome} (ID: {self.id})"
