"""
Modello Credenziale
"""

from typing import Optional, List
from .database import DatabaseManager


class Credenziale:
    """Rappresenta una credenziale di accesso a un servizio"""
    
    def __init__(self, id: Optional[int] = None, servizio_id: int = 0,
                 username: str = "", password: str = "", host: str = "",
                 porta: Optional[int] = None, note: str = "", rdp_configurata: bool = False):
        self.id = id
        self.servizio_id = servizio_id
        self.username = username
        self.password = password
        self.host = host
        self.porta = porta
        self.note = note
        self.rdp_configurata = rdp_configurata
    
    @staticmethod
    def create(db: DatabaseManager, servizio_id: int, username: str,
               password: str, host: str = "", porta: Optional[int] = None,
               note: str = "", rdp_configurata: bool = False) -> int:
        """
        Crea una nuova credenziale nel database
        
        Args:
            db: Gestore del database
            servizio_id: ID del servizio associato
            username: Nome utente
            password: Password
            host: Host/IP del servizio
            porta: Porta del servizio
            note: Note aggiuntive
            rdp_configurata: Se True, è una RDP già configurata da lanciare direttamente
            
        Returns:
            ID della credenziale creata
        """
        query = """
            INSERT INTO credenziali (servizio_id, username, password, host, porta, note, rdp_configurata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (servizio_id, username, password, 
                                         host, porta, note, 1 if rdp_configurata else 0))
    
    @staticmethod
    def get_by_servizio(db: DatabaseManager, servizio_id: int) -> List['Credenziale']:
        """
        Recupera tutte le credenziali di un servizio
        
        Args:
            db: Gestore del database
            servizio_id: ID del servizio
            
        Returns:
            Lista di credenziali del servizio
        """
        query = """
            SELECT * FROM credenziali 
            WHERE servizio_id = ?
            ORDER BY username
        """
        rows = db.execute_query(query, (servizio_id,))
        
        credenziali = []
        for row in rows:
            # Gestisci rdp_configurata con try-except per compatibilità
            try:
                rdp_conf = bool(row['rdp_configurata'])
            except (KeyError, IndexError):
                rdp_conf = False
            
            credenziale = Credenziale(
                id=row['id'],
                servizio_id=row['servizio_id'],
                username=row['username'],
                password=row['password'],
                host=row['host'],
                porta=row['porta'],
                note=row['note'],
                rdp_configurata=rdp_conf
            )
            credenziali.append(credenziale)
        
        return credenziali
    
    @staticmethod
    def get_by_id(db: DatabaseManager, credenziale_id: int) -> Optional['Credenziale']:
        """
        Recupera una credenziale specifica per ID
        
        Args:
            db: Gestore del database
            credenziale_id: ID della credenziale
            
        Returns:
            Credenziale trovata o None
        """
        query = "SELECT * FROM credenziali WHERE id = ?"
        rows = db.execute_query(query, (credenziale_id,))
        
        if rows:
            row = rows[0]
            # Gestisci rdp_configurata con try-except per compatibilità
            try:
                rdp_conf = bool(row['rdp_configurata'])
            except (KeyError, IndexError):
                rdp_conf = False
            
            return Credenziale(
                id=row['id'],
                servizio_id=row['servizio_id'],
                username=row['username'],
                password=row['password'],
                host=row['host'],
                porta=row['porta'],
                note=row['note'],
                rdp_configurata=rdp_conf
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, credenziale_id: int, username: str,
               password: str, host: str = "", porta: Optional[int] = None,
               note: str = "", rdp_configurata: bool = False) -> bool:
        """
        Aggiorna una credenziale esistente
        
        Args:
            db: Gestore del database
            credenziale_id: ID della credenziale da aggiornare
            username: Nuovo username
            password: Nuova password
            host: Nuovo host
            porta: Nuova porta
            note: Nuove note
            rdp_configurata: Se True, è una RDP già configurata
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE credenziali 
            SET username = ?, password = ?, host = ?, porta = ?, note = ?, rdp_configurata = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (username, password, host, 
                                             porta, note, 1 if rdp_configurata else 0, credenziale_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, credenziale_id: int) -> bool:
        """
        Elimina una credenziale
        
        Args:
            db: Gestore del database
            credenziale_id: ID della credenziale da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM credenziali WHERE id = ?"
        rowcount = db.execute_update(query, (credenziale_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"Credenziale: {self.username} @ {self.host or 'N/A'}"
