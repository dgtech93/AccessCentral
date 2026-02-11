"""
Controller per gestire la logica di servizi e credenziali
"""

from typing import List, Optional
from models.database import DatabaseManager
from models.servizio import Servizio
from models.credenziale import Credenziale


class CredenzialeController:
    """Gestisce tutta la logica business relativa a servizi e credenziali"""
    
    def __init__(self, db: DatabaseManager, crypto_manager=None):
        """
        Inizializza il controller
        
        Args:
            db: Gestore del database
            crypto_manager: Gestore crittografia (opzionale per compatibilità)
        """
        self.db = db
        self.crypto_manager = crypto_manager
    
    # ===== GESTIONE SERVIZI =====
    
    def crea_servizio(self, cliente_id: int, nome: str, tipo: str,
                     descrizione: str = "", link: str = "") -> int:
        """
        Crea un nuovo servizio
        
        Args:
            cliente_id: ID del cliente proprietario
            nome: Nome del servizio
            tipo: Tipo di servizio
            descrizione: Descrizione opzionale
            link: Link/URL opzionale (per CRM e Web)
            
        Returns:
            ID del servizio creato
            
        Raises:
            ValueError: Se i parametri non sono validi
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del servizio è obbligatorio")
        
        if tipo not in Servizio.TIPI_DISPONIBILI:
            raise ValueError(f"Tipo di servizio non valido: {tipo}")
        
        nome = nome.strip()
        
        # Verifica se esiste già un servizio con questo nome per il cliente
        servizi = Servizio.get_by_cliente(self.db, cliente_id)
        if any(s.nome.lower() == nome.lower() for s in servizi):
            raise ValueError(f"Esiste già un servizio con nome '{nome}' per questo cliente")
        
        return Servizio.create(self.db, cliente_id, nome, tipo, descrizione, link)
    
    def ottieni_servizi_cliente(self, cliente_id: int) -> List[Servizio]:
        """
        Recupera tutti i servizi di un cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista di servizi
        """
        return Servizio.get_by_cliente(self.db, cliente_id)
    
    def ottieni_servizio(self, servizio_id: int) -> Optional[Servizio]:
        """
        Recupera un servizio specifico
        
        Args:
            servizio_id: ID del servizio
            
        Returns:
            Servizio trovato o None
        """
        return Servizio.get_by_id(self.db, servizio_id)
    
    def modifica_servizio(self, servizio_id: int, nome: str, tipo: str,
                         descrizione: str = "", link: str = "") -> bool:
        """
        Modifica un servizio esistente
        
        Args:
            servizio_id: ID del servizio da modificare
            nome: Nuovo nome
            tipo: Nuovo tipo
            descrizione: Nuova descrizione
            link: Nuovo link/URL (per CRM e Web)
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se i parametri non sono validi
        """
        if not nome or not nome.strip():
            raise ValueError("Il nome del servizio è obbligatorio")
        
        if tipo not in Servizio.TIPI_DISPONIBILI:
            raise ValueError(f"Tipo di servizio non valido: {tipo}")
        
        nome = nome.strip()
        
        # Recupera il servizio corrente per ottenere il cliente_id
        servizio_corrente = Servizio.get_by_id(self.db, servizio_id)
        if not servizio_corrente:
            raise ValueError("Servizio non trovato")
        
        # Verifica se esiste già un altro servizio con questo nome per il cliente
        servizi = Servizio.get_by_cliente(self.db, servizio_corrente.cliente_id)
        if any(s.nome.lower() == nome.lower() and s.id != servizio_id for s in servizi):
            raise ValueError(f"Esiste già un altro servizio con nome '{nome}' per questo cliente")
        
        return Servizio.update(self.db, servizio_id, nome, tipo, descrizione, link)
    
    def elimina_servizio(self, servizio_id: int) -> bool:
        """
        Elimina un servizio e tutte le sue credenziali
        
        Args:
            servizio_id: ID del servizio da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        return Servizio.delete(self.db, servizio_id)
    
    # ===== GESTIONE CREDENZIALI =====
    
    def crea_credenziale(self, servizio_id: int, username: str, password: str,
                        host: str = "", porta: Optional[int] = None,
                        note: str = "", rdp_configurata: bool = False, link: str = "") -> int:
        """
        Crea una nuova credenziale
        
        Args:
            servizio_id: ID del servizio associato
            username: Nome utente
            password: Password
            host: Host/IP del servizio
            porta: Porta del servizio
            note: Note aggiuntive
            rdp_configurata: Se True, è una RDP già configurata da lanciare direttamente
            link: Link/URL del servizio (per aprire nel browser)
            
        Returns:
            ID della credenziale creata
            
        Raises:
            ValueError: Se i parametri non sono validi
        """
        if not username or not username.strip():
            raise ValueError("Lo username è obbligatorio")
        
        if not password:
            raise ValueError("La password è obbligatoria")
        
        # Cripta la password se disponibile il crypto manager
        password_da_salvare = password
        if self.crypto_manager:
            password_da_salvare = self.crypto_manager.cripta(password)
        
        return Credenziale.create(self.db, servizio_id, username.strip(),
                                 password_da_salvare, host.strip(), porta, note, rdp_configurata, link.strip())
    
    def ottieni_credenziali_servizio(self, servizio_id: int) -> List[Credenziale]:
        """
        Recupera tutte le credenziali di un servizio (con password decriptate)
        
        Args:
            servizio_id: ID del servizio
            
        Returns:
            Lista di credenziali con password decriptate
        """
        credenziali = Credenziale.get_by_servizio(self.db, servizio_id)
        
        # Decripta le password se disponibile il crypto manager
        if self.crypto_manager:
            for cred in credenziali:
                try:
                    cred.password = self.crypto_manager.decripta(cred.password)
                except:
                    pass  # Mantieni la password come è se la decrittazione fallisce
        
        return credenziali
    
    def ottieni_credenziale(self, credenziale_id: int) -> Optional[Credenziale]:
        """
        Recupera una credenziale specifica (con password decriptata)
        
        Args:
            credenziale_id: ID della credenziale
            
        Returns:
            Credenziale trovata o None
        """
        cred = Credenziale.get_by_id(self.db, credenziale_id)
        
        # Decripta la password se disponibile il crypto manager
        if cred and self.crypto_manager:
            try:
                cred.password = self.crypto_manager.decripta(cred.password)
            except:
                pass  # Mantieni la password come è se la decrittazione fallisce
        
        return cred
    
    def modifica_credenziale(self, credenziale_id: int, username: str,
                            password: str, host: str = "",
                            porta: Optional[int] = None, note: str = "",
                            rdp_configurata: bool = False, link: str = "") -> bool:
        """
        Modifica una credenziale esistente
        
        Args:
            credenziale_id: ID della credenziale da modificare
            username: Nuovo nome utente
            password: Nuova password
            host: Nuovo host/IP
            porta: Nuova porta
            note: Nuove note
            rdp_configurata: Se True, è una RDP già configurata
            link: Link/URL del servizio (per aprire nel browser)
            
        Returns:
            True se la modifica è riuscita
            
        Raises:
            ValueError: Se i parametri non sono validi
        """
        if not username or not username.strip():
            raise ValueError("Lo username è obbligatorio")
        
        if not password:
            raise ValueError("La password è obbligatoria")
        
        # Cripta la password se disponibile il crypto manager
        password_da_salvare = password
        if self.crypto_manager:
            password_da_salvare = self.crypto_manager.cripta(password)
        
        return Credenziale.update(self.db, credenziale_id, username.strip(),
                                 password_da_salvare, host.strip(), porta, note, rdp_configurata, link.strip())
    
    def elimina_credenziale(self, credenziale_id: int) -> bool:
        """
        Elimina una credenziale
        
        Args:
            credenziale_id: ID della credenziale da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        return Credenziale.delete(self.db, credenziale_id)
    
    def conta_credenziali_servizio(self, servizio_id: int) -> int:
        """
        Conta quante credenziali ha un servizio
        
        Args:
            servizio_id: ID del servizio
            
        Returns:
            Numero di credenziali
        """
        credenziali = Credenziale.get_by_servizio(self.db, servizio_id)
        return len(credenziali)
