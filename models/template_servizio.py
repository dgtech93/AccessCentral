"""
Modello Template Servizio
"""

from typing import Optional, List
from models.database import DatabaseManager


class TemplateServizio:
    """Rappresenta un template per creare servizi rapidamente"""
    
    def __init__(self, id: Optional[int] = None, nome_template: str = "",
                 tipo: str = "", descrizione: str = "", link: str = "",
                 note_template: str = ""):
        self.id = id
        self.nome_template = nome_template
        self.tipo = tipo
        self.descrizione = descrizione
        self.link = link
        self.note_template = note_template
    
    @staticmethod
    def create(db: DatabaseManager, nome_template: str, tipo: str,
               descrizione: str = "", link: str = "", note_template: str = "") -> int:
        """Crea un nuovo template servizio"""
        query = """
            INSERT INTO template_servizi (nome_template, tipo, descrizione, link, note_template)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_update(query, (nome_template, tipo, descrizione, link, note_template))
    
    @staticmethod
    def get_all(db: DatabaseManager) -> List['TemplateServizio']:
        """Recupera tutti i template"""
        query = "SELECT * FROM template_servizi ORDER BY nome_template"
        rows = db.execute_query(query)
        
        templates = []
        for row in rows:
            template = TemplateServizio(
                id=row['id'],
                nome_template=row['nome_template'],
                tipo=row['tipo'],
                descrizione=row['descrizione'],
                link=row['link'] if 'link' in row.keys() else "",
                note_template=row['note_template'] if 'note_template' in row.keys() else ""
            )
            templates.append(template)
        
        return templates
    
    @staticmethod
    def get_by_id(db: DatabaseManager, template_id: int) -> Optional['TemplateServizio']:
        """Recupera un template per ID"""
        query = "SELECT * FROM template_servizi WHERE id = ?"
        rows = db.execute_query(query, (template_id,))
        
        if rows:
            row = rows[0]
            return TemplateServizio(
                id=row['id'],
                nome_template=row['nome_template'],
                tipo=row['tipo'],
                descrizione=row['descrizione'],
                link=row['link'] if 'link' in row.keys() else "",
                note_template=row['note_template'] if 'note_template' in row.keys() else ""
            )
        return None
    
    @staticmethod
    def get_by_tipo(db: DatabaseManager, tipo: str) -> List['TemplateServizio']:
        """Recupera template filtrati per tipo"""
        query = "SELECT * FROM template_servizi WHERE tipo = ? ORDER BY nome_template"
        rows = db.execute_query(query, (tipo,))
        
        templates = []
        for row in rows:
            template = TemplateServizio(
                id=row['id'],
                nome_template=row['nome_template'],
                tipo=row['tipo'],
                descrizione=row['descrizione'],
                link=row['link'] if 'link' in row.keys() else "",
                note_template=row['note_template'] if 'note_template' in row.keys() else ""
            )
            templates.append(template)
        
        return templates
    
    @staticmethod
    def update(db: DatabaseManager, template_id: int, nome_template: str,
               tipo: str, descrizione: str = "", link: str = "", 
               note_template: str = "") -> bool:
        """Aggiorna un template"""
        query = """
            UPDATE template_servizi 
            SET nome_template = ?, tipo = ?, descrizione = ?, link = ?,
                note_template = ?, modificato_il = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        rowcount = db.execute_update(query, (nome_template, tipo, descrizione, 
                                              link, note_template, template_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, template_id: int) -> bool:
        """Elimina un template"""
        query = "DELETE FROM template_servizi WHERE id = ?"
        rowcount = db.execute_update(query, (template_id,))
        return rowcount > 0
    
    def __str__(self):
        return f"Template: {self.nome_template} ({self.tipo})"
