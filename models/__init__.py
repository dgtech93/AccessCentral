"""
Modelli dati per l'applicazione CredenzialiSuite
"""

from .database import DatabaseManager
from .cliente import Cliente
from .servizio import Servizio
from .credenziale import Credenziale
from .pm import PM
from .consulente import Consulente
from .contatto import Contatto
from .template_servizio import TemplateServizio
from .template_credenziale import TemplateCredenziale
from .template_cliente import TemplateCliente
from .allegato import Allegato

__all__ = ['DatabaseManager', 'Cliente', 'Servizio', 'Credenziale', 
           'PM', 'Consulente', 'Contatto', 'TemplateServizio', 'TemplateCredenziale',
           'TemplateCliente', 'Allegato']
