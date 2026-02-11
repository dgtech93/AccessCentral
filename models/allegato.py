"""
Modello Allegato (file allegati ai clienti)
"""

import os
import shutil
from typing import Optional, List
from models.database import DatabaseManager


class Allegato:
    """Rappresenta un allegato associato a un cliente"""
    
    BASE_DIR = "documenti"
    MAX_SIZE_MB = 10
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
    
    def __init__(self, id: Optional[int] = None, cliente_id: int = 0,
                 nome_file: str = "", nome_originale: str = "",
                 percorso_file: str = "", dimensione_kb: int = 0,
                 tipo_mime: str = "", descrizione: str = "", creato_il: str = ""):
        self.id = id
        self.cliente_id = cliente_id
        self.nome_file = nome_file
        self.nome_originale = nome_originale
        self.percorso_file = percorso_file
        self.dimensione_kb = dimensione_kb
        self.tipo_mime = tipo_mime
        self.descrizione = descrizione
        self.creato_il = creato_il
    
    @staticmethod
    def _get_storage_dir(cliente_id: int) -> str:
        """Restituisce la directory di storage per un cliente"""
        storage_dir = os.path.join(Allegato.BASE_DIR, str(cliente_id))
        os.makedirs(storage_dir, exist_ok=True)
        return storage_dir
    
    @staticmethod
    def _get_unique_filename(directory: str, original_name: str) -> str:
        """Genera un nome file unico"""
        base_name, ext = os.path.splitext(original_name)
        counter = 1
        new_name = original_name
        
        while os.path.exists(os.path.join(directory, new_name)):
            new_name = f"{base_name}_{counter}{ext}"
            counter += 1
        
        return new_name
    
    @staticmethod
    def crea_allegato(db: DatabaseManager, cliente_id: int, file_path: str,
                     descrizione: str = "") -> int:
        """Crea un nuovo allegato caricando il file"""
        if not os.path.exists(file_path):
            raise ValueError(f"File non trovato: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size > Allegato.MAX_SIZE_BYTES:
            raise ValueError(f"File troppo grande (max {Allegato.MAX_SIZE_MB} MB)")
        
        nome_originale = os.path.basename(file_path)
        dimensione_kb = file_size // 1024
        
        # MIME type semplificato
        ext = os.path.splitext(nome_originale)[1].lower()
        mime_types = {
            '.pdf': 'application/pdf', '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.txt': 'text/plain', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif',
            '.zip': 'application/zip', '.rar': 'application/x-rar-compressed'
        }
        tipo_mime = mime_types.get(ext, 'application/octet-stream')
        
        storage_dir = Allegato._get_storage_dir(cliente_id)
        nome_file = Allegato._get_unique_filename(storage_dir, nome_originale)
        percorso_completo = os.path.join(storage_dir, nome_file)
        
        try:
            shutil.copy2(file_path, percorso_completo)
        except Exception as e:
            raise IOError(f"Errore caricamento file: {e}")
        
        query = """
            INSERT INTO allegati (cliente_id, nome_file, nome_originale, percorso_file,
                                 dimensione_kb, tipo_mime, descrizione)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        percorso_relativo = os.path.join(Allegato.BASE_DIR, str(cliente_id), nome_file)
        
        return db.execute_update(query, (cliente_id, nome_file, nome_originale,
                                         percorso_relativo, dimensione_kb, tipo_mime,
                                         descrizione))
    
    @staticmethod
    def get_by_cliente(db: DatabaseManager, cliente_id: int) -> List['Allegato']:
        """Recupera tutti gli allegati di un cliente"""
        query = "SELECT * FROM allegati WHERE cliente_id = ? ORDER BY creato_il DESC"
        rows = db.execute_query(query, (cliente_id,))
        
        allegati = []
        for row in rows:
            allegato = Allegato(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome_file=row['nome_file'],
                nome_originale=row['nome_originale'],
                percorso_file=row['percorso_file'],
                dimensione_kb=row['dimensione_kb'] if 'dimensione_kb' in row.keys() else 0,
                tipo_mime=row['tipo_mime'] if 'tipo_mime' in row.keys() else "",
                descrizione=row['descrizione'] if 'descrizione' in row.keys() else "",
                creato_il=row['creato_il'] if 'creato_il' in row.keys() else ""
            )
            allegati.append(allegato)
        
        return allegati
    
    @staticmethod
    def get_by_id(db: DatabaseManager, allegato_id: int) -> Optional['Allegato']:
        """Recupera un allegato per ID"""
        query = "SELECT * FROM allegati WHERE id = ?"
        rows = db.execute_query(query, (allegato_id,))
        
        if rows:
            row = rows[0]
            return Allegato(
                id=row['id'],
                cliente_id=row['cliente_id'],
                nome_file=row['nome_file'],
                nome_originale=row['nome_originale'],
                percorso_file=row['percorso_file'],
                dimensione_kb=row['dimensione_kb'] if 'dimensione_kb' in row.keys() else 0,
                tipo_mime=row['tipo_mime'] if 'tipo_mime' in row.keys() else "",
                descrizione=row['descrizione'] if 'descrizione' in row.keys() else "",
                creato_il=row['creato_il'] if 'creato_il' in row.keys() else ""
            )
        return None
    
    @staticmethod
    def update_descrizione(db: DatabaseManager, allegato_id: int, descrizione: str) -> bool:
        """Aggiorna la descrizione"""
        query = "UPDATE allegati SET descrizione = ? WHERE id = ?"
        rowcount = db.execute_update(query, (descrizione, allegato_id))
        return rowcount > 0
    
    @staticmethod
    def delete(db: DatabaseManager, allegato_id: int) -> bool:
        """Elimina un allegato"""
        allegato = Allegato.get_by_id(db, allegato_id)
        if not allegato:
            return False
        
        if os.path.exists(allegato.percorso_file):
            try:
                os.remove(allegato.percorso_file)
            except:
                pass
        
        query = "DELETE FROM allegati WHERE id = ?"
        rowcount = db.execute_update(query, (allegato_id,))
        return rowcount > 0
    
    @staticmethod
    def conta_allegati_cliente(db: DatabaseManager, cliente_id: int) -> int:
        """Conta allegati di un cliente"""
        allegati = Allegato.get_by_cliente(db, cliente_id)
        return len(allegati)
    
    @staticmethod
    def get_dimensione_totale_cliente(db: DatabaseManager, cliente_id: int) -> int:
        """Calcola dimensione totale in KB"""
        allegati = Allegato.get_by_cliente(db, cliente_id)
        return sum(a.dimensione_kb for a in allegati)
    
    def get_dimensione_formattata(self) -> str:
        """Dimensione formattata"""
        if self.dimensione_kb < 1024:
            return f"{self.dimensione_kb} KB"
        else:
            mb = self.dimensione_kb / 1024
            return f"{mb:.2f} MB"
    
    def get_icona(self) -> str:
        """Icona basata sul tipo file"""
        ext = os.path.splitext(self.nome_file)[1].lower()
        icone = {
            '.pdf': '📄', '.doc': '📝', '.docx': '📝',
            '.xls': '📊', '.xlsx': '📊', '.txt': '📃',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.zip': '📦', '.rar': '📦'
        }
        return icone.get(ext, '📎')
    
    def __str__(self):
        return f"Allegato: {self.nome_originale} ({self.get_dimensione_formattata()})"
