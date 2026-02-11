"""
Dialog per gestire i template cliente (cliente + servizi + credenziali)
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QLineEdit, QTextEdit,
                             QLabel, QListWidget, QListWidgetItem, QInputDialog)
from PyQt5.QtCore import Qt


class GestioneTemplateClienteDialog(QDialog):
    """Dialog per gestire i template cliente"""
    
    def __init__(self, parent, credenziale_controller):
        super().__init__(parent)
        self.credenziale_controller = credenziale_controller
        self.setWindowTitle("Gestione Template Cliente")
        self.setMinimumSize(900, 600)
        self.init_ui()
        self.carica_template()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel("<h2>👥 Gestione Template Cliente</h2>")
        layout.addWidget(titolo)
        
        info = QLabel("I template permettono di creare clienti completi con servizi e credenziali predefiniti")
        info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(info)
        
        # Tabella template
        self.tabella = QTableWidget()
        self.tabella.setColumnCount(4)
        self.tabella.setHorizontalHeaderLabels(["ID", "Nome Template", "Descrizione", "N. Servizi"])
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabella.setSelectionMode(QTableWidget.SingleSelection)
        self.tabella.verticalHeader().setVisible(False)
        self.tabella.setColumnHidden(0, True)
        layout.addWidget(self.tabella)
        
        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_nuovo = QPushButton("➕ Nuovo Template Cliente")
        btn_nuovo.setObjectName("btn_success")
        btn_nuovo.clicked.connect(self.nuovo_template)
        
        btn_modifica = QPushButton("✏️ Modifica")
        btn_modifica.setObjectName("btn_primary")
        btn_modifica.clicked.connect(self.modifica_template)
        
        btn_servizi = QPushButton("⚙️ Gestisci Servizi")
        btn_servizi.setObjectName("btn_neutral")
        btn_servizi.clicked.connect(self.gestisci_servizi)
        
        btn_elimina = QPushButton("🗑️ Elimina")
        btn_elimina.setObjectName("btn_danger")
        btn_elimina.clicked.connect(self.elimina_template)
        
        btn_chiudi = QPushButton("✅ Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_nuovo)
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_servizi)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        
        layout.addLayout(btn_layout)
    
    def carica_template(self):
        """Carica tutti i template nella tabella"""
        self.tabella.setRowCount(0)
        templates = self.credenziale_controller.ottieni_tutti_template_cliente()
        
        for template in templates:
            row = self.tabella.rowCount()
            self.tabella.insertRow(row)
            
            servizi = self.credenziale_controller.ottieni_servizi_template_cliente(template.id)
            
            self.tabella.setItem(row, 0, QTableWidgetItem(str(template.id)))
            self.tabella.setItem(row, 1, QTableWidgetItem(template.nome_template))
            self.tabella.setItem(row, 2, QTableWidgetItem(template.descrizione_cliente[:100]))
            self.tabella.setItem(row, 3, QTableWidgetItem(str(len(servizi))))
    
    def nuovo_template(self):
        """Crea un nuovo template cliente"""
        dialog = TemplateClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.credenziale_controller.crea_template_cliente(
                    dialog.nome_edit.text(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.note_edit.toPlainText()
                )
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template cliente creato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore creazione template: {e}")
    
    def modifica_template(self):
        """Modifica il template selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un template da modificare")
            return
        
        template_id = int(self.tabella.item(row, 0).text())
        template = self.credenziale_controller.ottieni_template_cliente(template_id)
        
        if not template:
            QMessageBox.critical(self, "Errore", "Template non trovato")
            return
        
        dialog = TemplateClienteDialog(self, template)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.credenziale_controller.modifica_template_cliente(
                    template_id,
                    dialog.nome_edit.text(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.note_edit.toPlainText()
                )
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template modificato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore modifica template: {e}")
    
    def gestisci_servizi(self):
        """Gestisce i servizi del template selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un template per gestire i servizi")
            return
        
        template_id = int(self.tabella.item(row, 0).text())
        template = self.credenziale_controller.ottieni_template_cliente(template_id)
        
        if not template:
            QMessageBox.critical(self, "Errore", "Template non trovato")
            return
        
        dialog = GestioneServiziTemplateClienteDialog(self, self.credenziale_controller, template)
        dialog.exec_()
        self.carica_template()  # Ricarica per aggiornare conteggio servizi
    
    def elimina_template(self):
        """Elimina il template selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un template da eliminare")
            return
        
        template_id = int(self.tabella.item(row, 0).text())
        nome = self.tabella.item(row, 1).text()
        
        risposta = QMessageBox.question(
            self, "Conferma",
            f"Vuoi eliminare il template '{nome}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            try:
                self.credenziale_controller.elimina_template_cliente(template_id)
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template eliminato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore eliminazione template: {e}")


class TemplateClienteDialog(QDialog):
    """Dialog per creare/modificare un template cliente"""
    
    def __init__(self, parent, template=None):
        super().__init__(parent)
        self.template = template
        self.setWindowTitle("Modifica Template Cliente" if template else "Nuovo Template Cliente")
        self.setMinimumWidth(600)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Nome template
        self.nome_edit = QLineEdit()
        self.nome_edit.setPlaceholderText("es: Cliente Standard, Cliente Enterprise...")
        if self.template:
            self.nome_edit.setText(self.template.nome_template)
        layout.addRow("Nome Template *:", self.nome_edit)
        
        # Descrizione predefinita cliente
        self.descrizione_edit = QTextEdit()
        self.descrizione_edit.setMaximumHeight(80)
        self.descrizione_edit.setPlaceholderText("Descrizione che verrà usata per i clienti creati da questo template...")
        if self.template:
            self.descrizione_edit.setPlainText(self.template.descrizione_cliente)
        layout.addRow("Descrizione Cliente:", self.descrizione_edit)
        
        # Note template
        self.note_edit = QTextEdit()
        self.note_edit.setMaximumHeight(80)
        self.note_edit.setPlaceholderText("Note o istruzioni per l'uso di questo template...")
        if self.template:
            self.note_edit.setPlainText(self.template.note_template)
        layout.addRow("Note Template:", self.note_edit)
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_salva = QPushButton("💾 Salva")
        btn_salva.setObjectName("btn_success")
        btn_salva.clicked.connect(self.accept)
        
        btn_annulla = QPushButton("❌ Annulla")
        btn_annulla.setObjectName("btn_neutral")
        btn_annulla.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        
        layout.addRow(btn_layout)


class GestioneServiziTemplateClienteDialog(QDialog):
    """Dialog per gestire i servizi associati a un template cliente"""
    
    def __init__(self, parent, credenziale_controller, template_cliente):
        super().__init__(parent)
        self.credenziale_controller = credenziale_controller
        self.template_cliente = template_cliente
        self.setWindowTitle(f"Servizi - {template_cliente.nome_template}")
        self.setMinimumSize(700, 500)
        self.init_ui()
        self.carica_servizi()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel(f"<h3>⚙️ Servizi per {self.template_cliente.nome_template}</h3>")
        layout.addWidget(titolo)
        
        info = QLabel("Seleziona quali template servizio verranno creati quando si usa questo template cliente")
        info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(info)
        
        # Lista servizi
        self.lista = QListWidget()
        layout.addWidget(self.lista)
        
        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_aggiungi = QPushButton("➕ Aggiungi Servizio")
        btn_aggiungi.setObjectName("btn_success")
        btn_aggiungi.clicked.connect(self.aggiungi_servizio)
        
        btn_rimuovi = QPushButton("➖ Rimuovi")
        btn_rimuovi.setObjectName("btn_danger")
        btn_rimuovi.clicked.connect(self.rimuovi_servizio)
        
        btn_chiudi = QPushButton("✅ Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_aggiungi)
        btn_layout.addWidget(btn_rimuovi)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        
        layout.addLayout(btn_layout)
    
    def carica_servizi(self):
        """Carica i servizi associati al template"""
        self.lista.clear()
        servizi = self.credenziale_controller.ottieni_servizi_template_cliente(self.template_cliente.id)
        
        for servizio in servizi:
            item = QListWidgetItem()
            item.setText(f"⚙️ {servizio.nome_template} ({servizio.tipo})")
            item.setData(Qt.UserRole, servizio.id)
            self.lista.addItem(item)
    
    def aggiungi_servizio(self):
        """Aggiungi un template servizio al template cliente"""
        # Recupera tutti i template servizio disponibili
        tutti_servizi = self.credenziale_controller.ottieni_tutti_template()
        servizi_attuali = self.credenziale_controller.ottieni_servizi_template_cliente(self.template_cliente.id)
        servizi_attuali_ids = {s.id for s in servizi_attuali}
        
        # Filtra quelli non ancora associati
        servizi_disponibili = [s for s in tutti_servizi if s.id not in servizi_attuali_ids]
        
        if not servizi_disponibili:
            QMessageBox.information(self, "Info", "Tutti i template servizio sono già stati aggiunti")
            return
        
        # Crea lista nomi
        nomi_servizi = [f"{s.nome_template} ({s.tipo})" for s in servizi_disponibili]
        
        nome_selezionato, ok = QInputDialog.getItem(
            self,
            "Seleziona Template Servizio",
            "Scegli un template servizio da aggiungere:",
            nomi_servizi,
            0,
            False
        )
        
        if ok and nome_selezionato:
            idx = nomi_servizi.index(nome_selezionato)
            servizio_da_aggiungere = servizi_disponibili[idx]
            
            try:
                self.credenziale_controller.aggiungi_servizio_a_template_cliente(
                    self.template_cliente.id,
                    servizio_da_aggiungere.id
                )
                self.carica_servizi()
                QMessageBox.information(self, "Successo", "Servizio aggiunto con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore aggiunta servizio: {e}")
    
    def rimuovi_servizio(self):
        """Rimuovi il servizio selezionato"""
        item = self.lista.currentItem()
        if not item:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da rimuovere")
            return
        
        servizio_id = item.data(Qt.UserRole)
        
        risposta = QMessageBox.question(
            self, "Conferma",
            "Vuoi rimuovere questo servizio dal template?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            try:
                self.credenziale_controller.rimuovi_servizio_da_template_cliente(
                    self.template_cliente.id,
                    servizio_id
                )
                self.carica_servizi()
                QMessageBox.information(self, "Successo", "Servizio rimosso con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore rimozione servizio: {e}")


class SelezionaTemplateClienteDialog(QDialog):
    """Dialog per selezionare un template cliente da cui creare un cliente completo"""
    
    def __init__(self, parent, credenziale_controller):
        super().__init__(parent)
        self.credenziale_controller = credenziale_controller
        self.template_selezionato = None
        self.setWindowTitle("Seleziona Template Cliente")
        self.setMinimumSize(600, 450)
        self.init_ui()
        self.carica_template()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel("<h3>👥 Seleziona un Template Cliente</h3>")
        layout.addWidget(titolo)
        
        info = QLabel("Scegli un template per creare un cliente completo con servizi e credenziali")
        info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(info)
        
        # Lista template
        self.lista = QListWidget()
        self.lista.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.lista)
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_seleziona = QPushButton("✅ Seleziona")
        btn_seleziona.setObjectName("btn_success")
        btn_seleziona.clicked.connect(self.seleziona)
        
        btn_annulla = QPushButton("❌ Annulla")
        btn_annulla.setObjectName("btn_neutral")
        btn_annulla.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_seleziona)
        btn_layout.addWidget(btn_annulla)
        
        layout.addLayout(btn_layout)
    
    def carica_template(self):
        """Carica i template nella lista"""
        self.lista.clear()
        
        templates = self.credenziale_controller.ottieni_tutti_template_cliente()
        
        for template in templates:
            servizi = self.credenziale_controller.ottieni_servizi_template_cliente(template.id)
            item = QListWidgetItem()
            item.setText(f"👥 {template.nome_template} ({len(servizi)} servizi)")
            item.setData(Qt.UserRole, template.id)
            item.setToolTip(f"{template.descrizione_cliente}\n\nServizi: {', '.join([s.nome_template for s in servizi])}")
            self.lista.addItem(item)
        
        if self.lista.count() == 0:
            item = QListWidgetItem("Nessun template disponibile")
            item.setFlags(Qt.NoItemFlags)
            self.lista.addItem(item)
    
    def seleziona(self):
        """Conferma la selezione"""
        item = self.lista.currentItem()
        if not item or not item.data(Qt.UserRole):
            QMessageBox.warning(self, "Attenzione", "Seleziona un template")
            return
        
        self.template_selezionato = self.credenziale_controller.ottieni_template_cliente(
            item.data(Qt.UserRole)
        )
        self.accept()
