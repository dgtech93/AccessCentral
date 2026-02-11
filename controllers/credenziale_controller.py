"""
Controller per gestire la logica di servizi e credenziali
"""

from typing import List, Optional
from models.database import DatabaseManager
from models.servizio import Servizio
from models.credenziale import Credenziale
from models.template_servizio import TemplateServizio
from models.template_credenziale import TemplateCredenziale
from models.template_cliente import TemplateCliente


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
    
    # ===== GESTIONE TEMPLATE SERVIZI (v2.1) =====
    
    def crea_template(self, nome_template: str, tipo: str, descrizione: str = "",
                     link: str = "", note_template: str = "") -> int:
        """Crea un nuovo template servizio"""
        if not nome_template or not nome_template.strip():
            raise ValueError("Il nome del template è obbligatorio")
        
        if not tipo or tipo not in Servizio.TIPI_DISPONIBILI:
            raise ValueError(f"Tipo di servizio non valido: {tipo}")
        
        return TemplateServizio.create(self.db, nome_template.strip(), tipo,
                                      descrizione.strip(), link.strip(), note_template.strip())
    
    def ottieni_tutti_template(self) -> List[TemplateServizio]:
        """Recupera tutti i template"""
        return TemplateServizio.get_all(self.db)
    
    def ottieni_template_per_tipo(self, tipo: str) -> List[TemplateServizio]:
        """Recupera template filtrati per tipo"""
        return TemplateServizio.get_by_tipo(self.db, tipo)
    
    def ottieni_template(self, template_id: int) -> Optional[TemplateServizio]:
        """Recupera un template specifico"""
        return TemplateServizio.get_by_id(self.db, template_id)
    
    def modifica_template(self, template_id: int, nome_template: str, tipo: str,
                         descrizione: str = "", link: str = "", note_template: str = "") -> bool:
        """Modifica un template"""
        if not nome_template or not nome_template.strip():
            raise ValueError("Il nome del template è obbligatorio")
        
        if not tipo or tipo not in Servizio.TIPI_DISPONIBILI:
            raise ValueError(f"Tipo di servizio non valido: {tipo}")
        
        return TemplateServizio.update(self.db, template_id, nome_template.strip(),
                                      tipo, descrizione.strip(), link.strip(), note_template.strip())
    
    def elimina_template(self, template_id: int) -> bool:
        """Elimina un template"""
        return TemplateServizio.delete(self.db, template_id)
    
    def crea_servizio_da_template(self, cliente_id: int, nome_servizio: str,
                                  template_id: int) -> int:
        """Crea un servizio da un template (senza credenziali - v2.2 simplified)"""
        template = TemplateServizio.get_by_id(self.db, template_id)
        if not template:
            raise ValueError(f"Template con ID {template_id} non trovato")
        
        # Crea il servizio con i dati del template
        servizio_id = self.crea_servizio(cliente_id, nome_servizio, template.tipo,
                                         template.descrizione, template.link)
        
        # Le credenziali vanno aggiunte manualmente dopo la creazione
        return servizio_id
    
    # ===== GESTIONE TEMPLATE CREDENZIALI (v2.1 extended) =====
    
    def crea_template_credenziale(self, template_servizio_id: int, username: str = "",
                                  password: str = "", host: str = "", porta: Optional[int] = None,
                                  dominio: str = "", link: str = "", note: str = "") -> int:
        """Crea una credenziale template per un template servizio"""
        return TemplateCredenziale.create(self.db, template_servizio_id, username,
                                         password, host, porta, dominio, link, note)
    
    def ottieni_credenziali_template(self, template_servizio_id: int) -> List[TemplateCredenziale]:
        """Recupera tutte le credenziali di un template servizio"""
        return TemplateCredenziale.get_by_template_servizio(self.db, template_servizio_id)
    
    def ottieni_credenziale_template(self, id: int) -> Optional[TemplateCredenziale]:
        """Recupera una credenziale template per ID"""
        return TemplateCredenziale.get_by_id(self.db, id)
    
    def modifica_template_credenziale(self, id: int, username: str = "", password: str = "",
                                     host: str = "", porta: Optional[int] = None,
                                     dominio: str = "", link: str = "", note: str = "") -> bool:
        """Modifica una credenziale template"""
        return TemplateCredenziale.update(self.db, id, username, password, host,
                                         porta, dominio, link, note)
    
    def elimina_template_credenziale(self, id: int) -> bool:
        """Elimina una credenziale template"""
        return TemplateCredenziale.delete(self.db, id)
    
    # ===== GESTIONE TEMPLATE CLIENTE (v2.1 extended) =====
    
    def crea_template_cliente(self, nome_template: str, descrizione_cliente: str = "",
                             note_template: str = "") -> int:
        """Crea un nuovo template cliente"""
        if not nome_template or not nome_template.strip():
            raise ValueError("Il nome del template è obbligatorio")
        
        return TemplateCliente.create(self.db, nome_template.strip(),
                                     descrizione_cliente.strip(), note_template.strip())
    
    def ottieni_tutti_template_cliente(self) -> List[TemplateCliente]:
        """Recupera tutti i template cliente"""
        return TemplateCliente.get_all(self.db)
    
    def ottieni_template_cliente(self, template_id: int) -> Optional[TemplateCliente]:
        """Recupera un template cliente specifico"""
        return TemplateCliente.get_by_id(self.db, template_id)
    
    def modifica_template_cliente(self, template_id: int, nome_template: str,
                                 descrizione_cliente: str = "", note_template: str = "") -> bool:
        """Modifica un template cliente"""
        if not nome_template or not nome_template.strip():
            raise ValueError("Il nome del template è obbligatorio")
        
        return TemplateCliente.update(self.db, template_id, nome_template.strip(),
                                     descrizione_cliente.strip(), note_template.strip())
    
    def elimina_template_cliente(self, template_id: int) -> bool:
        """Elimina un template cliente"""
        return TemplateCliente.delete(self.db, template_id)
    
    def aggiungi_servizio_a_template_cliente(self, template_cliente_id: int,
                                            template_servizio_id: int) -> int:
        """Associa un template servizio a un template cliente"""
        return TemplateCliente.add_servizio(self.db, template_cliente_id, template_servizio_id)
    
    def rimuovi_servizio_da_template_cliente(self, template_cliente_id: int,
                                            template_servizio_id: int) -> bool:
        """Rimuove un template servizio da un template cliente"""
        return TemplateCliente.remove_servizio(self.db, template_cliente_id, template_servizio_id)
    
    def ottieni_servizi_template_cliente(self, template_cliente_id: int) -> List[TemplateServizio]:
        """Recupera tutti i template servizio di un template cliente"""
        return TemplateCliente.get_servizi(self.db, template_cliente_id)
