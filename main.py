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
import os
import json
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSystemSemaphore, QSharedMemory
from views.main_window import MainWindow
from views.security_dialogs import MasterPasswordDialog
from utils.crypto_manager import CryptoManager
from utils.backup_manager import BackupManager


def verifica_prima_esecuzione():
    """Verifica se è la prima esecuzione dell'app con crittografia"""
    config_file = 'security_config.json'
    return not os.path.exists(config_file)


def salva_config_sicurezza(salt: bytes, password_hash: str, recovery_code_hash: str = None):
    """Salva la configurazione di sicurezza"""
    config = {
        'salt': salt.hex(),
        'password_hash': password_hash
    }
    if recovery_code_hash:
        config['recovery_code_hash'] = recovery_code_hash
    with open('security_config.json', 'w') as f:
        json.dump(config, f)


def carica_config_sicurezza():
    """Carica la configurazione di sicurezza"""
    try:
        with open('security_config.json', 'r') as f:
            config = json.load(f)
            recovery_hash = config.get('recovery_code_hash', None)
            return bytes.fromhex(config['salt']), config['password_hash'], recovery_hash
    except:
        return None, None, None


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
    
    # === SISTEMA CRITTOGRAFIA E MASTER PASSWORD ===
    crypto_manager = CryptoManager()
    prima_volta = verifica_prima_esecuzione()
    
    if prima_volta:
        # Prima esecuzione: crea configurazione
        dialog = MasterPasswordDialog(None, prima_volta)
        if dialog.exec_() != MasterPasswordDialog.Accepted:
            return  # Utente ha annullato
        
        password = dialog.get_password()
        salt = crypto_manager.inizializza_con_password(password)
        
        # Genera codice di recupero
        recovery_code = crypto_manager.genera_recovery_code()
        recovery_hash = crypto_manager.calcola_hash_password(recovery_code)
        
        salva_config_sicurezza(salt, crypto_manager.master_password_hash, recovery_hash)
        
        QMessageBox.information(
            None, "⚠️ CODICE DI RECUPERO - SALVALO!",
            f"Master password impostata con successo!\n\n"
            f"🔑 CODICE DI RECUPERO:\n{recovery_code}\n\n"
            f"⚠️ IMPORTANTE: Salva questo codice in un posto sicuro!\n"
            f"Ti servirà per recuperare l'accesso se dimentichi la password.\n\n"
            f"Questo codice verrà mostrato solo ora!"
        )
    else:
        # Carica configurazione esistente
        salt, password_hash, recovery_hash = carica_config_sicurezza()
        if not salt:
            QMessageBox.critical(
                None, "Errore", 
                "Configurazione di sicurezza corrotta!"
            )
            return
        
        # Sistema di tentativi (max 3)
        tentativi = 0
        max_tentativi = 3
        password_corretta = False
        
        while tentativi < max_tentativi and not password_corretta:
            # Mostra dialog master password
            dialog = MasterPasswordDialog(None, prima_volta)
            if dialog.exec_() != MasterPasswordDialog.Accepted:
                return  # Utente ha annullato
            
            password = dialog.get_password()
            
            # Verifica password
            password_hash_inserita = crypto_manager.calcola_hash_password(password)
            if password_hash_inserita == password_hash:
                password_corretta = True
                crypto_manager.inizializza_con_password(password, salt)
                crypto_manager.master_password_hash = password_hash
            else:
                tentativi += 1
                rimanenti = max_tentativi - tentativi
                
                if rimanenti > 0:
                    QMessageBox.warning(
                        None, "Password Errata",
                        f"Password errata!\n\nTentativi rimanenti: {rimanenti}"
                    )
                else:
                    # Esauriti i tentativi
                    risposta = QMessageBox.question(
                        None, "Accesso Negato",
                        "Hai esaurito i tentativi disponibili.\n\n"
                        "Non ricordi la password?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if risposta == QMessageBox.Yes:
                        # Recupero password
                        from views.security_dialogs import RecoveryCodeDialog
                        
                        recovery_dialog = RecoveryCodeDialog(None)
                        if recovery_dialog.exec_() == RecoveryCodeDialog.Accepted:
                            recovery_code = recovery_dialog.get_code()
                            recovery_hash_inserito = crypto_manager.calcola_hash_password(recovery_code)
                            
                            if recovery_hash and recovery_hash_inserito == recovery_hash:
                                # Codice corretto, permetti di impostare nuova password
                                new_pass_dialog = MasterPasswordDialog(None, prima_volta=True)
                                if new_pass_dialog.exec_() == MasterPasswordDialog.Accepted:
                                    nuova_password = new_pass_dialog.get_password()
                                    salt = crypto_manager.inizializza_con_password(nuova_password)
                                    salva_config_sicurezza(salt, crypto_manager.master_password_hash, recovery_hash)
                                    
                                    QMessageBox.information(
                                        None, "Password Reimpostata",
                                        "Password reimpostata con successo!\n\n"
                                        "Usa la nuova password al prossimo avvio."
                                    )
                                    password_corretta = True
                                else:
                                    return
                            else:
                                QMessageBox.critical(
                                    None, "Codice Errato",
                                    "Codice di recupero non valido!\n\n"
                                    "Contatta l'amministratore del sistema."
                                )
                                return
                        else:
                            return
                    else:
                        return
        
        if not password_corretta:
            return
    
    # === BACKUP AUTOMATICO ===
    db_path = 'credenziali_suite.db'
    backup_manager = BackupManager(db_path)
    
    if backup_manager.necessita_backup():
        successo, path, messaggio = backup_manager.crea_backup()
        if not successo:
            QMessageBox.warning(None, "Avviso Backup", 
                              f"Impossibile creare backup automatico:\n{messaggio}")
    
    # Crea e mostra la finestra principale
    window = MainWindow(crypto_manager, backup_manager)
    window.show()
    
    # Avvia il loop degli eventi
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
