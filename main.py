"""
AccessCentral - Gestione Credenziali di Accesso
Applicazione per gestire credenziali RDP, CRM e altri sistemi
con supporto VPN e organizzazione per clienti.

Architettura: MVC (Model-View-Controller)
- Models: Gestione dati e database (SQLite)
- Views: Interfaccia grafica (PyQt5)
- Controllers: Logica business
"""

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSystemSemaphore, QSharedMemory
import os
from views.main_window import MainWindow


def main():
    """
    Funzione principale che avvia l'applicazione
    """
    # Crea l'applicazione Qt
    app = QApplication(sys.argv)
    
    # Imposta lo stile dell'applicazione
    app.setStyle('Fusion')
    
    # Previene l'esecuzione di istanze multiple
    shared_memory = QSharedMemory('CredenzialiSuiteAppMutex')
    if shared_memory.attach():
        # Un'altra istanza è già in esecuzione
        QMessageBox.warning(None, 'Applicazione già avviata', 
                          'AccessCentral è già in esecuzione.')
        return
    
    if not shared_memory.create(1):
        QMessageBox.warning(None, 'Errore', 
                          'Impossibile avviare l\'applicazione.')
        return
    
    # Imposta l'icona dell'applicazione
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()
    
    # Avvia il loop degli eventi
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
