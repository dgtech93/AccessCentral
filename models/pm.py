"""
Modello Project Manager (PM)
"""

from typing import Optional, List
from .database import DatabaseManager


class PM:
    """Rappresenta un Project Manager"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", 
                 email: str = "", telefono: str = "", cellulare: str = ""):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefono = telefono
        self.cellulare = cellulare
    
    @staticmethod
    def create(db: DatabaseManager, nome: str, email: str = "", 
               telefono: str = "", cellulare: str = "") -> int:
        """
        Crea un nuovo PM nel database
        
        Args:
            db: Gestore del database
            nome: Nome del PM
            email: Email del PM
            telefono: Telefono del PM
            cellulare: Cellulare del PM
            
        Returns:
            ID del PM creato
        """
        query = """
            INSERT INTO pm (nome, email, telefono, cellulare)
            VALUES (?, ?, ?, ?)
        """
        return db.execute_update(query, (nome, email, telefono, cellulare))
    
    @staticmethod
    def get_all(db: DatabaseManager) -> List['PM']:
        """
        Recupera tutti i PM dal database
        
        Args:
            db: Gestore del database
            
        Returns:
            Lista di PM
        """
        query = "SELECT * FROM pm ORDER BY nome"
        rows = db.execute_query(query)
        
        pms = []
        for row in rows:
            pm = PM(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare']
            )
            pms.append(pm)
        
        return pms
    
    @staticmethod
    def get_by_id(db: DatabaseManager, pm_id: int) -> Optional['PM']:
        """
        Recupera un PM specifico per ID
        
        Args:
            db: Gestore del database
            pm_id: ID del PM
            
        Returns:
            PM trovato o None
        """
        query = "SELECT * FROM pm WHERE id = ?"
        rows = db.execute_query(query, (pm_id,))
        
        if rows:
            row = rows[0]
            return PM(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare']
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, pm_id: int, nome: str, 
               email: str = "", telefono: str = "", cellulare: str = "") -> bool:
        """
        Aggiorna un PM esistente
        
        Args:
            db: Gestore del database
            pm_id: ID del PM da aggiornare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE pm 
            SET nome = ?, email = ?, telefono = ?, cellulare = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome, email, telefono, cellulare, pm_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, pm_id: int) -> bool:
        """
        Elimina un PM
        
        Args:
            db: Gestore del database
            pm_id: ID del PM da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM pm WHERE id = ?"
        rowcount = db.execute_update(query, (pm_id,))
        return rowcount > 0
    
    @staticmethod
    def get_clienti_count(db: DatabaseManager, pm_id: int) -> int:
        """
        Conta quanti clienti sono associati a questo PM
        
        Args:
            db: Gestore del database
            pm_id: ID del PM
            
        Returns:
            Numero di clienti
        """
        query = "SELECT COUNT(*) as count FROM clienti WHERE pm_id = ?"
        rows = db.execute_query(query, (pm_id,))
        return rows[0]['count'] if rows else 0
    
    def __str__(self):
        return f"PM: {self.nome} (ID: {self.id})"
