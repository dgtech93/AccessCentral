"""
Modello per le credenziali predefinite nei template servizio
"""

from typing import List, Optional
from models.database import DatabaseManager


class TemplateCredenziale:
    """Rappresenta una credenziale predefinita per un template servizio"""
    
    def __init__(self, id: Optional[int] = None, template_servizio_id: int = 0,
                 username: str = "", password: str = "", host: str = "",
                 porta: Optional[int] = None, dominio: str = "", link: str = "", note: str = ""):
        self.id = id
        self.template_servizio_id = template_servizio_id
        self.username = username
        self.password = password
        self.host = host
        self.porta = porta
        self.dominio = dominio
        self.link = link
        self.note = note
    
    @staticmethod
    def create(db: DatabaseManager, template_servizio_id: int, username: str = "",
               password: str = "", host: str = "", porta: Optional[int] = None,
               dominio: str = "", link: str = "", note: str = "") -> int:
        """Crea una nuova credenziale template"""
        query = """
            INSERT INTO template_credenziali 
            (template_servizio_id, username, password, host, porta, dominio, link, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (template_servizio_id, username, password,
                                         host, porta, dominio, link, note))
    
    @staticmethod
    def get_by_template_servizio(db: DatabaseManager, template_servizio_id: int) -> List['TemplateCredenziale']:
        """Recupera tutte le credenziali di un template servizio"""
        query = "SELECT * FROM template_credenziali WHERE template_servizio_id = ?"
        rows = db.execute_query(query, (template_servizio_id,))
        
        credenziali = []
        for row in rows:
            # Gestione retrocompatibilità per campo link
            try:
                link = row['link'] or ""
            except (KeyError, IndexError):
                link = ""
            
            cred = TemplateCredenziale(
                id=row['id'],
                template_servizio_id=row['template_servizio_id'],
                username=row['username'] or "",
                password=row['password'] or "",
                host=row['host'] or "",
                porta=row['porta'],
                dominio=row['dominio'] or "",
                link=link,
                note=row['note'] or ""
            )
            credenziali.append(cred)
        
        return credenziali
    
    @staticmethod
    def get_by_id(db: DatabaseManager, id: int) -> Optional['TemplateCredenziale']:
        """Recupera una credenziale template per ID"""
        query = "SELECT * FROM template_credenziali WHERE id = ?"
        rows = db.execute_query(query, (id,))
        
        if rows:
            row = rows[0]
            # Gestione retrocompatibilità per campo link
            try:
                link = row['link'] or ""
            except (KeyError, IndexError):
                link = ""
            
            return TemplateCredenziale(
                id=row['id'],
                template_servizio_id=row['template_servizio_id'],
                username=row['username'] or "",
                password=row['password'] or "",
                host=row['host'] or "",
                porta=row['porta'],
                dominio=row['dominio'] or "",
                link=link,
                note=row['note'] or ""
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, id: int, username: str = "", password: str = "",
               host: str = "", porta: Optional[int] = None, dominio: str = "",
               link: str = "", note: str = "") -> bool:
        """Aggiorna una credenziale template"""
        query = """
            UPDATE template_credenziali 
            SET username = ?, password = ?, host = ?, porta = ?, dominio = ?, link = ?, note = ?
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (username, password, host, porta,
                                             dominio, link, note, id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, id: int) -> bool:
        """Elimina una credenziale template"""
        query = "DELETE FROM template_credenziali WHERE id = ?"
        rowcount = db.execute_update(query, (id,))
        return rowcount > 0
    
    @staticmethod
    def delete_by_template_servizio(db: DatabaseManager, template_servizio_id: int) -> bool:
        """Elimina tutte le credenziali di un template servizio"""
        query = "DELETE FROM template_credenziali WHERE template_servizio_id = ?"
        rowcount = db.execute_update(query, (template_servizio_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"TemplateCredenziale: {self.username}@{self.host or self.dominio}"
