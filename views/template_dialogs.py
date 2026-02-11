"""
Dialog per gestire i template servizi
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QLineEdit, QTextEdit,
                             QComboBox, QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from models.servizio import Servizio
from models.template_servizio import TemplateServizio


class GestioneTemplateDialog(QDialog):
    """Dialog per gestire i template servizi"""
    
    def __init__(self, parent, credenziale_controller):
        super().__init__(parent)
        self.credenziale_controller = credenziale_controller
        self.setWindowTitle("Gestione Template Servizi")
        self.setMinimumSize(900, 600)
        self.init_ui()
        self.carica_template()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel("<h2>📋 Gestione Template Servizi</h2>")
        layout.addWidget(titolo)
        
        info = QLabel("I template permettono di creare servizi rapidamente con configurazioni predefinite")
        info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(info)
        
        # Tabella template
        self.tabella = QTableWidget()
        self.tabella.setColumnCount(5)
        self.tabella.setHorizontalHeaderLabels(["ID", "Nome Template", "Tipo", "Descrizione", "Link"])
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabella.setSelectionMode(QTableWidget.SingleSelection)
        self.tabella.verticalHeader().setVisible(False)
        self.tabella.setColumnHidden(0, True)
        layout.addWidget(self.tabella)
        
        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_nuovo = QPushButton("➕ Nuovo Template")
        btn_nuovo.setObjectName("btn_success")
        btn_nuovo.clicked.connect(self.nuovo_template)
        
        btn_modifica = QPushButton("✏️ Modifica")
        btn_modifica.setObjectName("btn_primary")
        btn_modifica.clicked.connect(self.modifica_template)
        
        btn_elimina = QPushButton("🗑️ Elimina")
        btn_elimina.setObjectName("btn_danger")
        btn_elimina.clicked.connect(self.elimina_template)
        
        btn_chiudi = QPushButton("✅ Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_nuovo)
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        
        layout.addLayout(btn_layout)
    
    def carica_template(self):
        """Carica tutti i template nella tabella"""
        self.tabella.setRowCount(0)
        templates = self.credenziale_controller.ottieni_tutti_template()
        
        for template in templates:
            row = self.tabella.rowCount()
            self.tabella.insertRow(row)
            
            self.tabella.setItem(row, 0, QTableWidgetItem(str(template.id)))
            self.tabella.setItem(row, 1, QTableWidgetItem(template.nome_template))
            self.tabella.setItem(row, 2, QTableWidgetItem(template.tipo))
            self.tabella.setItem(row, 3, QTableWidgetItem(template.descrizione[:100]))
            self.tabella.setItem(row, 4, QTableWidgetItem(template.link[:80]))
    
    def nuovo_template(self):
        """Crea un nuovo template"""
        dialog = TemplateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                template_id = self.credenziale_controller.crea_template(
                    dialog.nome_edit.text(),
                    dialog.tipo_combo.currentText(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.link_edit.text(),
                    dialog.note_edit.toPlainText()
                )
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template creato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore creazione template: {e}")
    
    def modifica_template(self):
        """Modifica il template selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un template da modificare")
            return
        
        template_id = int(self.tabella.item(row, 0).text())
        template = self.credenziale_controller.ottieni_template(template_id)
        
        if not template:
            QMessageBox.critical(self, "Errore", "Template non trovato")
            return
        
        dialog = TemplateDialog(self, template)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.credenziale_controller.modifica_template(
                    template_id,
                    dialog.nome_edit.text(),
                    dialog.tipo_combo.currentText(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.link_edit.text(),
                    dialog.note_edit.toPlainText()
                )
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template modificato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore modifica template: {e}")
    
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
                self.credenziale_controller.elimina_template(template_id)
                self.carica_template()
                QMessageBox.information(self, "Successo", "Template eliminato con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore eliminazione template: {e}")


class TemplateDialog(QDialog):
    """Dialog per creare/modificare un template"""
    
    def __init__(self, parent, template: TemplateServizio = None):
        super().__init__(parent)
        self.template = template
        self.setWindowTitle("Modifica Template" if template else "Nuovo Template")
        self.setMinimumWidth(600)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Nome template
        self.nome_edit = QLineEdit()
        self.nome_edit.setPlaceholderText("es: CRM Standard, RDP Dominio...")
        if self.template:
            self.nome_edit.setText(self.template.nome_template)
        layout.addRow("Nome Template *:", self.nome_edit)
        
        # Tipo servizio
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(Servizio.TIPI_DISPONIBILI)
        if self.template:
            index = self.tipo_combo.findText(self.template.tipo)
            if index >= 0:
                self.tipo_combo.setCurrentIndex(index)
        layout.addRow("Tipo Servizio *:", self.tipo_combo)
        
        # Descrizione predefinita
        self.descrizione_edit = QTextEdit()
        self.descrizione_edit.setMaximumHeight(80)
        self.descrizione_edit.setPlaceholderText("Descrizione che verrà usata per i servizi creati da questo template...")
        if self.template:
            self.descrizione_edit.setPlainText(self.template.descrizione)
        layout.addRow("Descrizione:", self.descrizione_edit)
        
        # Link predefinito
        self.link_edit = QLineEdit()
        self.link_edit.setPlaceholderText("URL predefinito (opzionale)")
        if self.template:
            self.link_edit.setText(self.template.link)
        layout.addRow("Link:", self.link_edit)
        
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


class SelezionaTemplateDialog(QDialog):
    """Dialog per selezionare un template da cui creare un servizio"""
    
    def __init__(self, parent, credenziale_controller, tipo_servizio=None):
        super().__init__(parent)
        self.credenziale_controller = credenziale_controller
        self.tipo_servizio = tipo_servizio
        self.template_selezionato = None
        self.setWindowTitle("Seleziona Template")
        self.setMinimumSize(600, 450)
        self.init_ui()
        self.carica_template()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel("<h3>📋 Seleziona un Template</h3>")
        layout.addWidget(titolo)
        
        info = QLabel("Scegli un template da cui creare il nuovo servizio")
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
        
        if self.tipo_servizio:
            templates = self.credenziale_controller.ottieni_template_per_tipo(self.tipo_servizio)
        else:
            templates = self.credenziale_controller.ottieni_tutti_template()
        
        for template in templates:
            item = QListWidgetItem()
            item.setText(f"📋 {template.nome_template} ({template.tipo})")
            item.setData(Qt.UserRole, template.id)
            item.setToolTip(f"{template.descrizione[:200]}\n\nLink: {template.link}")
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
        
        self.template_selezionato = self.credenziale_controller.ottieni_template(
            item.data(Qt.UserRole)
        )
        self.accept()
