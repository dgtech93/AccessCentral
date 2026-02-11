"""
Dialog per gestire gli allegati dei clienti
"""

import os
import subprocess
import platform
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFileDialog, QInputDialog, QLabel)
from PyQt5.QtCore import Qt
from models.allegato import Allegato
from models.database import DatabaseManager


class AllegatiDialog(QDialog):
    """Dialog per gestire gli allegati di un cliente"""
    
    def __init__(self, parent, cliente_id, nome_cliente):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.nome_cliente = nome_cliente
        self.db = DatabaseManager()
        self.setWindowTitle(f"Allegati - {nome_cliente}")
        self.setMinimumSize(1000, 600)
        self.init_ui()
        self.carica_allegati()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        titolo = QLabel(f"<h2>📎 Allegati di {self.nome_cliente}</h2>")
        layout.addWidget(titolo)
        
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(self.info_label)
        
        # Tabella allegati
        self.tabella = QTableWidget()
        self.tabella.setColumnCount(6)
        self.tabella.setHorizontalHeaderLabels([
            "ID", "Tipo", "Nome File", "Dimensione", "Descrizione", "Data Upload"
        ])
        self.tabella.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabella.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabella.setSelectionMode(QTableWidget.SingleSelection)
        self.tabella.verticalHeader().setVisible(False)
        self.tabella.setColumnHidden(0, True)
        self.tabella.setColumnWidth(1, 80)
        self.tabella.setColumnWidth(3, 100)
        self.tabella.doubleClicked.connect(self.apri_allegato)
        layout.addWidget(self.tabella)
        
        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_carica = QPushButton("📤 Carica File")
        btn_carica.setObjectName("btn_success")
        btn_carica.clicked.connect(self.carica_file)
        
        btn_apri = QPushButton("👁️ Apri")
        btn_apri.setObjectName("btn_primary")
        btn_apri.clicked.connect(self.apri_allegato)
        
        btn_salva = QPushButton("💾 Salva Come...")
        btn_salva.setObjectName("btn_neutral")
        btn_salva.clicked.connect(self.salva_come)
        
        btn_modifica = QPushButton("✏️ Modifica Descrizione")
        btn_modifica.setObjectName("btn_neutral")
        btn_modifica.clicked.connect(self.modifica_descrizione)
        
        btn_elimina = QPushButton("🗑️ Elimina")
        btn_elimina.setObjectName("btn_danger")
        btn_elimina.clicked.connect(self.elimina_allegato)
        
        btn_chiudi = QPushButton("✅ Chiudi")
        btn_chiudi.setObjectName("btn_neutral")
        btn_chiudi.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_carica)
        btn_layout.addWidget(btn_apri)
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_chiudi)
        
        layout.addLayout(btn_layout)
    
    def carica_allegati(self):
        """Carica gli allegati del cliente nella tabella"""
        self.tabella.setRowCount(0)
        allegati = Allegato.get_by_cliente(self.db, self.cliente_id)
        
        dimensione_totale = 0
        for allegato in allegati:
            row = self.tabella.rowCount()
            self.tabella.insertRow(row)
            
            self.tabella.setItem(row, 0, QTableWidgetItem(str(allegato.id)))
            self.tabella.setItem(row, 1, QTableWidgetItem(allegato.get_icona()))
            self.tabella.setItem(row, 2, QTableWidgetItem(allegato.nome_file))
            self.tabella.setItem(row, 3, QTableWidgetItem(allegato.get_dimensione_formattata()))
            self.tabella.setItem(row, 4, QTableWidgetItem(allegato.descrizione or ""))
            self.tabella.setItem(row, 5, QTableWidgetItem(allegato.creato_il))
            
            dimensione_totale += allegato.dimensione_kb
        
        # Aggiorna info
        if allegati:
            dim_mb = dimensione_totale / 1024
            self.info_label.setText(
                f"{len(allegati)} file allegati - "
                f"Dimensione totale: {dim_mb:.2f} MB - "
                f"Limite per file: {Allegato.MAX_SIZE_MB} MB"
            )
        else:
            self.info_label.setText(f"Nessun allegato - Limite per file: {Allegato.MAX_SIZE_MB} MB")
    
    def carica_file(self):
        """Carica un nuovo file allegato"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File",
            "",
            "Tutti i file (*.*);;"
            "Documenti PDF (*.pdf);;"
            "Documenti Office (*.doc *.docx *.xls *.xlsx *.ppt *.pptx);;"
            "Immagini (*.jpg *.jpeg *.png *.gif *.bmp);;"
            "Archivi (*.zip *.rar *.7z)"
        )
        
        if not file_path:
            return
        
        # Controlla dimensione
        dimensione = os.path.getsize(file_path)
        if dimensione > Allegato.MAX_SIZE_MB * 1024 * 1024:
            QMessageBox.warning(
                self,
                "File Troppo Grande",
                f"Il file supera il limite di {Allegato.MAX_SIZE_MB} MB.\n"
                f"Dimensione attuale: {dimensione / (1024 * 1024):.2f} MB"
            )
            return
        
        # Chiedi descrizione
        descrizione, ok = QInputDialog.getText(
            self,
            "Descrizione",
            "Inserisci una descrizione per l'allegato (opzionale):",
            text=os.path.splitext(os.path.basename(file_path))[0]
        )
        
        if not ok:
            return
        
        try:
            Allegato.crea_allegato(
                self.db,
                self.cliente_id,
                file_path,
                descrizione if descrizione else None
            )
            self.carica_allegati()
            QMessageBox.information(self, "Successo", "File caricato con successo!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore caricamento file:\n{e}")
    
    def apri_allegato(self):
        """Apre l'allegato selezionato con l'applicazione predefinita"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un allegato da aprire")
            return
        
        allegato_id = int(self.tabella.item(row, 0).text())
        allegato = Allegato.get_by_id(self.db, allegato_id)
        
        if not allegato:
            QMessageBox.critical(self, "Errore", "Allegato non trovato")
            self.carica_allegati()
            return
        
        # Verifica esistenza file
        if not os.path.exists(allegato.percorso_file):
            QMessageBox.critical(
                self,
                "Errore",
                f"File non trovato:\n{allegato.percorso_file}"
            )
            return
        
        # Apri con applicazione predefinita
        try:
            if platform.system() == 'Windows':
                os.startfile(allegato.percorso_file)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', allegato.percorso_file])
            else:  # Linux
                subprocess.run(['xdg-open', allegato.percorso_file])
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile aprire il file:\n{e}")
    
    def salva_come(self):
        """Salva una copia dell'allegato in una posizione scelta dall'utente"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un allegato da salvare")
            return
        
        allegato_id = int(self.tabella.item(row, 0).text())
        allegato = Allegato.get_by_id(self.db, allegato_id)
        
        if not allegato:
            QMessageBox.critical(self, "Errore", "Allegato non trovato")
            self.carica_allegati()
            return
        
        # Verifica esistenza file
        if not os.path.exists(allegato.percorso_file):
            QMessageBox.critical(
                self,
                "Errore",
                f"File non trovato:\n{allegato.percorso_file}"
            )
            return
        
        # Chiedi dove salvare
        ext = os.path.splitext(allegato.nome_file)[1]
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Come",
            allegato.nome_file,
            f"File {ext.upper()} (*{ext});;Tutti i file (*.*)"
        )
        
        if not save_path:
            return
        
        try:
            import shutil
            shutil.copy2(allegato.percorso_file, save_path)
            QMessageBox.information(self, "Successo", "File salvato con successo!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore salvataggio file:\n{e}")
    
    def modifica_descrizione(self):
        """Modifica la descrizione dell'allegato selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un allegato da modificare")
            return
        
        allegato_id = int(self.tabella.item(row, 0).text())
        allegato = Allegato.get_by_id(self.db, allegato_id)
        
        if not allegato:
            QMessageBox.critical(self, "Errore", "Allegato non trovato")
            self.carica_allegati()
            return
        
        nuova_descrizione, ok = QInputDialog.getText(
            self,
            "Modifica Descrizione",
            "Inserisci la nuova descrizione:",
            text=allegato.descrizione or ""
        )
        
        if ok:
            try:
                Allegato.update_descrizione(self.db, allegato_id, nuova_descrizione if nuova_descrizione else None)
                self.carica_allegati()
                QMessageBox.information(self, "Successo", "Descrizione modificata con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore modifica descrizione:\n{e}")
    
    def elimina_allegato(self):
        """Elimina l'allegato selezionato"""
        row = self.tabella.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un allegato da eliminare")
            return
        
        allegato_id = int(self.tabella.item(row, 0).text())
        nome_file = self.tabella.item(row, 2).text()
        
        risposta = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Vuoi eliminare l'allegato '{nome_file}'?\n\n"
            "Il file verrà eliminato definitivamente dal disco.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            try:
                if Allegato.delete(self.db, allegato_id):
                    self.carica_allegati()
                    QMessageBox.information(self, "Successo", "Allegato eliminato con successo!")
                else:
                    QMessageBox.critical(self, "Errore", "Allegato non trovato")
                    self.carica_allegati()
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore eliminazione allegato:\n{e}")
