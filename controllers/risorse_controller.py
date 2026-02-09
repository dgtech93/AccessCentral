"""
Controller per gestire la logica di PM, Consulenti e Contatti
"""

from typing import List, Optional
from models.database import DatabaseManager
from models.pm import PM
from models.consulente import Consulente
from models.contatto import Contatto


class RisorseController:
    """Gestisce tutta la logica business relativa a PM, Consulenti e Contatti"""
    
    def __init__(self, db: DatabaseManager):
        """
        Inizializza il controller
        
        Args:
            db: Gestore del database
        """
        self.db = db
    
    # ===== GESTIONE PM =====
    
    def crea_pm(self, nome: str, email: str = "", telefono: str = "",
                cellulare: str = "") -> int:
        """
        Crea un nuovo PM
        
        Args:
            nome: Nome del PM
            email: Email
            telefono: Telefono
            cellulare: Cellulare
            
        Returns:
            ID del PM creato
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del PM è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un PM con questo nome
        pms = PM.get_all(self.db)
        if any(p.nome.lower() == nome.lower() for p in pms):
            raise ValueError(f"Esiste già un PM con nome '{nome}'")
        
        return PM.create(self.db, nome, email, telefono, cellulare)
    
    def ottieni_tutti_pm(self) -> List[PM]:
        """Recupera tutti i PM"""
        return PM.get_all(self.db)
    
    def ottieni_pm(self, pm_id: int) -> Optional[PM]:
        """Recupera un PM specifico"""
        return PM.get_by_id(self.db, pm_id)
    
    def modifica_pm(self, pm_id: int, nome: str, email: str = "",
                    telefono: str = "", cellulare: str = "") -> bool:
        """
        Modifica un PM esistente
        
        Args:
            pm_id: ID del PM da modificare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del PM è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un altro PM con questo nome
        pms = PM.get_all(self.db)
        if any(p.nome.lower() == nome.lower() and p.id != pm_id for p in pms):
            raise ValueError(f"Esiste già un altro PM con nome '{nome}'")
        
        return PM.update(self.db, pm_id, nome, email, telefono, cellulare)
    
    def elimina_pm(self, pm_id: int) -> bool:
        """Elimina un PM"""
        return PM.delete(self.db, pm_id)
    
    def conta_clienti_pm(self, pm_id: int) -> int:
        """Conta quanti clienti sono associati a un PM"""
        return PM.get_clienti_count(self.db, pm_id)
    
    # ===== GESTIONE CONSULENTI =====
    
    def crea_consulente(self, nome: str, email: str = "", telefono: str = "",
                       cellulare: str = "", competenza: str = "") -> int:
        """
        Crea un nuovo Consulente
        
        Args:
            nome: Nome del consulente
            email: Email
            telefono: Telefono
            cellulare: Cellulare
            competenza: Competenza
            
        Returns:
            ID del consulente creato
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del consulente è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un consulente con questo nome
        consulenti = Consulente.get_all(self.db)
        if any(c.nome.lower() == nome.lower() for c in consulenti):
            raise ValueError(f"Esiste già un consulente con nome '{nome}'")
        
        return Consulente.create(self.db, nome, email, telefono, cellulare, competenza)
    
    def ottieni_tutti_consulenti(self) -> List[Consulente]:
        """Recupera tutti i consulenti"""
        return Consulente.get_all(self.db)
    
    def ottieni_consulente(self, consulente_id: int) -> Optional[Consulente]:
        """Recupera un consulente specifico"""
        return Consulente.get_by_id(self.db, consulente_id)
    
    def ottieni_consulenti_cliente(self, cliente_id: int) -> List[Consulente]:
        """Recupera tutti i consulenti associati a un cliente"""
        return Consulente.get_by_cliente(self.db, cliente_id)
    
    def modifica_consulente(self, consulente_id: int, nome: str, email: str = "",
                           telefono: str = "", cellulare: str = "", 
                           competenza: str = "") -> bool:
        """
        Modifica un consulente esistente
        
        Args:
            consulente_id: ID del consulente da modificare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            competenza: Nuova competenza
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del consulente è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un altro consulente con questo nome
        consulenti = Consulente.get_all(self.db)
        if any(c.nome.lower() == nome.lower() and c.id != consulente_id for c in consulenti):
            raise ValueError(f"Esiste già un altro consulente con nome '{nome}'")
        
        return Consulente.update(self.db, consulente_id, nome, email, 
                                telefono, cellulare, competenza)
    
    def elimina_consulente(self, consulente_id: int) -> bool:
        """Elimina un consulente"""
        return Consulente.delete(self.db, consulente_id)
    
    def associa_consulente_cliente(self, cliente_id: int, consulente_id: int) -> bool:
        """Associa un consulente a un cliente"""
        return Consulente.associa_a_cliente(self.db, cliente_id, consulente_id)
    
    def disassocia_consulente_cliente(self, cliente_id: int, consulente_id: int) -> bool:
        """Rimuove l'associazione tra consulente e cliente"""
        return Consulente.disassocia_da_cliente(self.db, cliente_id, consulente_id)
    
    def conta_clienti_consulente(self, consulente_id: int) -> int:
        """Conta quanti clienti sono associati a un consulente"""
        return Consulente.get_clienti_count(self.db, consulente_id)
    
    # ===== GESTIONE CONTATTI =====
    
    def crea_contatto(self, cliente_id: int, nome: str, email: str = "",
                     telefono: str = "", cellulare: str = "", ruolo: str = "") -> int:
        """
        Crea un nuovo contatto per un cliente
        
        Args:
            cliente_id: ID del cliente
            nome: Nome del contatto
            email: Email
            telefono: Telefono
            cellulare: Cellulare
            ruolo: Ruolo
            
        Returns:
            ID del contatto creato
            
        Raises:
            ValueError: Se il nome è vuoto
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del contatto è obbligatorio")
        
        return Contatto.create(self.db, cliente_id, nome.strip(), 
                              email, telefono, cellulare, ruolo)
    
    def ottieni_contatti_cliente(self, cliente_id: int) -> List[Contatto]:
        """Recupera tutti i contatti di un cliente"""
        return Contatto.get_by_cliente(self.db, cliente_id)
    
    def ottieni_contatto(self, contatto_id: int) -> Optional[Contatto]:
        """Recupera un contatto specifico"""
        return Contatto.get_by_id(self.db, contatto_id)
    
    def modifica_contatto(self, contatto_id: int, nome: str, email: str = "",
                         telefono: str = "", cellulare: str = "", ruolo: str = "") -> bool:
        """
        Modifica un contatto esistente
        
        Args:
            contatto_id: ID del contatto da modificare
            nome: Nuovo nome
            email: Nuova email
            telefono: Nuovo telefono
            cellulare: Nuovo cellulare
            ruolo: Nuovo ruolo
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se il nome è vuoto
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del contatto è obbligatorio")
        
        return Contatto.update(self.db, contatto_id, nome.strip(), 
                              email, telefono, cellulare, ruolo)
    
    def elimina_contatto(self, contatto_id: int) -> bool:
        """Elimina un contatto"""
        return Contatto.delete(self.db, contatto_id)
