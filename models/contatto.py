"""
Modello Contatto (Rubrica del cliente)
"""

from typing import Optional, List
from .database import DatabaseManager


class Contatto:
    """Rappresenta un contatto nella rubrica di un cliente"""
    
    def __init__(self, id: Optional[int] = None, cliente_id: int = 0,
                 nome: str = "", email: str = "", telefono: str = "",
                 cellulare: str = "", ruolo: str = ""):
        self.id = id
        self.cliente_id = cliente_id
        self.nome = nome
        self.email = email
        self.telefono = telefono
        self.cellulare = cellulare
        self.ruolo = ruolo
    
    @staticmethod
    def create(db: DatabaseManager, cliente_id: int, nome: str,
               email: str = "", telefono: str = "", cellulare: str = "",
               ruolo: str = "") -> int:
        """
        Crea un nuovo contatto nel database
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente proprietario
            nome: Nome del contatto
            email: Email del contatto
            telefono: Telefono del contatto
            cellulare: Cellulare del contatto
            ruolo: Ruolo del contatto
            
        Returns:
            ID del contatto creato
        """
        query = """
            INSERT INTO contatti (cliente_id, nome, email, telefono, cellulare, ruolo)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (cliente_id, nome, email, telefono, 
                                         cellulare, ruolo))
    
    @staticmethod
    def get_by_cliente(db: DatabaseManager, cliente_id: int) -> List['Contatto']:
        """
        Recupera tutti i contatti di un cliente
        
        Args:
            db: Gestore del database
            cliente_id: ID del cliente
            
        Returns:
            Lista di contatti del cliente
        """
        query = """
            SELECT * FROM contatti 
            WHERE cliente_id = ?
            ORDER BY nome
        """
        rows = db.execute_query(query, (cliente_id,))
        
        contatti = []
        for row in rows:
            contatto = Contatto(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare'],
                ruolo=row['ruolo']
            )
            contatti.append(contatto)
        
        return contatti
    
    @staticmethod
    def get_by_id(db: DatabaseManager, contatto_id: int) -> Optional['Contatto']:
        """
        Recupera un contatto specifico per ID
        
        Args:
            db: Gestore del database
            contatto_id: ID del contatto
            
        Returns:
            Contatto trovato o None
        """
        query = "SELECT * FROM contatti WHERE id = ?"
        rows = db.execute_query(query, (contatto_id,))
        
        if rows:
            row = rows[0]
            return Contatto(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome=row['nome'],
                email=row['email'],
                telefono=row['telefono'],
                cellulare=row['cellulare'],
                ruolo=row['ruolo']
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, contatto_id: int, nome: str,
               email: str = "", telefono: str = "", cellulare: str = "",
               ruolo: str = "") -> bool:
        """
        Aggiorna un contatto esistente
        
        Args:
            db: Gestore del database
            contatto_id: ID del contatto da aggiornare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            ruolo: Nuovo ruolo
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = """
            UPDATE contatti 
            SET nome = ?, email = ?, telefono = ?, cellulare = ?, ruolo = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome, email, telefono, cellulare, 
                                             ruolo, contatto_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, contatto_id: int) -> bool:
        """
        Elimina un contatto
        
        Args:
            db: Gestore del database
            contatto_id: ID del contatto da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        query = "DELETE FROM contatti WHERE id = ?"
        rowcount = db.execute_update(query, (contatto_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"Contatto: {self.nome} - {self.ruolo}"
