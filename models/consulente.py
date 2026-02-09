"""
Modello Consulente
"""

from typing import Optional, List
from .database import DatabaseManager


class Consulente:
    """Rappresenta un Consulente"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", 
                 email: str = "", telefono: str = "", cellulare: str = "",
                 competenza: str = ""):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefono = telefono
        self.cellulare = cellulare
        self.competenza = competenza
    
    @staticmethod
    def create(db: DatabaseManager, nome: str, email: str = "", 
               telefono: str = "", cellulare: str = "", competenza: str = "") -> int:
        """
        Crea un nuovo Consulente nel database
        
        Args:
            db: Gestore del database
            nome: Nome del consulente
            email: Email del consulente
            telefono: Telefono del consulente
            cellulare: Cellulare del consulente
            competenza: Competenza del consulente
            
        Returns:
            ID del consulente creato
        """
        query = """
            INSERT INTO consulenti (nome, email, telefono, cellulare, competenza)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (nome, email, telefono, cellulare, competenza))
    
    @staticmethod
    def get_all(db: DatabaseManager) -> List['Consulente']:
        """
        Recupera tutti i consulenti dal database
        
        Args:
            db: Gestore del database
            
        Returns:
            Lista di consulenti
        """
        query = "SELECT * FROM consulenti ORDER BY nome"
        rows = db.execute_query(query)
        
        consulenti = []
        for row in rows:
            consulente = Consulente(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare'],
                competenza=row['competenza']
            )
            consulenti.append(consulente)
        
        return consulenti
    
    @staticmethod
    def get_by_id(db: DatabaseManager, consulente_id: int) -> Optional['Consulente']:
        """
        Recupera un consulente specifico per ID
        
        Args:
            db: Gestore del database
            consulente_id: ID del consulente
            
        Returns:
            Consulente trovato o None
        """
        query = "SELECT * FROM consulenti WHERE id = ?"
        rows = db.execute_query(query, (consulente_id,))
        
        if rows:
            row = rows[0]
            return Consulente(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare'],
                competenza=row['competenza']
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, consulente_id: int, nome: str, 
               email: str = "", telefono: str = "", cellulare: str = "",
               competenza: str = "") -> bool:
        """
        Aggiorna un consulente esistente
        
        Args:
            db: Gestore del database
            consulente_id: ID del consulente da aggiornare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            competenza: Nuova competenza
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE consulenti 
            SET nome = ?, email = ?, telefono = ?, cellulare = ?, competenza = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome, email, telefono, cellulare, 
                                             competenza, consulente_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, consulente_id: int) -> bool:
        """
        Elimina un consulente
        
        Args:
            db: Gestore del database
            consulente_id: ID del consulente da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM consulenti WHERE id = ?"
        rowcount = db.execute_update(query, (consulente_id,))
        return rowcount > 0
    
    @staticmethod
    def get_by_cliente(db: DatabaseManager, cliente_id: int) -> List['Consulente']:
        """
        Recupera tutti i consulenti associati a un cliente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            
        Returns:
            Lista di consulenti
        """
        query = """
            SELECT c.* FROM consulenti c
            INNER JOIN clienti_consulenti cc ON c.id = cc.consulente_id
            WHERE cc.cliente_id = ?
            ORDER BY c.nome
        """
        rows = db.execute_query(query, (cliente_id,))
        
        consulenti = []
        for row in rows:
            consulente = Consulente(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare'],
                competenza=row['competenza']
            )
            consulenti.append(consulente)
        
        return consulenti
    
    @staticmethod
    def associa_a_cliente(db: DatabaseManager, cliente_id: int, consulente_id: int) -> bool:
        """
        Associa un consulente a un cliente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            consulente_id: ID del consulente
            
        Returns:
            True se l'associazione è riuscita
        """
        query = """
            INSERT OR IGNORE INTO clienti_consulenti (cliente_id, consulente_id)
            VALUES (?, ?)
        """
        db.execute_update(query, (cliente_id, consulente_id))
        return True
    
    @staticmethod
    def disassocia_da_cliente(db: DatabaseManager, cliente_id: int, consulente_id: int) -> bool:
        """
        Rimuove l'associazione tra un consulente e un cliente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            consulente_id: ID del consulente
            
        Returns:
            True se la rimozione è riuscita
        """
        query = """
            DELETE FROM clienti_consulenti 
            WHERE cliente_id = ? AND consulente_id = ?
        """
        rowcount = db.execute_update(query, (cliente_id, consulente_id))
        return rowcount > 0
    
    @staticmethod
    def get_clienti_count(db: DatabaseManager, consulente_id: int) -> int:
        """
        Conta quanti clienti sono associati a questo consulente
        
        Args:
            db: Gestore del database
            consulente_id: ID del consulente
            
        Returns:
            Numero di clienti
        """
        query = """
            SELECT COUNT(*) as count FROM clienti_consulenti 
            WHERE consulente_id = ?
        """
        rows = db.execute_query(query, (consulente_id,))
        return rows[0]['count'] if rows else 0
    
    def __str__(self):
        return f"Consulente: {self.nome} - {self.competenza} (ID: {self.id})"
