"""
Dialog per gestire la master password
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt
import os
import json


class MasterPasswordDialog(QDialog):
    """Dialog per inserire/creare la master password"""
    
    def __init__(self, parent=None, prima_volta=False):
        super().__init__(parent)
        self.prima_volta = prima_volta
        self.password = None
        self.init_ui()
    
    def init_ui(self):
        """Inizializza l'interfaccia"""
        if self.prima_volta:
            self.setWindowTitle("Imposta Master Password")
        else:
            self.setWindowTitle("AccessCentral - Login")
        
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titolo
        if self.prima_volta:
            titolo = QLabel("<h2>🔐 Imposta Master Password</h2>")
            descrizione = QLabel(
                "Crea una password master per proteggere l'applicazione.\n"
                "⚠️ IMPORTANTE: Non dimenticare questa password!\n"
                "Senza di essa non potrai accedere alle tue credenziali."
            )
        else:
            titolo = QLabel("<h2>🔐 Inserisci Master Password</h2>")
            descrizione = QLabel("Inserisci la password master per accedere all'applicazione.")
        
        titolo.setAlignment(Qt.AlignCenter)
        descrizione.setWordWrap(True)
        descrizione.setStyleSheet("color: #666; padding: 10px;")
        
        layout.addWidget(titolo)
        layout.addWidget(descrizione)
        
        # Campo password
        layout.addWidget(QLabel("Password:"))
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setMinimumHeight(35)
        self.txt_password.returnPressed.connect(self.verifica_password)
        layout.addWidget(self.txt_password)
        
        # Se è prima volta, chiedi conferma
        if self.prima_volta:
            layout.addWidget(QLabel("Conferma Password:"))
            self.txt_conferma = QLineEdit()
            self.txt_conferma.setEchoMode(QLineEdit.Password)
            self.txt_conferma.setMinimumHeight(35)
            self.txt_conferma.returnPressed.connect(self.verifica_password)
            layout.addWidget(self.txt_conferma)
        
        # Mostra password
        self.chk_mostra = QCheckBox("Mostra password")
        self.chk_mostra.stateChanged.connect(self.toggle_visibilita_password)
        layout.addWidget(self.chk_mostra)
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        
        self.btn_ok = QPushButton("Conferma" if self.prima_volta else "Accedi")
        self.btn_ok.setObjectName("btn_primary")
        self.btn_ok.setMinimumHeight(40)
        self.btn_ok.clicked.connect(self.verifica_password)
        
        btn_esci = QPushButton("Esci")
        btn_esci.setObjectName("btn_neutral")
        btn_esci.setMinimumHeight(40)
        btn_esci.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_esci)
        btn_layout.addWidget(self.btn_ok)
        
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        
        # Focus sul campo password
        self.txt_password.setFocus()
    
    def toggle_visibilita_password(self, state):
        """Mostra/nasconde la password"""
        if state == Qt.Checked:
            self.txt_password.setEchoMode(QLineEdit.Normal)
            if self.prima_volta:
                self.txt_conferma.setEchoMode(QLineEdit.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.Password)
            if self.prima_volta:
                self.txt_conferma.setEchoMode(QLineEdit.Password)
    
    def verifica_password(self):
        """Verifica e salva la password"""
        password = self.txt_password.text()
        
        if not password:
            QMessageBox.warning(self, "Errore", "Inserisci una password")
            return
        
        if self.prima_volta:
            # Verifica lunghezza minima
            if len(password) < 6:
                QMessageBox.warning(
                    self, "Password Troppo Corta", 
                    "La password deve essere di almeno 6 caratteri"
                )
                return
            
            # Verifica conferma
            conferma = self.txt_conferma.text()
            if password != conferma:
                QMessageBox.warning(
                    self, "Errore", 
                    "Le password non corrispondono"
                )
                return
        
        self.password = password
        self.accept()
    
    def get_password(self):
        """Ritorna la password inserita"""
        return self.password


class GeneratorePasswordDialog(QDialog):
    """Dialog per generare password sicure"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_generata = None
        self.init_ui()
    
    def init_ui(self):
        """Inizializza l'interfaccia"""
        self.setWindowTitle("Genera Password Sicura")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        
        # Titolo
        titolo = QLabel("<h2>🎲 Generatore Password</h2>")
        titolo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titolo)
        
        # Lunghezza
        lunghezza_layout = QHBoxLayout()
        lunghezza_layout.addWidget(QLabel("Lunghezza:"))
        
        from PyQt5.QtWidgets import QSpinBox
        self.spin_lunghezza = QSpinBox()
        self.spin_lunghezza.setMinimum(8)
        self.spin_lunghezza.setMaximum(64)
        self.spin_lunghezza.setValue(16)
        lunghezza_layout.addWidget(self.spin_lunghezza)
        lunghezza_layout.addStretch()
        
        layout.addLayout(lunghezza_layout)
        layout.addSpacing(10)
        
        # Opzioni
        self.chk_maiuscole = QCheckBox("Lettere Maiuscole (A-Z)")
        self.chk_maiuscole.setChecked(True)
        layout.addWidget(self.chk_maiuscole)
        
        self.chk_numeri = QCheckBox("Numeri (0-9)")
        self.chk_numeri.setChecked(True)
        layout.addWidget(self.chk_numeri)
        
        self.chk_simboli = QCheckBox("Simboli (!@#$%...)")
        self.chk_simboli.setChecked(True)
        layout.addWidget(self.chk_simboli)
        
        layout.addSpacing(15)
        
        # Password generata
        layout.addWidget(QLabel("Password generata:"))
        self.txt_password = QLineEdit()
        self.txt_password.setReadOnly(True)
        self.txt_password.setMinimumHeight(40)
        self.txt_password.setStyleSheet("font-size: 14pt; font-family: monospace;")
        layout.addWidget(self.txt_password)
        
        layout.addSpacing(10)
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        
        btn_genera = QPushButton("🎲 Genera")
        btn_genera.setObjectName("btn_secondary")
        btn_genera.clicked.connect(self.genera_password)
        
        btn_copia = QPushButton("📋 Copia")
        btn_copia.setObjectName("btn_action")
        btn_copia.clicked.connect(self.copia_password)
        
        btn_usa = QPushButton("✓ Usa Password")
        btn_usa.setObjectName("btn_success")
        btn_usa.clicked.connect(self.usa_password)
        
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setObjectName("btn_neutral")
        btn_annulla.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_genera)
        btn_layout.addWidget(btn_copia)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_annulla)
        btn_layout.addWidget(btn_usa)
        
        layout.addLayout(btn_layout)
        
        # Genera subito una password
        self.genera_password()
    
    def genera_password(self):
        """Genera una nuova password"""
        from utils.crypto_manager import CryptoManager
        
        lunghezza = self.spin_lunghezza.value()
        usa_maiuscole = self.chk_maiuscole.isChecked()
        usa_numeri = self.chk_numeri.isChecked()
        usa_simboli = self.chk_simboli.isChecked()
        
        # Almeno una opzione deve essere selezionata
        if not (usa_maiuscole or usa_numeri or usa_simboli):
            QMessageBox.warning(
                self, "Attenzione", 
                "Seleziona almeno un tipo di carattere"
            )
            return
        
        password = CryptoManager.genera_password_sicura(
            lunghezza, usa_maiuscole, usa_numeri, usa_simboli
        )
        
        self.txt_password.setText(password)
        self.password_generata = password
    
    def copia_password(self):
        """Copia la password negli appunti"""
        from PyQt5.QtWidgets import QApplication
        
        password = self.txt_password.text()
        if password:
            QApplication.clipboard().setText(password)
            QMessageBox.information(
                self, "Copiato", 
                "Password copiata negli appunti!"
            )
    
    def usa_password(self):
        """Usa la password generata"""
        if self.password_generata:
            self.accept()
    
    def get_password(self):
        """Ritorna la password generata"""
        return self.password_generata


class RecoveryCodeDialog(QDialog):
    """Dialog per inserire il codice di recupero"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recovery_code = None
        self.init_ui()
    
    def init_ui(self):
        """Inizializza l'interfaccia"""
        self.setWindowTitle("Recupero Password")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titolo
        titolo = QLabel("<h2>🔑 Recupero Password</h2>")
        titolo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titolo)
        
        # Descrizione
        descrizione = QLabel(
            "Inserisci il codice di recupero che hai salvato\n"
            "durante la prima configurazione.\n\n"
            "Formato: XXXX-XXXX-XXXX-XXXX"
        )
        descrizione.setWordWrap(True)
        descrizione.setStyleSheet("color: #666; padding: 10px;")
        descrizione.setAlignment(Qt.AlignCenter)
        layout.addWidget(descrizione)
        
        layout.addSpacing(10)
        
        # Campo codice
        layout.addWidget(QLabel("Codice di Recupero:"))
        self.txt_code = QLineEdit()
        self.txt_code.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        self.txt_code.setMinimumHeight(40)
        self.txt_code.setStyleSheet("font-size: 14pt; font-family: monospace; text-transform: uppercase;")
        self.txt_code.setMaxLength(19)  # 16 caratteri + 3 trattini
        self.txt_code.returnPressed.connect(self.verifica_codice)
        layout.addWidget(self.txt_code)
        
        layout.addSpacing(10)
        
        # Info
        info = QLabel(
            "⚠️ Se non hai il codice di recupero, non sarà possibile\n"
            "recuperare l'accesso ai dati criptati."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #d9534f; font-size: 10pt; padding: 10px;")
        layout.addWidget(info)
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        
        btn_ok = QPushButton("Recupera Password")
        btn_ok.setObjectName("btn_primary")
        btn_ok.setMinimumHeight(40)
        btn_ok.clicked.connect(self.verifica_codice)
        
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setObjectName("btn_neutral")
        btn_annulla.setMinimumHeight(40)
        btn_annulla.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_annulla)
        btn_layout.addWidget(btn_ok)
        
        layout.addLayout(btn_layout)
        
        # Focus sul campo
        self.txt_code.setFocus()
    
    def verifica_codice(self):
        """Verifica il codice inserito"""
        code = self.txt_code.text().strip().upper()
        
        if not code:
            QMessageBox.warning(self, "Errore", "Inserisci il codice di recupero")
            return
        
        # Rimuovi spazi e converti in maiuscolo
        code = code.replace(" ", "")
        
        # Verifica formato base (16 caratteri + trattini)
        if len(code) < 16:
            QMessageBox.warning(
                self, "Formato Errato", 
                "Il codice deve essere nel formato XXXX-XXXX-XXXX-XXXX"
            )
            return
        
        self.recovery_code = code
        self.accept()
    
    def get_code(self):
        """Ritorna il codice inserito"""
        return self.recovery_code
