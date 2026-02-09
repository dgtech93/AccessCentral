"""
Controller per gestire la logica dei clienti
"""

from typing import List, Optional
from models.database import DatabaseManager
from models.cliente import Cliente
from models.servizio import Servizio


class ClienteController:
    """Gestisce tutta la logica business relativa ai clienti"""
    
    def __init__(self, db: DatabaseManager):
        """
        Inizializza il controller
        
        Args:
            db: Gestore del database
        """
        self.db = db
    
    def crea_cliente(self, nome: str, descrizione: str = "",
                     vpn_exe_path: str = "", vpn_windows_name: str = "",
                     pm_id: Optional[int] = None) -> int:
        """
        Crea un nuovo cliente
        
        Args:
            nome: Nome del cliente
            descrizione: Descrizione opzionale
            vpn_exe_path: Percorso file .exe VPN
            vpn_windows_name: Nome VPN Windows
            pm_id: ID del PM di riferimento
            
        Returns:
            ID del cliente creato
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del cliente è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un cliente con questo nome
        clienti = Cliente.get_all(self.db)
        if any(c.nome.lower() == nome.lower() for c in clienti):
            raise ValueError(f"Esiste già un cliente con nome '{nome}'")
        
        return Cliente.create(self.db, nome, descrizione, 
                            vpn_exe_path, vpn_windows_name, pm_id)
    
    def ottieni_tutti_clienti(self) -> List[Cliente]:
        """
        Recupera tutti i clienti
        
        Returns:
            Lista di tutti i clienti
        """
        return Cliente.get_all(self.db)
    
    def ottieni_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """
        Recupera un cliente specifico
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Cliente trovato o None
        """
        return Cliente.get_by_id(self.db, cliente_id)
    
    def modifica_cliente(self, cliente_id: int, nome: str, 
                        descrizione: str = "", vpn_exe_path: str = "",
                        vpn_windows_name: str = "", pm_id: Optional[int] = None) -> bool:
        """
        Modifica un cliente esistente
        
        Args:
            cliente_id: ID del cliente da modificare
            nome: Nuovo nome
            descrizione: Nuova descrizione
            vpn_exe_path: Nuovo percorso VPN exe
            vpn_windows_name: Nuovo nome VPN Windows
            pm_id: ID del PM di riferimento
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se il nome è vuoto o già esistente
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del cliente è obbligatorio")
        
        nome = nome.strip()
        
        # Verifica se esiste già un altro cliente con questo nome
        clienti = Cliente.get_all(self.db)
        if any(c.nome.lower() == nome.lower() and c.id != cliente_id for c in clienti):
            raise ValueError(f"Esiste già un altro cliente con nome '{nome}'")
        
        return Cliente.update(self.db, cliente_id, nome, descrizione,
                            vpn_exe_path, vpn_windows_name, pm_id)
    
    def elimina_cliente(self, cliente_id: int) -> bool:
        """
        Elimina un cliente e tutti i suoi servizi/credenziali
        
        Args:
            cliente_id: ID del cliente da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        return Cliente.delete(self.db, cliente_id)
    
    def ottieni_servizi_cliente(self, cliente_id: int) -> List[Servizio]:
        """
        Recupera tutti i servizi di un cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista di servizi del cliente
        """
        return Servizio.get_by_cliente(self.db, cliente_id)
    
    def conta_servizi_cliente(self, cliente_id: int) -> int:
        """
        Conta quanti servizi ha un cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Numero di servizi
        """
        servizi = Servizio.get_by_cliente(self.db, cliente_id)
        return len(servizi)
