"""
Modello Servizio
"""

from typing import Optional, List
from .database import DatabaseManager


class Servizio:
    """Rappresenta un servizio associato a un cliente"""
    
    # Tipi di servizio supportati
    TIPO_RDP = "RDP"
    TIPO_CRM = "CRM"
    TIPO_WEB = "Web"
    TIPO_DATABASE = "Database"
    TIPO_SSH = "SSH"
    TIPO_FTP = "FTP"
    TIPO_ALTRO = "Altro"
    
    TIPI_DISPONIBILI = [TIPO_RDP, TIPO_CRM, TIPO_WEB, TIPO_DATABASE, 
                        TIPO_SSH, TIPO_FTP, TIPO_ALTRO]
    
    def __init__(self, id: Optional[int] = None, cliente_id: int = 0, 
                 nome: str = "", tipo: str = TIPO_ALTRO, descrizione: str = "", link: str = ""):
        self.id = id
        self.cliente_id = cliente_id
        self.nome = nome
        self.tipo = tipo
        self.descrizione = descrizione
        self.link = link
    
    @staticmethod
    def create(db: DatabaseManager, cliente_id: int, nome: str, 
               tipo: str, descrizione: str = "", link: str = "") -> int:
        """
        Crea un nuovo servizio nel database
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente proprietario
            nome: Nome del servizio
            tipo: Tipo di servizio
            descrizione: Descrizione opzionale
            link: Link/URL del servizio (per CRM, Web, etc.)
            
        Returns:
            ID del servizio creato
        """
        query = """
            INSERT INTO servizi (cliente_id, nome, tipo, descrizione, link)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (cliente_id, nome, tipo, descrizione, link))
    
    @staticmethod
    def get_by_cliente(db: DatabaseManager, cliente_id: int) -> List['Servizio']:
        """
        Recupera tutti i servizi di un cliente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            
        Returns:
            Lista di servizi del cliente
        """
        query = """
            SELECT * FROM servizi 
            WHERE cliente_id = ?
            ORDER BY tipo, nome
        """
        rows = db.execute_query(query, (cliente_id,))
        
        servizi = []
        for row in rows:
            # Gestisci link con try-except per compatibilità
            try:
                link_val = row['link'] or ""
            except (KeyError, IndexError):
                link_val = ""
            
            servizio = Servizio(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome=row['nome'],
                tipo=row['tipo'],
                descrizione=row['descrizione'],
                link=link_val
            )
            servizi.append(servizio)
        
        return servizi
    
    @staticmethod
    def get_by_id(db: DatabaseManager, servizio_id: int) -> Optional['Servizio']:
        """
        Recupera un servizio specifico per ID
        
        Args:
            db: Gestore del database
            servizio_id: ID del servizio
            
        Returns:
            Servizio trovato o None
        """
        query = "SELECT * FROM servizi WHERE id = ?"
        rows = db.execute_query(query, (servizio_id,))
        
        if rows:
            row = rows[0]
            # Gestisci link con try-except per compatibilità
            try:
                link_val = row['link'] or ""
            except (KeyError, IndexError):
                link_val = ""
            
            return Servizio(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome=row['nome'],
                tipo=row['tipo'],
                descrizione=row['descrizione'],
                link=link_val
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, servizio_id: int, nome: str, 
               tipo: str, descrizione: str = "", link: str = "") -> bool:
        """
        Aggiorna un servizio esistente
        
        Args:
            db: Gestore del database
            servizio_id: ID del servizio da aggiornare
            nome: Nuovo nome
            tipo: Nuovo tipo
            descrizione: Nuova descrizione
            link: Nuovo link
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE servizi 
            SET nome = ?, tipo = ?, descrizione = ?, link = ?, 
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome, tipo, descrizione, link, servizio_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, servizio_id: int) -> bool:
        """
        Elimina un servizio (e tutte le credenziali associate)
        
        Args:
            db: Gestore del database
            servizio_id: ID del servizio da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM servizi WHERE id = ?"
        rowcount = db.execute_update(query, (servizio_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"Servizio: {self.nome} ({self.tipo}) - ID: {self.id}"
