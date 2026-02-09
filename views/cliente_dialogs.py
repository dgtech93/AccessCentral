"""
Dialog per gestire Consulenti e Contatti del Cliente
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QLabel, QMessageBox, QFormLayout,
                             QLineEdit, QListWidgetItem)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont, QColor
from controllers.risorse_controller import RisorseController


class GestioneConsulentiClienteDialog(QDialog):
    """Dialog per associare/disassociare consulenti a un cliente"""
    
    def __init__(self, parent, cliente_id: int, cliente_nome: str, risorse_controller: RisorseController):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.risorse_controller = risorse_controller
        self.setWindowTitle(f"Consulenti di {cliente_nome}")
        self.setMinimumSize(700, 500)
        
        # Applica stile dalla finestra principale
        if hasattr(parent, 'styleSheet') and parent.styleSheet():
            self.setStyleSheet(parent.styleSheet())
        
        self.init_ui()
        self.carica_dati()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        titolo = QLabel("<h2 style='color: #1976D2;'>👥 Gestione Consulenti</h2>")
        layout.addWidget(titolo)
        layout.addSpacing(10)
        
        # Layout orizzontale con due liste
        lists_layout = QHBoxLayout()
        lists_layout.setSpacing(15)
        
        # Lista consulenti disponibili
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("<b>Consulenti Disponibili:</b>"))
        self.list_disponibili = QListWidget()
        left_layout.addWidget(self.list_disponibili)
        
        btn_aggiungi = QPushButton("➡️ Aggiungi")
        btn_aggiungi.setObjectName("btn_success")
        btn_aggiungi.clicked.connect(self.aggiungi_consulente)
        left_layout.addWidget(btn_aggiungi)
        
        lists_layout.addLayout(left_layout)
        
        # Lista consulenti associati
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("<b>Consulenti Associati:</b>"))
        self.list_associati = QListWidget()
        right_layout.addWidget(self.list_associati)
        
        btn_rimuovi = QPushButton("⬅️ Rimuovi")
        btn_rimuovi.setObjectName("btn_danger")
        btn_rimuovi.clicked.connect(self.rimuovi_consulente)
        right_layout.addWidget(btn_rimuovi)
        
        lists_layout.addLayout(right_layout)
        
        layout.addLayout(lists_layout)
        layout.addSpacing(10)
        
        # Pulsante chiudi
        btn_chiudi = QPushButton("✓ Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.setMinimumWidth(120)
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        layout.addLayout(btn_layout)
    
    def carica_dati(self):
        """Carica le liste di consulenti"""
        # Ottieni tutti i consulenti
        tutti_consulenti = self.risorse_controller.ottieni_tutti_consulenti()
        
        # Ottieni consulenti già associati
        consulenti_associati = self.risorse_controller.ottieni_consulenti_cliente(self.cliente_id)
        consulenti_associati_ids = {c.id for c in consulenti_associati}
        
        # Popola lista disponibili
        self.list_disponibili.clear()
        for consulente in tutti_consulenti:
            if consulente.id not in consulenti_associati_ids:
                item = QListWidgetItem(f"{consulente.nome} - {consulente.competenza or 'N/A'}")
                item.setData(Qt.UserRole, consulente.id)
                self.list_disponibili.addItem(item)
        
        # Popola lista associati
        self.list_associati.clear()
        for consulente in consulenti_associati:
            item = QListWidgetItem(f"{consulente.nome} - {consulente.competenza or 'N/A'}")
            item.setData(Qt.UserRole, consulente.id)
            self.list_associati.addItem(item)
    
    def aggiungi_consulente(self):
        """Associa il consulente selezionato al cliente"""
        item = self.list_disponibili.currentItem()
        if not item:
            QMessageBox.warning(self, "Attenzione", "Seleziona un consulente da aggiungere")
            return
        
        consulente_id = item.data(Qt.UserRole)
        self.risorse_controller.associa_consulente_cliente(self.cliente_id, consulente_id)
        self.carica_dati()
    
    def rimuovi_consulente(self):
        """Disassocia il consulente selezionato dal cliente"""
        item = self.list_associati.currentItem()
        if not item:
            QMessageBox.warning(self, "Attenzione", "Seleziona un consulente da rimuovere")
            return
        
        consulente_id = item.data(Qt.UserRole)
        self.risorse_controller.disassocia_consulente_cliente(self.cliente_id, consulente_id)
        self.carica_dati()


class GestioneContattiDialog(QDialog):
    """Dialog per gestire i contatti (rubrica) di un cliente"""
    
    def __init__(self, parent, cliente_id: int, cliente_nome: str, risorse_controller: RisorseController):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.risorse_controller = risorse_controller
        self.setWindowTitle(f"Rubrica Contatti - {cliente_nome}")
        self.setMinimumSize(900, 600)
        
        # Applica stile dalla finestra principale
        if hasattr(parent, 'styleSheet') and parent.styleSheet():
            self.setStyleSheet(parent.styleSheet())
        
        self.init_ui()
        self.carica_dati()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        titolo = QLabel("<h2 style='color: #1976D2;'>📇 Rubrica Contatti</h2>")
        layout.addWidget(titolo)
        layout.addSpacing(10)
        
        # Pulsanti azione
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_nuovo = QPushButton("➕ Nuovo")
        self.btn_modifica = QPushButton("✏️ Modifica")
        self.btn_elimina = QPushButton("🗑️ Elimina")
        self.btn_invia_email = QPushButton("📧 Email")
        
        self.btn_nuovo.setObjectName("btn_primary")
        self.btn_modifica.setObjectName("btn_secondary")
        self.btn_elimina.setObjectName("btn_danger")
        self.btn_invia_email.setObjectName("btn_action")
        
        self.btn_nuovo.clicked.connect(self.nuovo_contatto)
        self.btn_modifica.clicked.connect(self.modifica_contatto)
        self.btn_elimina.clicked.connect(self.elimina_contatto)
        self.btn_invia_email.clicked.connect(self.invia_email_contatto)
        self.btn_invia_email.setEnabled(False)
        
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addWidget(self.btn_invia_email)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        
        # Lista contatti
        self.list_contatti = QListWidget()
        self.list_contatti.itemDoubleClicked.connect(self.mostra_dettaglio_contatto)
        self.list_contatti.itemClicked.connect(self.contatto_selezionato)
        layout.addWidget(self.list_contatti)
        
        # Pulsante chiudi
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.accept)
        layout.addWidget(btn_chiudi)
    
    def carica_dati(self):
        """Carica i contatti del cliente"""
        contatti = self.risorse_controller.ottieni_contatti_cliente(self.cliente_id)
        
        self.list_contatti.clear()
        for contatto in contatti:
            # Costruisci il testo HTML
            html_text = f"👤 <b>{contatto.nome}</b>"
            if contatto.ruolo:
                html_text += f" ({contatto.ruolo})"
            
            # Aggiungi email cliccabile subito dopo
            if contatto.email:
                html_text += f" | 📧 <a href='mailto:{contatto.email}' style='color: blue; text-decoration: underline;'>{contatto.email}</a>"
            
            # Aggiungi telefoni
            if contatto.telefono:
                html_text += f" | ☎️ {contatto.telefono}"
            if contatto.cellulare:
                html_text += f" | 📱 {contatto.cellulare}"
            
            item = QListWidgetItem()
            item.setData(Qt.UserRole, contatto.id)
            
            if contatto.email:
                item.setToolTip(f"Doppio click per modificare | Click su email per scrivere")
            else:
                item.setToolTip("Doppio click per modificare")
            
            self.list_contatti.addItem(item)
            
            # Crea widget custom con label HTML
            from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout as HBox
            widget = QWidget()
            widget.setAttribute(Qt.WA_TransparentForMouseEvents)  # Permette click sulla riga
            layout_widget = HBox()
            layout_widget.setContentsMargins(5, 2, 5, 2)
            
            label = QLabel()
            label.setText(html_text)
            label.setTextFormat(Qt.RichText)
            label.setOpenExternalLinks(True)  # Abilita click sui link
            label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)  # Solo i link sono cliccabili
            
            layout_widget.addWidget(label)
            layout_widget.addStretch()
            
            widget.setLayout(layout_widget)
            item.setSizeHint(widget.sizeHint())
            self.list_contatti.setItemWidget(item, widget)
    
    def contatto_selezionato(self, item: QListWidgetItem):
        """Gestisce la selezione di un contatto"""
        if item:
            contatto_id = item.data(Qt.UserRole)
            contatto = self.risorse_controller.ottieni_contatto(contatto_id)
            # Abilita pulsante email solo se il contatto ha un'email
            self.btn_invia_email.setEnabled(contatto and bool(contatto.email))
    
    def mostra_dettaglio_contatto(self):
        """Mostra il dettaglio del contatto selezionato in sola lettura"""
        item = self.list_contatti.currentItem()
        if not item:
            return
        
        contatto_id = item.data(Qt.UserRole)
        contatto = self.risorse_controller.ottieni_contatto(contatto_id)
        
        if not contatto:
            return
        
        # Crea un messaggio HTML con i dettagli
        html = f"<h3>👤 {contatto.nome}</h3>"
        
        if contatto.ruolo:
            html += f"<p><b>Ruolo:</b> {contatto.ruolo}</p>"
        
        if contatto.email:
            html += f"<p><b>Email:</b> <a href='mailto:{contatto.email}' style='color: blue;'>{contatto.email}</a></p>"
        
        if contatto.telefono:
            html += f"<p><b>Telefono:</b> {contatto.telefono}</p>"
        
        if contatto.cellulare:
            html += f"<p><b>Cellulare:</b> {contatto.cellulare}</p>"
        
        # Mostra dialog con dettagli
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Dettaglio Contatto - {contatto.nome}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        from PyQt5.QtWidgets import QTextBrowser
        text_browser = QTextBrowser()
        text_browser.setHtml(html)
        text_browser.setOpenExternalLinks(True)
        text_browser.setMinimumHeight(200)
        
        layout.addWidget(text_browser)
        
        btn_layout = QHBoxLayout()
        btn_modifica = QPushButton("✏️ Modifica")
        btn_chiudi = QPushButton("Chiudi")
        
        btn_modifica.clicked.connect(lambda: (dialog.accept(), self.modifica_contatto()))
        btn_chiudi.clicked.connect(dialog.accept)
        
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_chiudi)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def invia_email_contatto(self):
        """Apre il client email per il contatto selezionato"""
        item = self.list_contatti.currentItem()
        if not item:
            return
        
        contatto_id = item.data(Qt.UserRole)
        contatto = self.risorse_controller.ottieni_contatto(contatto_id)
        
        if contatto and contatto.email:
            QDesktopServices.openUrl(QUrl(f"mailto:{contatto.email}"))
        else:
            QMessageBox.warning(self, "Attenzione", "Questo contatto non ha un'email")
    
    def nuovo_contatto(self):
        """Crea un nuovo contatto"""
        dialog = ContattoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.crea_contatto(
                    self.cliente_id,
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text(),
                    dialog.ruolo_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Contatto creato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def modifica_contatto(self):
        """Modifica il contatto selezionato"""
        item = self.list_contatti.currentItem()
        if not item:
            QMessageBox.warning(self, "Attenzione", "Seleziona un contatto da modificare")
            return
        
        contatto_id = item.data(Qt.UserRole)
        contatto = self.risorse_controller.ottieni_contatto(contatto_id)
        
        dialog = ContattoDialog(self, contatto)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.modifica_contatto(
                    contatto_id,
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text(),
                    dialog.ruolo_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Contatto modificato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_contatto(self):
        """Elimina il contatto selezionato"""
        item = self.list_contatti.currentItem()
        if not item:
            QMessageBox.warning(self, "Attenzione", "Seleziona un contatto da eliminare")
            return
        
        contatto_id = item.data(Qt.UserRole)
        contatto = self.risorse_controller.ottieni_contatto(contatto_id)
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare il contatto '{contatto.nome}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            self.risorse_controller.elimina_contatto(contatto_id)
            self.carica_dati()
            QMessageBox.information(self, "Successo", "Contatto eliminato con successo!")


class ContattoDialog(QDialog):
    """Dialog per creare/modificare un contatto"""
    
    def __init__(self, parent, contatto=None):
        super().__init__(parent)
        self.contatto = contatto
        self.setWindowTitle("Modifica Contatto" if contatto else "Nuovo Contatto")
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.nome_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.cellulare_edit = QLineEdit()
        self.ruolo_edit = QLineEdit()
        
        if self.contatto:
            self.nome_edit.setText(self.contatto.nome)
            self.email_edit.setText(self.contatto.email or "")
            self.telefono_edit.setText(self.contatto.telefono or "")
            self.cellulare_edit.setText(self.contatto.cellulare or "")
            self.ruolo_edit.setText(self.contatto.ruolo or "")
        
        layout.addRow("Nome *:", self.nome_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Telefono:", self.telefono_edit)
        layout.addRow("Cellulare:", self.cellulare_edit)
        layout.addRow("Ruolo:", self.ruolo_edit)
        
        btn_layout = QHBoxLayout()
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)
