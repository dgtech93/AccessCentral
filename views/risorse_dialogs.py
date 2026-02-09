"""
Dialog per gestire PM, Consulenti e Contatti
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from models.pm import PM
from models.consulente import Consulente
from models.contatto import Contatto
from controllers.risorse_controller import RisorseController


class GestionePMDialog(QDialog):
    """Dialog per gestire i Project Manager"""
    
    def __init__(self, parent, risorse_controller: RisorseController):
        super().__init__(parent)
        self.risorse_controller = risorse_controller
        self.setWindowTitle("Gestione Project Manager")
        self.setMinimumSize(1000, 650)
        
        # Applica stile dalla finestra principale
        if hasattr(parent, 'styleSheet') and parent.styleSheet():
            self.setStyleSheet(parent.styleSheet())
        
        self.init_ui()
        self.carica_dati()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel("<h2 style='color: #1976D2;'>👤 Gestione Project Manager</h2>")
        layout.addWidget(titolo)
        layout.addSpacing(10)
        
        # Pulsanti azione
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_nuovo = QPushButton("➕ Nuovo")
        self.btn_modifica = QPushButton("✏️ Modifica")
        self.btn_elimina = QPushButton("🗑️ Elimina")
        
        self.btn_nuovo.setObjectName("btn_primary")
        self.btn_modifica.setObjectName("btn_secondary")
        self.btn_elimina.setObjectName("btn_danger")
        
        self.btn_nuovo.clicked.connect(self.nuovo_pm)
        self.btn_modifica.clicked.connect(self.modifica_pm)
        self.btn_elimina.clicked.connect(self.elimina_pm)
        
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addStretch()
        
        # Bottoni Import/Export
        self.btn_export_csv = QPushButton("📄 Export CSV")
        self.btn_export_excel = QPushButton("📊 Export Excel")
        self.btn_import = QPushButton("📥 Import")
        
        self.btn_export_csv.setObjectName("btn_action")
        self.btn_export_excel.setObjectName("btn_action")
        self.btn_import.setObjectName("btn_success")
        
        self.btn_export_csv.clicked.connect(self.export_csv)
        self.btn_export_excel.clicked.connect(self.export_excel)
        self.btn_import.clicked.connect(self.import_dati)
        
        btn_layout.addWidget(self.btn_export_csv)
        btn_layout.addWidget(self.btn_export_excel)
        btn_layout.addWidget(self.btn_import)
        
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        
        # Tabella PM
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefono", "Cellulare", "N° Clienti"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)        
        self.table.cellDoubleClicked.connect(self.gestisci_doppio_click)        
        layout.addWidget(self.table)
        
        # Pulsante chiudi
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.accept)
        layout.addWidget(btn_chiudi)
    
    def carica_dati(self):
        """Carica i PM nella tabella"""
        pms = self.risorse_controller.ottieni_tutti_pm()
        self.table.setRowCount(len(pms))
        
        for row, pm in enumerate(pms):
            num_clienti = self.risorse_controller.conta_clienti_pm(pm.id)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(pm.id)))
            self.table.setItem(row, 1, QTableWidgetItem(pm.nome))
            
            # Email cliccabile
            email_item = QTableWidgetItem(pm.email or "")
            if pm.email:
                email_item.setForeground(Qt.blue)
                email_item.setToolTip("Doppio click per inviare email")
            self.table.setItem(row, 2, email_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(pm.telefono or ""))
            self.table.setItem(row, 4, QTableWidgetItem(pm.cellulare or ""))
            self.table.setItem(row, 5, QTableWidgetItem(str(num_clienti)))
    
    def gestisci_doppio_click(self, row: int, col: int):
        """Gestisce il doppio click sulle celle"""
        if col == 2:  # Colonna email
            email = self.table.item(row, col).text()
            if email:
                QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
    
    def nuovo_pm(self):
        """Crea un nuovo PM"""
        dialog = PMDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.crea_pm(
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "PM creato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def modifica_pm(self):
        """Modifica il PM selezionato"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un PM da modificare")
            return
        
        pm_id = int(self.table.item(row, 0).text())
        pm = self.risorse_controller.ottieni_pm(pm_id)
        
        dialog = PMDialog(self, pm)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.modifica_pm(
                    pm_id,
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "PM modificato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_pm(self):
        """Elimina il PM selezionato"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un PM da eliminare")
            return
        
        pm_id = int(self.table.item(row, 0).text())
        pm_nome = self.table.item(row, 1).text()
        num_clienti = int(self.table.item(row, 5).text())
        
        if num_clienti > 0:
            risposta = QMessageBox.question(
                self, "Conferma Eliminazione",
                f"Il PM '{pm_nome}' ha {num_clienti} clienti associati.\n"
                f"Eliminandolo, i clienti rimarranno senza PM.\nContinuare?",
                QMessageBox.Yes | QMessageBox.No
            )
            if risposta != QMessageBox.Yes:
                return
        
        self.risorse_controller.elimina_pm(pm_id)
        self.carica_dati()
        QMessageBox.information(self, "Successo", "PM eliminato con successo!")
    
    def export_csv(self):
        """Esporta PM in formato CSV"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta PM CSV", "", "File CSV (*.csv)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            from models.database import DatabaseManager
            db = DatabaseManager()
            manager = ImportExportManager(db)
            successo, messaggio = manager.export_pm_to_csv(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def export_excel(self):
        """Esporta PM in formato Excel"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta PM Excel", "", "File Excel (*.xlsx)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            from models.database import DatabaseManager
            db = DatabaseManager()
            manager = ImportExportManager(db)
            successo, messaggio = manager.export_pm_to_excel(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def import_dati(self):
        """Importa PM da file CSV o Excel"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importa PM", "", "File CSV/Excel (*.csv *.xlsx *.xls)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self,
                "Conferma Import",
                "Sei sicuro di voler importare i PM?\n\nI duplicati verranno ignorati.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from utils.import_export import ImportExportManager
                from models.database import DatabaseManager
                db = DatabaseManager()
                manager = ImportExportManager(db)
                successo, messaggio, stats = manager.import_pm_from_file(file_path)
                
                if successo:
                    QMessageBox.information(self, "Import Completato", messaggio)
                    self.carica_dati()
                else:
                    QMessageBox.warning(self, "Errore Import", messaggio)


class PMDialog(QDialog):
    """Dialog per creare/modificare un PM"""
    
    def __init__(self, parent, pm: PM = None):
        super().__init__(parent)
        self.pm = pm
        self.setWindowTitle("Modifica PM" if pm else "Nuovo PM")
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.nome_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.cellulare_edit = QLineEdit()
        
        if self.pm:
            self.nome_edit.setText(self.pm.nome)
            self.email_edit.setText(self.pm.email or "")
            self.telefono_edit.setText(self.pm.telefono or "")
            self.cellulare_edit.setText(self.pm.cellulare or "")
        
        layout.addRow("Nome *:", self.nome_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Telefono:", self.telefono_edit)
        layout.addRow("Cellulare:", self.cellulare_edit)
        
        btn_layout = QHBoxLayout()
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)


# Continua con dialog analoghi per Consulenti...
class GestioneConsulentiDialog(QDialog):
    """Dialog per gestire i Consulenti"""
    
    def __init__(self, parent, risorse_controller: RisorseController):
        super().__init__(parent)
        self.risorse_controller = risorse_controller
        self.setWindowTitle("Gestione Consulenti")
        self.setMinimumSize(1100, 650)
        
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
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        self.btn_nuovo = QPushButton("➕ Nuovo")
        self.btn_modifica = QPushButton("✏️ Modifica")
        self.btn_elimina = QPushButton("🗑️ Elimina")
        
        self.btn_nuovo.setObjectName("btn_primary")
        self.btn_modifica.setObjectName("btn_secondary")
        self.btn_elimina.setObjectName("btn_danger")
        
        self.btn_nuovo.clicked.connect(self.nuovo_consulente)
        self.btn_modifica.clicked.connect(self.modifica_consulente)
        self.btn_elimina.clicked.connect(self.elimina_consulente)
        
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addStretch()
        
        # Bottoni Import/Export
        self.btn_export_csv = QPushButton("📄 Export CSV")
        self.btn_export_excel = QPushButton("📊 Export Excel")
        self.btn_import = QPushButton("📥 Import")
        
        self.btn_export_csv.setObjectName("btn_action")
        self.btn_export_excel.setObjectName("btn_action")
        self.btn_import.setObjectName("btn_success")
        
        self.btn_export_csv.clicked.connect(self.export_csv)
        self.btn_export_excel.clicked.connect(self.export_excel)
        self.btn_import.clicked.connect(self.import_dati)
        
        btn_layout.addWidget(self.btn_export_csv)
        btn_layout.addWidget(self.btn_export_excel)
        btn_layout.addWidget(self.btn_import)
        
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefono", 
                                              "Cellulare", "Competenza", "N° Clienti"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.gestisci_doppio_click)
        layout.addWidget(self.table)
        
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.accept)
        layout.addWidget(btn_chiudi)
    
    def carica_dati(self):
        consulenti = self.risorse_controller.ottieni_tutti_consulenti()
        self.table.setRowCount(len(consulenti))
        
        for row, consulente in enumerate(consulenti):
            num_clienti = self.risorse_controller.conta_clienti_consulente(consulente.id)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(consulente.id)))
            self.table.setItem(row, 1, QTableWidgetItem(consulente.nome))
            
            # Email cliccabile
            email_item = QTableWidgetItem(consulente.email or "")
            if consulente.email:
                email_item.setForeground(Qt.blue)
                email_item.setToolTip("Doppio click per inviare email")
            self.table.setItem(row, 2, email_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(consulente.telefono or ""))
            self.table.setItem(row, 4, QTableWidgetItem(consulente.cellulare or ""))
            self.table.setItem(row, 5, QTableWidgetItem(consulente.competenza or ""))
            self.table.setItem(row, 6, QTableWidgetItem(str(num_clienti)))
    
    def gestisci_doppio_click(self, row: int, col: int):
        """Gestisce il doppio click sulle celle"""
        if col == 2:  # Colonna email
            email = self.table.item(row, col).text()
            if email:
                QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
    
    def nuovo_consulente(self):
        dialog = ConsulenteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.crea_consulente(
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text(),
                    dialog.competenza_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Consulente creato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def modifica_consulente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un consulente da modificare")
            return
        
        consulente_id = int(self.table.item(row, 0).text())
        consulente = self.risorse_controller.ottieni_consulente(consulente_id)
        
        dialog = ConsulenteDialog(self, consulente)
        if dialog.exec_() == QDialog.Accepted:
            try:
                self.risorse_controller.modifica_consulente(
                    consulente_id,
                    dialog.nome_edit.text(),
                    dialog.email_edit.text(),
                    dialog.telefono_edit.text(),
                    dialog.cellulare_edit.text(),
                    dialog.competenza_edit.text()
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Consulente modificato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_consulente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un consulente da eliminare")
            return
        
        consulente_id = int(self.table.item(row, 0).text())
        consulente_nome = self.table.item(row, 1).text()
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare il consulente '{consulente_nome}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            self.risorse_controller.elimina_consulente(consulente_id)
            self.carica_dati()
            QMessageBox.information(self, "Successo", "Consulente eliminato con successo!")
    
    def export_csv(self):
        """Esporta Consulenti in formato CSV"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Consulenti CSV", "", "File CSV (*.csv)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            from models.database import DatabaseManager
            db = DatabaseManager()
            manager = ImportExportManager(db)
            successo, messaggio = manager.export_consulenti_to_csv(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def export_excel(self):
        """Esporta Consulenti in formato Excel"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Consulenti Excel", "", "File Excel (*.xlsx)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            from models.database import DatabaseManager
            db = DatabaseManager()
            manager = ImportExportManager(db)
            successo, messaggio = manager.export_consulenti_to_excel(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def import_dati(self):
        """Importa Consulenti da file CSV o Excel"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importa Consulenti", "", "File CSV/Excel (*.csv *.xlsx *.xls)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self,
                "Conferma Import",
                "Sei sicuro di voler importare i Consulenti?\n\nI duplicati verranno ignorati.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from utils.import_export import ImportExportManager
                from models.database import DatabaseManager
                db = DatabaseManager()
                manager = ImportExportManager(db)
                successo, messaggio, stats = manager.import_consulenti_from_file(file_path)
                
                if successo:
                    QMessageBox.information(self, "Import Completato", messaggio)
                    self.carica_dati()
                else:
                    QMessageBox.warning(self, "Errore Import", messaggio)


class ConsulenteDialog(QDialog):
    """Dialog per creare/modificare un Consulente"""
    
    def __init__(self, parent, consulente: Consulente = None):
        super().__init__(parent)
        self.consulente = consulente
        self.setWindowTitle("Modifica Consulente" if consulente else "Nuovo Consulente")
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.nome_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.cellulare_edit = QLineEdit()
        self.competenza_edit = QLineEdit()
        
        if self.consulente:
            self.nome_edit.setText(self.consulente.nome)
            self.email_edit.setText(self.consulente.email or "")
            self.telefono_edit.setText(self.consulente.telefono or "")
            self.cellulare_edit.setText(self.consulente.cellulare or "")
            self.competenza_edit.setText(self.consulente.competenza or "")
        
        layout.addRow("Nome *:", self.nome_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Telefono:", self.telefono_edit)
        layout.addRow("Cellulare:", self.cellulare_edit)
        layout.addRow("Competenza:", self.competenza_edit)
        
        btn_layout = QHBoxLayout()
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)
