"""
Controllers per la logica business dell'applicazione
"""

from .cliente_controller import ClienteController
from .credenziale_controller import CredenzialeController
from .risorse_controller import RisorseController

__all__ = ['ClienteController', 'CredenzialeController', 'RisorseController']
