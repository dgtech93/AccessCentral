"""
Dialog per gestione backup
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QSpinBox, QCheckBox, QGroupBox,
                             QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt
from datetime import datetime


class BackupDialog(QDialog):
    """Dialog per gestire i backup"""
    
    def __init__(self, parent, backup_manager):
        super().__init__(parent)
        self.backup_manager = backup_manager
        self.init_ui()
        self.carica_backups()
    
    def init_ui(self):
        """Inizializza l'interfaccia"""
        self.setWindowTitle("Gestione Backup")
        self.setModal(True)
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(self)
        
        # Titolo
        titolo = QLabel("<h2>💾 Gestione Backup</h2>")
        titolo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titolo)
        
        # Impostazioni backup
        settings_group = QGroupBox("Impostazioni Backup Automatici")
        settings_layout = QFormLayout()
        
        # Abilita backup automatici
        self.chk_abilita = QCheckBox("Abilita backup automatici")
        self.chk_abilita.setChecked(self.backup_manager.config["abilitato"])
        settings_layout.addRow("", self.chk_abilita)
        
        # Intervallo giorni
        intervallo_layout = QHBoxLayout()
        self.spin_intervallo = QSpinBox()
        self.spin_intervallo.setMinimum(1)
        self.spin_intervallo.setMaximum(365)
        self.spin_intervallo.setValue(self.backup_manager.config["intervallo_giorni"])
        self.spin_intervallo.setSuffix(" giorni")
        intervallo_layout.addWidget(self.spin_intervallo)
        intervallo_layout.addStretch()
        settings_layout.addRow("Frequenza backup:", intervallo_layout)
        
        # Max backup
        max_layout = QHBoxLayout()
        self.spin_max = QSpinBox()
        self.spin_max.setMinimum(1)
        self.spin_max.setMaximum(100)
        self.spin_max.setValue(self.backup_manager.config["max_backup"])
        self.spin_max.setSuffix(" backup")
        max_layout.addWidget(self.spin_max)
        max_layout.addStretch()
        settings_layout.addRow("Numero massimo:", max_layout)
        
        # Ultimo backup
        ultimo_backup = self.backup_manager.config.get("ultimo_backup")
        if ultimo_backup:
            try:
                data = datetime.fromisoformat(ultimo_backup)
                ultimo_txt = data.strftime("%d/%m/%Y %H:%M")
            except:
                ultimo_txt = "Mai"
        else:
            ultimo_txt = "Mai"
        
        lbl_ultimo = QLabel(f"<b>{ultimo_txt}</b>")
        settings_layout.addRow("Ultimo backup:", lbl_ultimo)
        
        # Pulsante salva impostazioni
        btn_salva_settings = QPushButton("💾 Salva Impostazioni")
        btn_salva_settings.setObjectName("btn_success")
        btn_salva_settings.clicked.connect(self.salva_impostazioni)
        settings_layout.addRow("", btn_salva_settings)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        layout.addSpacing(20)
        
        # Lista backup esistenti
        lbl_lista = QLabel("<h3>📋 Backup Disponibili</h3>")
        layout.addWidget(lbl_lista)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Data/Ora", "Dimensione", "Percorso"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        
        btn_crea = QPushButton("➕ Crea Backup")
        btn_crea.setObjectName("btn_primary")
        btn_crea.clicked.connect(self.crea_backup)
        
        btn_ripristina = QPushButton("↩️ Ripristina")
        btn_ripristina.setObjectName("btn_secondary")
        btn_ripristina.clicked.connect(self.ripristina_backup)
        
        btn_elimina = QPushButton("🗑️ Elimina")
        btn_elimina.setObjectName("btn_danger")
        btn_elimina.clicked.connect(self.elimina_backup)
        
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_crea)
        btn_layout.addWidget(btn_ripristina)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        
        layout.addLayout(btn_layout)
    
    def carica_backups(self):
        """Carica la lista dei backup nella tabella"""
        backups = self.backup_manager.ottieni_lista_backup()
        
        self.table.setRowCount(len(backups))
        
        for row, (path, data, size) in enumerate(backups):
            # Data/Ora
            data_item = QTableWidgetItem(data.strftime("%d/%m/%Y %H:%M:%S"))
            self.table.setItem(row, 0, data_item)
            
            # Dimensione
            size_str = self.backup_manager.formato_dimensione(size)
            size_item = QTableWidgetItem(size_str)
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, size_item)
            
            # Percorso
            path_item = QTableWidgetItem(path)
            path_item.setToolTip(path)
            self.table.setItem(row, 2, path_item)
    
    def salva_impostazioni(self):
        """Salva le impostazioni dei backup"""
        self.backup_manager.aggiorna_impostazioni(
            abilitato=self.chk_abilita.isChecked(),
            intervallo_giorni=self.spin_intervallo.value(),
            max_backup=self.spin_max.value()
        )
        
        QMessageBox.information(
            self, "Impostazioni Salvate",
            "Le impostazioni dei backup sono state aggiornate"
        )
    
    def crea_backup(self):
        """Crea un nuovo backup"""
        successo, path, messaggio = self.backup_manager.crea_backup()
        
        if successo:
            QMessageBox.information(self, "Backup Creato", messaggio)
            self.carica_backups()
        else:
            QMessageBox.warning(self, "Errore", messaggio)
    
    def ripristina_backup(self):
        """Ripristina il backup selezionato"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(
                self, "Attenzione",
                "Seleziona un backup da ripristinare"
            )
            return
        
        path = self.table.item(row, 2).text()
        data = self.table.item(row, 0).text()
        
        risposta = QMessageBox.warning(
            self, "⚠️ CONFERMA RIPRISTINO",
            f"Ripristinare il backup del {data}?\n\n"
            "ATTENZIONE: Tutti i dati correnti verranno sovrascritti!\n"
            "Un backup di sicurezza verrà creato automaticamente.\n\n"
            "L'applicazione si chiuderà dopo il ripristino.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if risposta != QMessageBox.Yes:
            return
        
        successo, messaggio = self.backup_manager.ripristina_backup(path)
        
        if successo:
            QMessageBox.information(self, "Ripristino Completato", messaggio)
            self.accept()
            # Chiudi l'applicazione
            self.parent().close()
        else:
            QMessageBox.critical(self, "Errore", messaggio)
    
    def elimina_backup(self):
        """Elimina il backup selezionato"""
        import os
        
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(
                self, "Attenzione",
                "Seleziona un backup da eliminare"
            )
            return
        
        path = self.table.item(row, 2).text()
        data = self.table.item(row, 0).text()
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Eliminare il backup del {data}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta != QMessageBox.Yes:
            return
        
        try:
            os.remove(path)
            QMessageBox.information(self, "Eliminato", "Backup eliminato con successo")
            self.carica_backups()
        except Exception as e:
            QMessageBox.critical(
                self, "Errore",
                f"Impossibile eliminare il backup:\n{str(e)}"
            )
