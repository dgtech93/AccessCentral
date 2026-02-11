"""
Modello per i template cliente (cliente + servizi + credenziali)
"""

from typing import List, Optional
from models.database import DatabaseManager
from models.template_servizio import TemplateServizio


class TemplateCliente:
    """Rappresenta un template per creare un cliente completo con servizi"""
    
    def __init__(self, id: Optional[int] = None, nome_template: str = "",
                 descrizione_cliente: str = "", note_template: str = ""):
        self.id = id
        self.nome_template = nome_template
        self.descrizione_cliente = descrizione_cliente
        self.note_template = note_template
    
    @staticmethod
    def create(db: DatabaseManager, nome_template: str, descrizione_cliente: str = "",
               note_template: str = "") -> int:
        """Crea un nuovo template cliente"""
        query = """
            INSERT INTO template_cliente (nome_template, descrizione_cliente, note_template)
            VALUES (?, ?, ?)
        """
        return db.execute_update(query, (nome_template, descrizione_cliente, note_template))
    
    @staticmethod
    def get_all(db: DatabaseManager) -> List['TemplateCliente']:
        """Recupera tutti i template cliente"""
        query = "SELECT * FROM template_cliente ORDER BY nome_template"
        rows = db.execute_query(query)
        
        templates = []
        for row in rows:
            template = TemplateCliente(
                id=row['id'],
                nome_template=row['nome_template'],
                descrizione_cliente=row['descrizione_cliente'] or "",
                note_template=row['note_template'] or ""
            )
            templates.append(template)
        
        return templates
    
    @staticmethod
    def get_by_id(db: DatabaseManager, id: int) -> Optional['TemplateCliente']:
        """Recupera un template cliente per ID"""
        query = "SELECT * FROM template_cliente WHERE id = ?"
        rows = db.execute_query(query, (id,))
        
        if rows:
            row = rows[0]
            return TemplateCliente(
                id=row['id'],
                nome_template=row['nome_template'],
                descrizione_cliente=row['descrizione_cliente'] or "",
                note_template=row['note_template'] or ""
            )
        return None
    
    @staticmethod
    def update(db: DatabaseManager, id: int, nome_template: str,
               descrizione_cliente: str = "", note_template: str = "") -> bool:
        """Aggiorna un template cliente"""
        query = """
            UPDATE template_cliente 
            SET nome_template = ?, descrizione_cliente = ?, note_template = ?,
                modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome_template, descrizione_cliente,
                                             note_template, id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, id: int) -> bool:
        """Elimina un template cliente (e i suoi servizi associati per CASCADE)"""
        query = "DELETE FROM template_cliente WHERE id = ?"
        rowcount = db.execute_update(query, (id,))
        return rowcount > 0
    
    @staticmethod
    def add_servizio(db: DatabaseManager, template_cliente_id: int,
                     template_servizio_id: int) -> int:
        """Associa un template servizio a un template cliente"""
        query = """
            INSERT INTO template_cliente_servizi (template_cliente_id, template_servizio_id)
            VALUES (?, ?)
        """
        return db.execute_update(query, (template_cliente_id, template_servizio_id))
    
    @staticmethod
    def remove_servizio(db: DatabaseManager, template_cliente_id: int,
                        template_servizio_id: int) -> bool:
        """Rimuove l'associazione tra template cliente e servizio"""
        query = """
            DELETE FROM template_cliente_servizi 
            WHERE template_cliente_id = ? AND template_servizio_id = ?
        """
        rowcount = db.execute_update(query, (template_cliente_id, template_servizio_id))
        return rowcount > 0
    
    @staticmethod
    def get_servizi(db: DatabaseManager, template_cliente_id: int) -> List[TemplateServizio]:
        """Recupera tutti i template servizio associati a un template cliente"""
        query = """
            SELECT ts.* FROM template_servizi ts
            INNER JOIN template_cliente_servizi tcs 
                ON ts.id = tcs.template_servizio_id
            WHERE tcs.template_cliente_id = ?
            ORDER BY ts.tipo, ts.nome_template
        """
        rows = db.execute_query(query, (template_cliente_id,))
        
        servizi = []
        for row in rows:
            servizio = TemplateServizio(
                id=row['id'],
                nome_template=row['nome_template'],
                tipo=row['tipo'],
                descrizione=row['descrizione'] or "",
                link=row['link'] or "",
                note_template=row['note_template'] or ""
            )
            servizi.append(servizio)
        
        return servizi
    
    def __str__(self):
        return f"TemplateCliente: {self.nome_template}"
