"""
Finestra principale dell'applicazione
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTreeWidget, QTreeWidgetItem, QPushButton, QLabel,
                             QMessageBox, QInputDialog, QDialog, QFormLayout,
                             QLineEdit, QTextEdit, QComboBox, QSpinBox,
                             QFileDialog, QMenu, QAction, QSplitter, QTabWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMenuBar,
                             QTextBrowser, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from models.database import DatabaseManager
from models.cliente import Cliente
from models.servizio import Servizio
from models.credenziale import Credenziale
from models.pm import PM
from models.consulente import Consulente
from models.contatto import Contatto
from controllers.cliente_controller import ClienteController
from controllers.credenziale_controller import CredenzialeController
from controllers.risorse_controller import RisorseController
from utils.vpn_launcher import VPNLauncher
from utils.rdp_launcher import RDPLauncher


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.cliente_controller = ClienteController(self.db)
        self.credenziale_controller = CredenzialeController(self.db)
        self.risorse_controller = RisorseController(self.db)
        self.vpn_launcher = VPNLauncher()
        self.rdp_launcher = RDPLauncher()
        
        self.init_ui()
        self.carica_dati()
    
    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        self.setWindowTitle("AccessCentral - Gestione Accessi")
        self.setGeometry(100, 100, 1400, 800)
        
        # Applica stylesheet globale
        self.applica_stile()
        
        # Crea menu bar
        self.crea_menu_bar()
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter per ridimensionare le sezioni
        splitter = QSplitter(Qt.Horizontal)
        
        # === PANNELLO SINISTRO: Lista Clienti ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        # Titolo e pulsanti clienti
        titolo_clienti = QLabel("<h2 style='color: #1976D2; margin: 0;'>📋 Clienti</h2>")
        left_layout.addWidget(titolo_clienti)
        left_layout.addSpacing(10)
        
        btn_layout_clienti = QHBoxLayout()
        btn_layout_clienti.setSpacing(8)
        self.btn_nuovo_cliente = QPushButton("➕ Nuovo")
        self.btn_modifica_cliente = QPushButton("✏️ Modifica")
        self.btn_elimina_cliente = QPushButton("🗑️ Elimina")
        
        self.btn_nuovo_cliente.setObjectName("btn_primary")
        self.btn_modifica_cliente.setObjectName("btn_secondary")
        self.btn_elimina_cliente.setObjectName("btn_danger")
        
        self.btn_nuovo_cliente.clicked.connect(self.nuovo_cliente)
        self.btn_modifica_cliente.clicked.connect(self.modifica_cliente)
        self.btn_elimina_cliente.clicked.connect(self.elimina_cliente)
        
        btn_layout_clienti.addWidget(self.btn_nuovo_cliente)
        btn_layout_clienti.addWidget(self.btn_modifica_cliente)
        btn_layout_clienti.addWidget(self.btn_elimina_cliente)
        left_layout.addLayout(btn_layout_clienti)
        left_layout.addSpacing(10)
        
        # Tree widget clienti
        self.tree_clienti = QTreeWidget()
        self.tree_clienti.setHeaderLabels(["Clienti e Servizi"])
        self.tree_clienti.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_clienti.customContextMenuRequested.connect(self.mostra_menu_contestuale)
        self.tree_clienti.itemClicked.connect(self.cliente_selezionato)
        left_layout.addWidget(self.tree_clienti)
        
        splitter.addWidget(left_panel)
        
        # === PANNELLO DESTRO: Dettagli e Credenziali ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        # Informazioni cliente/servizio con stile e VPN cards
        from PyQt5.QtWidgets import QFrame
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        # Layout orizzontale: Info a sinistra, VPN a destra
        main_info_layout = QHBoxLayout()
        
        # Informazioni cliente/servizio
        self.lbl_info = QLabel("<h3 style='color: #757575;'>Seleziona un cliente o servizio</h3>")
        self.lbl_info.setWordWrap(True)
        main_info_layout.addWidget(self.lbl_info, 1)
        
        main_info_layout.addSpacing(15)
        
        # Container VPN compatto a destra
        vpn_container = QFrame()
        vpn_container.setMaximumWidth(180)
        vpn_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E1F5FE, stop:0.5 #E1F5FE, stop:0.5 #E8F5E9, stop:1 #E8F5E9);
                border: 2px solid #1976D2;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        vpn_layout = QVBoxLayout(vpn_container)
        vpn_layout.setSpacing(3)
        vpn_layout.setContentsMargins(5, 5, 5, 5)
        
        # Titolo VPN
        vpn_title = QLabel("<b style='color: #1976D2;'>🔌 VPN</b>")
        vpn_title.setAlignment(Qt.AlignCenter)
        vpn_layout.addWidget(vpn_title)
        
        # Separatore
        sep_line = QFrame()
        sep_line.setFrameShape(QFrame.HLine)
        sep_line.setStyleSheet("background-color: #1976D2; max-height: 1px;")
        vpn_layout.addWidget(sep_line)
        
        # Bottone VPN EXE
        self.btn_vpn_exe = QPushButton("💻 VPN EXE")
        self.btn_vpn_exe.setObjectName("btn_action")
        self.btn_vpn_exe.setMaximumHeight(32)
        self.btn_vpn_exe.clicked.connect(self.lancia_vpn_exe)
        self.btn_vpn_exe.setEnabled(False)
        vpn_layout.addWidget(self.btn_vpn_exe)
        
        # Bottone VPN Windows
        self.btn_vpn_windows = QPushButton("🪟 VPN Win")
        self.btn_vpn_windows.setObjectName("btn_action")
        self.btn_vpn_windows.setMaximumHeight(32)
        self.btn_vpn_windows.clicked.connect(self.lancia_vpn_windows)
        self.btn_vpn_windows.setEnabled(False)
        vpn_layout.addWidget(self.btn_vpn_windows)
        
        main_info_layout.addWidget(vpn_container)
        
        info_layout.addLayout(main_info_layout)
        right_layout.addWidget(info_frame)
        right_layout.addSpacing(15)
        
        # Pulsante per aprire link (solo per servizi CRM/Web)
        self.btn_apri_link = QPushButton("🌐 Apri Link nel Browser")
        self.btn_apri_link.setObjectName("btn_action")
        self.btn_apri_link.clicked.connect(self.apri_link_servizio)
        self.btn_apri_link.setEnabled(False)
        self.btn_apri_link.setVisible(False)  # Nascosto di default
        right_layout.addWidget(self.btn_apri_link)
        
        # Sezione Risorse Cliente
        risorse_label = QLabel("<b style='color: #1976D2;'>👥 Risorse Cliente</b>")
        right_layout.addWidget(risorse_label)
        right_layout.addSpacing(5)
        
        risorse_layout = QHBoxLayout()
        risorse_layout.setSpacing(8)
        self.btn_info_pm = QPushButton("👤 Project Manager")
        self.btn_info_consulenti = QPushButton("👥 Consulenti")
        self.btn_gestisci_contatti = QPushButton("📇 Rubrica")
        
        self.btn_info_pm.setObjectName("btn_neutral")
        self.btn_info_consulenti.setObjectName("btn_neutral")
        self.btn_gestisci_contatti.setObjectName("btn_neutral")
        
        self.btn_info_pm.clicked.connect(self.mostra_info_pm_cliente)
        self.btn_info_consulenti.clicked.connect(self.mostra_info_consulenti_cliente)
        self.btn_gestisci_contatti.clicked.connect(self.gestisci_contatti_cliente)
        
        self.btn_info_pm.setEnabled(False)
        self.btn_info_consulenti.setEnabled(False)
        self.btn_gestisci_contatti.setEnabled(False)
        
        risorse_layout.addWidget(self.btn_info_pm)
        risorse_layout.addWidget(self.btn_info_consulenti)
        risorse_layout.addWidget(self.btn_gestisci_contatti)
        right_layout.addLayout(risorse_layout)
        right_layout.addSpacing(15)
        
        # Sezione Credenziali
        cred_label = QLabel("<b style='color: #1976D2;'>🔐 Credenziali</b>")
        right_layout.addWidget(cred_label)
        right_layout.addSpacing(5)
        
        # Tree widget credenziali con colonna azione
        self.tree_credenziali = QTreeWidget()
        self.tree_credenziali.setHeaderLabels(["Username", "Host", "Porta", "Password", "Note", "Azione"])
        self.tree_credenziali.setColumnWidth(0, 150)
        self.tree_credenziali.setColumnWidth(1, 120)
        self.tree_credenziali.setColumnWidth(2, 60)
        self.tree_credenziali.setColumnWidth(3, 120)
        self.tree_credenziali.setColumnWidth(4, 150)
        self.tree_credenziali.setColumnWidth(5, 120)
        self.tree_credenziali.setUniformRowHeights(False)
        self.tree_credenziali.setStyleSheet(self.tree_credenziali.styleSheet() + """
            QTreeWidget::item {
                height: 40px;
                padding: 5px 2px;
            }
        """)
        self.tree_credenziali.itemClicked.connect(self.credenziale_selezionata)
        self.tree_credenziali.itemDoubleClicked.connect(self.copia_password)
        right_layout.addWidget(self.tree_credenziali)
        
        # Info e pulsanti in basso
        bottom_layout = QHBoxLayout()
        
        # Info password a sinistra
        info_pwd_label = QLabel("<i style='color: #757575;'>💡 Doppio click su un campo per copiarlo</i>")
        bottom_layout.addWidget(info_pwd_label)
        bottom_layout.addStretch()
        
        # Pulsanti gestione credenziali a destra
        self.btn_nuova_credenziale = QPushButton("➕ Nuova")
        self.btn_duplica_credenziale = QPushButton("📋 Duplica")
        self.btn_modifica_credenziale = QPushButton("✏️ Modifica")
        self.btn_elimina_credenziale = QPushButton("🗑️ Elimina")
        
        self.btn_nuova_credenziale.setObjectName("btn_primary")
        self.btn_duplica_credenziale.setObjectName("btn_action")
        self.btn_modifica_credenziale.setObjectName("btn_secondary")
        self.btn_elimina_credenziale.setObjectName("btn_danger")
        
        self.btn_nuova_credenziale.clicked.connect(self.nuova_credenziale)
        self.btn_duplica_credenziale.clicked.connect(self.duplica_credenziale)
        self.btn_modifica_credenziale.clicked.connect(self.modifica_credenziale)
        self.btn_elimina_credenziale.clicked.connect(self.elimina_credenziale)
        
        self.btn_nuova_credenziale.setEnabled(False)
        self.btn_duplica_credenziale.setEnabled(False)
        self.btn_modifica_credenziale.setEnabled(False)
        self.btn_elimina_credenziale.setEnabled(False)
        
        bottom_layout.addWidget(self.btn_nuova_credenziale)
        bottom_layout.addWidget(self.btn_duplica_credenziale)
        bottom_layout.addWidget(self.btn_modifica_credenziale)
        bottom_layout.addWidget(self.btn_elimina_credenziale)
        
        right_layout.addSpacing(10)
        right_layout.addLayout(bottom_layout)
        
        splitter.addWidget(right_panel)
        
        # Imposta proporzioni splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # Variabili di stato
        self.cliente_corrente = None
        self.servizio_corrente = None
        self.credenziale_corrente = None
    
    def applica_stile(self):
        """Applica lo stile CSS all'applicazione"""
        self.setStyleSheet("""
            /* Stile generale */
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            /* Etichette e titoli */
            QLabel {
                color: #212121;
            }
            
            /* Tree Widget */
            QTreeWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 5px;
                font-size: 11pt;
            }
            
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f5f5f5;
            }
            
            QTreeWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            
            QTreeWidget::item:hover {
                background-color: #BBDEFB;
            }
            
            QTreeWidget::item:selected:hover {
                background-color: #1976D2;
            }
            
            /* Bottoni base */
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
                min-height: 32px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            QPushButton:pressed {
                padding-top: 10px;
            }
            
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
            
            /* Bottoni primari (Nuovo/Aggiungi) - Blu */
            QPushButton#btn_primary {
                background-color: #2196F3;
                color: white;
            }
            
            QPushButton#btn_primary:hover {
                background-color: #1976D2;
            }
            
            /* Bottoni successo (Salva/Conferma) - Verde */
            QPushButton#btn_success {
                background-color: #4CAF50;
                color: white;
            }
            
            QPushButton#btn_success:hover {
                background-color: #45a049;
            }
            
            /* Bottoni pericolo (Elimina) - Rosso */
            QPushButton#btn_danger {
                background-color: #f44336;
                color: white;
            }
            
            QPushButton#btn_danger:hover {
                background-color: #da190b;
            }
            
            /* Bottoni secondari (Modifica/Info) - Arancione */
            QPushButton#btn_secondary {
                background-color: #FF9800;
                color: white;
            }
            
            QPushButton#btn_secondary:hover {
                background-color: #FB8C00;
            }
            
            /* Bottoni azione speciale (RDP/VPN) - Verde Teal */
            QPushButton#btn_action {
                background-color: #009688;
                color: white;
            }
            
            QPushButton#btn_action:hover {
                background-color: #00796B;
            }
            
            /* Bottoni neutri - Grigio */
            QPushButton#btn_neutral {
                background-color: #757575;
                color: white;
            }
            
            QPushButton#btn_neutral:hover {
                background-color: #616161;
            }
            
            /* Input fields */
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                font-size: 10pt;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #2196F3;
            }
            
            /* ComboBox specifico */
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #757575;
                width: 0;
                height: 0;
            }
            
            /* Checkbox */
            QCheckBox {
                spacing: 8px;
                font-size: 10pt;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #2196F3;
                border-radius: 3px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                image: none;
            }
            
            /* GroupBox */
            QGroupBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                background-color: white;
            }
            
            QGroupBox::title {
                color: #2196F3;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background-color: #f5f5f5;
            }
            
            /* Splitter */
            QSplitter::handle {
                background-color: #e0e0e0;
                width: 2px;
            }
            
            QSplitter::handle:hover {
                background-color: #2196F3;
            }
            
            /* Menu Bar */
            QMenuBar {
                background-color: #1976D2;
                color: white;
                padding: 4px;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #1565C0;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
            }
            
            QMenu::item {
                padding: 8px 24px;
            }
            
            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
    
    def crea_menu_bar(self):
        """Crea la barra dei menu"""
        menubar = self.menuBar()
        
        # Menu File
        menu_file = menubar.addMenu("File")
        
        azione_export_csv = QAction("📤 Esporta CSV...", self)
        azione_export_csv.triggered.connect(self.esporta_csv)
        menu_file.addAction(azione_export_csv)
        
        azione_export_excel = QAction("📊 Esporta Excel...", self)
        azione_export_excel.triggered.connect(self.esporta_excel)
        menu_file.addAction(azione_export_excel)
        
        menu_file.addSeparator()
        
        azione_import = QAction("📥 Importa Dati...", self)
        azione_import.triggered.connect(self.importa_dati)
        menu_file.addAction(azione_import)
        
        # Menu Risorse
        menu_risorse = menubar.addMenu("Risorse")
        
        azione_pm = QAction("Gestione PM", self)
        azione_pm.triggered.connect(self.apri_gestione_pm)
        menu_risorse.addAction(azione_pm)
        
        azione_consulenti = QAction("Gestione Consulenti", self)
        azione_consulenti.triggered.connect(self.apri_gestione_consulenti)
        menu_risorse.addAction(azione_consulenti)
        
        # Menu Info
        menu_info = menubar.addMenu("Info")
        azione_about = QAction("Informazioni", self)
        azione_about.triggered.connect(self.mostra_info)
        menu_info.addAction(azione_about)
    
    def mostra_dialog_con_link(self, titolo: str, contenuto_html: str):
        """Mostra un dialog con contenuto HTML e link cliccabili"""
        dialog = QDialog(self)
        dialog.setWindowTitle(titolo)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        text_browser = QTextBrowser()
        text_browser.setHtml(contenuto_html)
        text_browser.setOpenExternalLinks(True)
        text_browser.setMinimumHeight(300)
        
        layout.addWidget(text_browser)
        
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(dialog.accept)
        layout.addWidget(btn_chiudi)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def apri_gestione_pm(self):
        """Apre il dialog per gestire i PM"""
        from views.risorse_dialogs import GestionePMDialog
        dialog = GestionePMDialog(self, self.risorse_controller)
        dialog.exec_()
    
    def apri_gestione_consulenti(self):
        """Apre il dialog per gestire i Consulenti"""
        from views.risorse_dialogs import GestioneConsulentiDialog
        dialog = GestioneConsulentiDialog(self, self.risorse_controller)
        dialog.exec_()
    
    def gestisci_consulenti_cliente(self, cliente_id: int):
        """Apre il dialog per gestire i consulenti di un cliente specifico"""
        cliente = self.cliente_controller.ottieni_cliente(cliente_id)
        if not cliente:
            return
        
        from views.cliente_dialogs import GestioneConsulentiClienteDialog
        dialog = GestioneConsulentiClienteDialog(self, cliente_id, cliente.nome, 
                                                 self.risorse_controller)
        dialog.exec_()
    
    def apri_rubrica_contatti(self, cliente_id: int):
        """Apre la rubrica contatti di un cliente"""
        cliente = self.cliente_controller.ottieni_cliente(cliente_id)
        if not cliente:
            return
        
        from views.cliente_dialogs import GestioneContattiDialog
        dialog = GestioneContattiDialog(self, cliente_id, cliente.nome, 
                                       self.risorse_controller)
        dialog.exec_()
    
    def mostra_info_pm_cliente(self):
        """Mostra le informazioni del PM del cliente corrente"""
        if not self.cliente_corrente or not self.cliente_corrente.pm_id:
            QMessageBox.information(self, "Info", "Nessun PM associato a questo cliente")
            return
        
        pm = self.risorse_controller.ottieni_pm(self.cliente_corrente.pm_id)
        if not pm:
            QMessageBox.warning(self, "Errore", "PM non trovato")
            return
        
        info = f"<h3>👤 Project Manager</h3>"
        info += f"<p><b>Nome:</b> {pm.nome}</p>"
        if pm.email:
            info += f"<p><b>Email:</b> <a href='mailto:{pm.email}'>{pm.email}</a></p>"
        if pm.telefono:
            info += f"<p><b>Telefono:</b> {pm.telefono}</p>"
        if pm.cellulare:
            info += f"<p><b>Cellulare:</b> {pm.cellulare}</p>"
        
        num_clienti = self.risorse_controller.conta_clienti_pm(pm.id)
        info += f"<p><b>Clienti gestiti:</b> {num_clienti}</p>"
        
        self.mostra_dialog_con_link("Info PM", info)
    
    def mostra_info_consulenti_cliente(self):
        """Mostra le informazioni dei consulenti del cliente corrente"""
        if not self.cliente_corrente:
            return
        
        consulenti = self.risorse_controller.ottieni_consulenti_cliente(self.cliente_corrente.id)
        
        if not consulenti:
            QMessageBox.information(self, "Info", "Nessun consulente associato a questo cliente")
            return
        
        info = f"<h3>👥 Consulenti di {self.cliente_corrente.nome}</h3>"
        info += f"<p><b>Totale consulenti:</b> {len(consulenti)}</p><hr>"
        
        for consulente in consulenti:
            info += f"<p><b>{consulente.nome}</b>"
            if consulente.competenza:
                info += f" - <i>{consulente.competenza}</i>"
            info += "<br>"
            if consulente.email:
                info += f"📧 <a href='mailto:{consulente.email}'>{consulente.email}</a><br>"
            if consulente.telefono:
                info += f"☎️ {consulente.telefono}<br>"
            if consulente.cellulare:
                info += f"📱 {consulente.cellulare}<br>"
            info += "</p>"
        
        self.mostra_dialog_con_link("Info Consulenti", info)
    
    def gestisci_contatti_cliente(self):
        """Apre la gestione contatti del cliente corrente"""
        if not self.cliente_corrente:
            return
        
        self.apri_rubrica_contatti(self.cliente_corrente.id)
        
        # Aggiorna le info dopo la chiusura del dialog
        self.mostra_info_cliente()
    
    def mostra_info(self):
        """Mostra informazioni sull'applicazione"""
        QMessageBox.information(
            self, "AccessCentral",
            "<h3>AccessCentral v1.3.1</h3>"
            "<p>Gestione completa di credenziali, servizi e risorse.</p>"
            "<p><b>Funzionalità:</b></p>"
            "<ul>"
            "<li>Gestione Clienti con PM e Consulenti</li>"
            "<li>Rubrica Contatti per ogni cliente</li>"
            "<li>Servizi e Credenziali organizzati</li>"
            "<li>Integrazione VPN e RDP</li>"
            "<li>Import/Export CSV e Excel</li>"
            "</ul>"
        )
    
    def esporta_csv(self):
        """Esporta tutti i dati in formato CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta CSV", "", "File CSV (*.csv)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            manager = ImportExportManager(self.db)
            successo, messaggio = manager.export_to_csv(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def esporta_excel(self):
        """Esporta tutti i dati in formato Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Excel", "", "File Excel (*.xlsx)"
        )
        
        if file_path:
            from utils.import_export import ImportExportManager
            manager = ImportExportManager(self.db)
            successo, messaggio = manager.export_to_excel(file_path)
            
            if successo:
                QMessageBox.information(self, "Export Completato", messaggio)
            else:
                QMessageBox.warning(self, "Errore Export", messaggio)
    
    def importa_dati(self):
        """Importa dati da file CSV o Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importa Dati", "", "File CSV/Excel (*.csv *.xlsx *.xls)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self, 
                "Conferma Import",
                "Sei sicuro di voler importare i dati?\n\n"
                "Verranno creati nuovi clienti, servizi e credenziali.\n"
                "Gli elementi esistenti non verranno modificati.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from utils.import_export import ImportExportManager
                manager = ImportExportManager(self.db)
                successo, messaggio, stats = manager.import_from_file(file_path)
                
                if successo:
                    QMessageBox.information(self, "Import Completato", messaggio)
                    self.carica_dati()  # Ricarica i dati per mostrare le nuove entità
                else:
                    QMessageBox.warning(self, "Errore Import", messaggio)
    
    def carica_dati(self):
        """Carica i dati nel tree widget"""
        self.tree_clienti.clear()
        clienti = self.cliente_controller.ottieni_tutti_clienti()
        
        for cliente in clienti:
            item_cliente = QTreeWidgetItem(self.tree_clienti)
            item_cliente.setText(0, f"👤 {cliente.nome}")
            item_cliente.setData(0, Qt.UserRole, {'tipo': 'cliente', 'id': cliente.id})
            
            # Aggiungi servizi
            servizi = self.cliente_controller.ottieni_servizi_cliente(cliente.id)
            for servizio in servizi:
                item_servizio = QTreeWidgetItem(item_cliente)
                icona = self.get_icona_servizio(servizio.tipo)
                item_servizio.setText(0, f"{icona} {servizio.nome} ({servizio.tipo})")
                item_servizio.setData(0, Qt.UserRole, {
                    'tipo': 'servizio',
                    'id': servizio.id,
                    'cliente_id': cliente.id
                })
        
        self.tree_clienti.expandAll()
    
    def get_icona_servizio(self, tipo: str) -> str:
        """Restituisce l'icona per il tipo di servizio"""
        icone = {
            'RDP': '🖥️',
            'CRM': '📊',
            'Web': '🌐',
            'Database': '💾',
            'SSH': '⌨️',
            'FTP': '📁',
            'Altro': '🔧'
        }
        return icone.get(tipo, '🔧')
    
    def cliente_selezionato(self, item, column):
        """Gestisce la selezione di un elemento nel tree"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        if data['tipo'] == 'cliente':
            self.cliente_corrente = self.cliente_controller.ottieni_cliente(data['id'])
            self.servizio_corrente = None
            self.mostra_info_cliente()
            self.tree_credenziali.clear()
            self.btn_nuova_credenziale.setEnabled(False)
            self.btn_duplica_credenziale.setEnabled(False)
            
            # Abilita pulsanti risorse (sempre abilitati quando c'è un cliente)
            self.btn_info_pm.setEnabled(True)  # Sempre abilitato per gestire PM
            self.btn_info_consulenti.setEnabled(True)  # Sempre abilitato per gestire consulenti
            self.btn_gestisci_contatti.setEnabled(True)
        
        elif data['tipo'] == 'servizio':
            self.cliente_corrente = self.cliente_controller.ottieni_cliente(data['cliente_id'])
            self.servizio_corrente = self.credenziale_controller.ottieni_servizio(data['id'])
            self.mostra_info_servizio()
            self.carica_credenziali()
            self.btn_nuova_credenziale.setEnabled(True)
            self.btn_duplica_credenziale.setEnabled(False)
            
            # Abilita pulsanti risorse anche quando si seleziona un servizio
            self.btn_info_pm.setEnabled(True)
            self.btn_info_consulenti.setEnabled(True)
            self.btn_gestisci_contatti.setEnabled(True)
    
    def mostra_info_cliente(self):
        """Mostra le informazioni del cliente selezionato"""
        if not self.cliente_corrente:
            return
        
        info = f"<h3>Cliente: {self.cliente_corrente.nome}</h3>"
        if self.cliente_corrente.descrizione:
            info += f"<p><b>Descrizione:</b> {self.cliente_corrente.descrizione}</p>"
        
        # PM di riferimento
        if self.cliente_corrente.pm_id:
            pm = self.risorse_controller.ottieni_pm(self.cliente_corrente.pm_id)
            if pm:
                info += f"<p><b>PM:</b> 👤 {pm.nome}</p>"
        
        # Consulenti
        consulenti = self.risorse_controller.ottieni_consulenti_cliente(self.cliente_corrente.id)
        if consulenti:
            info += f"<p><b>Consulenti ({len(consulenti)}):</b> "
            info += ", ".join([f"👥 {c.nome}" for c in consulenti[:3]])
            if len(consulenti) > 3:
                info += f" +{len(consulenti)-3} altri"
            info += "</p>"
        
        # Contatti
        contatti = self.risorse_controller.ottieni_contatti_cliente(self.cliente_corrente.id)
        if contatti:
            info += f"<p><b>Contatti in rubrica:</b> {len(contatti)}</p>"
        
        num_servizi = self.cliente_controller.conta_servizi_cliente(self.cliente_corrente.id)
        info += f"<p><b>Numero servizi:</b> {num_servizi}</p>"
        
        # Gestione VPN
        has_vpn_exe = bool(self.cliente_corrente.vpn_exe_path)
        has_vpn_win = bool(self.cliente_corrente.vpn_windows_name)
        
        if has_vpn_exe:
            info += f"<p><b>VPN EXE:</b> {self.cliente_corrente.vpn_exe_path}</p>"
        if has_vpn_win:
            info += f"<p><b>VPN Windows:</b> {self.cliente_corrente.vpn_windows_name}</p>"
        
        self.lbl_info.setText(info)
        self.btn_vpn_exe.setEnabled(has_vpn_exe)
        self.btn_vpn_windows.setEnabled(has_vpn_win)
    
    def mostra_info_servizio(self):
        """Mostra le informazioni del servizio selezionato"""
        if not self.servizio_corrente or not self.cliente_corrente:
            return
        
        info = f"<h3>Cliente: {self.cliente_corrente.nome}</h3>"
        info += f"<p><b>Servizio:</b> {self.servizio_corrente.nome}</p>"
        info += f"<p><b>Tipo:</b> {self.servizio_corrente.tipo}</p>"
        
        if self.servizio_corrente.descrizione:
            info += f"<p><b>Descrizione:</b> {self.servizio_corrente.descrizione}</p>"
        
        # Mostra link se presente
        if self.servizio_corrente.link and self.servizio_corrente.tipo in ["CRM", "Web"]:
            info += f"<p><b>Link:</b> <a href='{self.servizio_corrente.link}'>{self.servizio_corrente.link}</a></p>"
        
        num_cred = self.credenziale_controller.conta_credenziali_servizio(self.servizio_corrente.id)
        info += f"<p><b>Credenziali disponibili:</b> {num_cred}</p>"
        
        self.lbl_info.setText(info)
        self.lbl_info.setOpenExternalLinks(True)  # Abilita i link cliccabili
        
        # Gestione VPN
        has_vpn_exe = bool(self.cliente_corrente.vpn_exe_path)
        has_vpn_win = bool(self.cliente_corrente.vpn_windows_name)
        self.btn_vpn_exe.setEnabled(has_vpn_exe)
        self.btn_vpn_windows.setEnabled(has_vpn_win)
        
        # Gestione bottone link
        mostra_link = (self.servizio_corrente.tipo in ["CRM", "Web"] and 
                      bool(self.servizio_corrente.link))
        self.btn_apri_link.setVisible(mostra_link)
        self.btn_apri_link.setEnabled(mostra_link)
    
    def carica_credenziali(self):
        """Carica le credenziali del servizio selezionato"""
        self.tree_credenziali.clear()
        
        if not self.servizio_corrente:
            return
        
        credenziali = self.credenziale_controller.ottieni_credenziali_servizio(
            self.servizio_corrente.id
        )
        
        for cred in credenziali:
            item = QTreeWidgetItem(self.tree_credenziali)
            item.setText(0, cred.username)
            item.setText(1, cred.host or "")
            item.setText(2, str(cred.porta) if cred.porta else "")
            item.setText(3, cred.password)  # Mostra password visibile
            item.setText(4, cred.note or "")
            item.setData(0, Qt.UserRole, cred.id)
            
            # Aggiungi bottone RDP nella colonna Azione se servizio è RDP
            if self.servizio_corrente.tipo == 'RDP':
                # Container per centrare il bottone nella cella
                widget_container = QWidget()
                layout_container = QHBoxLayout(widget_container)
                layout_container.setContentsMargins(5, 4, 5, 4)
                layout_container.setSpacing(0)
                layout_container.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                
                btn_rdp = QPushButton()
                btn_rdp.setFixedSize(108, 30)
                
                if cred.rdp_configurata:
                    btn_rdp.setText("🚀 RDP Conf")
                    btn_rdp.setObjectName("btn_success")
                    btn_rdp.setToolTip("Lancia RDP configurata")
                    btn_rdp.clicked.connect(lambda checked, c=cred: self.lancia_rdp_configurata_diretta(c))
                else:
                    btn_rdp.setText("🖥️ Connetti")
                    btn_rdp.setObjectName("btn_action")
                    btn_rdp.setToolTip("Connetti RDP")
                    btn_rdp.clicked.connect(lambda checked, c=cred: self.connetti_rdp_diretta(c))
                
                # Applica stile al bottone
                btn_rdp.setStyleSheet(self.styleSheet() + """
                    QPushButton {
                        padding: 5px 8px;
                        font-size: 9pt;
                        margin: 0px;
                    }
                """)
                layout_container.addWidget(btn_rdp, 0, Qt.AlignVCenter)
                
                self.tree_credenziali.setItemWidget(item, 5, widget_container)
    
    def connetti_rdp_diretta(self, credenziale: 'Credenziale'):
        """Connette a RDP con la credenziale specificata"""
        try:
            if not credenziale.host or not credenziale.host.strip():
                QMessageBox.warning(self, "Attenzione", "La credenziale non ha un host configurato")
                return
            
            success, message = self.rdp_launcher.connetti_rdp(
                credenziale.host,
                credenziale.username,
                credenziale.password,
                credenziale.porta
            )
            
            if success:
                QMessageBox.information(self, "RDP Lanciato", message)
            else:
                QMessageBox.warning(self, "Errore RDP", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante la connessione RDP:\n{str(e)}")
    
    def lancia_rdp_configurata_diretta(self, credenziale: 'Credenziale'):
        """Lancia una RDP configurata con la credenziale specificata"""
        try:
            if not credenziale.host or not credenziale.host.strip():
                QMessageBox.warning(self, "Attenzione", "Nessun file RDP configurato")
                return
            
            success, message = self.rdp_launcher.lancia_rdp_configurata(credenziale.host)
            
            if success:
                QMessageBox.information(self, "RDP Configurata", message)
            else:
                QMessageBox.warning(self, "Errore", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante il lancio RDP configurata:\n{str(e)}")
    
    def credenziale_selezionata(self, item, column):
        """Gestisce la selezione di una credenziale"""
        credenziale_id = item.data(0, Qt.UserRole)
        self.credenziale_corrente = self.credenziale_controller.ottieni_credenziale(credenziale_id)
        self.btn_duplica_credenziale.setEnabled(True)
        self.btn_modifica_credenziale.setEnabled(True)
        self.btn_elimina_credenziale.setEnabled(True)
    
    def copia_password(self, item, column):
        """Copia il campo specifico negli appunti con doppio click"""
        credenziale_id = item.data(0, Qt.UserRole)
        cred = self.credenziale_controller.ottieni_credenziale(credenziale_id)
        
        if cred:
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            
            # Copia campo in base alla colonna cliccata
            if column == 0:  # Username
                clipboard.setText(cred.username)
                QMessageBox.information(self, "Username Copiato",
                                      f"Username '{cred.username}' copiato negli appunti!")
            elif column == 1:  # Host/IP
                clipboard.setText(cred.host or "")
                QMessageBox.information(self, "Host Copiato",
                                      f"Host '{cred.host}' copiato negli appunti!")
            elif column == 3:  # Password
                clipboard.setText(cred.password)
                QMessageBox.information(self, "Password Copiata",
                                      f"Password copiata negli appunti!")
            else:
                # Per altre colonne non fa nulla
                pass
    
    # ===== GESTIONE CLIENTI =====
    
    def nuovo_cliente(self):
        """Crea un nuovo cliente"""
        dialog = ClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                pm_id = dialog.pm_combo.currentData()
                cliente_id = self.cliente_controller.crea_cliente(
                    dialog.nome_edit.text(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.vpn_exe_edit.text(),
                    dialog.get_vpn_windows_selezionata(),
                    pm_id
                )
                
                # Associa i consulenti selezionati
                consulenti_ids = dialog.get_consulenti_selezionati()
                for consulente_id in consulenti_ids:
                    self.risorse_controller.associa_consulente_cliente(cliente_id, consulente_id)
                
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Cliente creato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def modifica_cliente(self):
        """Modifica il cliente selezionato"""
        if not self.cliente_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da modificare")
            return
        
        dialog = ClienteDialog(self, self.cliente_corrente)
        if dialog.exec_() == QDialog.Accepted:
            try:
                pm_id = dialog.pm_combo.currentData()
                self.cliente_controller.modifica_cliente(
                    self.cliente_corrente.id,
                    dialog.nome_edit.text(),
                    dialog.descrizione_edit.toPlainText(),
                    dialog.vpn_exe_edit.text(),
                    dialog.get_vpn_windows_selezionata(),
                    pm_id
                )
                
                # Aggiorna associazioni consulenti
                # Prima rimuovi tutte le associazioni esistenti
                consulenti_attuali = self.risorse_controller.ottieni_consulenti_cliente(self.cliente_corrente.id)
                for consulente in consulenti_attuali:
                    self.risorse_controller.disassocia_consulente_cliente(self.cliente_corrente.id, consulente.id)
                
                # Poi aggiungi le nuove associazioni
                consulenti_ids = dialog.get_consulenti_selezionati()
                for consulente_id in consulenti_ids:
                    self.risorse_controller.associa_consulente_cliente(self.cliente_corrente.id, consulente_id)
                
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Cliente modificato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_cliente(self):
        """Elimina il cliente selezionato"""
        if not self.cliente_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da eliminare")
            return
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare il cliente '{self.cliente_corrente.nome}' "
            f"e tutti i suoi servizi e credenziali?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            self.cliente_controller.elimina_cliente(self.cliente_corrente.id)
            self.cliente_corrente = None
            self.servizio_corrente = None
            self.carica_dati()
            self.tree_credenziali.clear()
            self.lbl_info.setText("<h3>Seleziona un cliente o servizio</h3>")
            QMessageBox.information(self, "Successo", "Cliente eliminato con successo!")
    
    # ===== GESTIONE SERVIZI =====
    
    def nuovo_servizio(self, cliente_id: int):
        """Crea un nuovo servizio"""
        dialog = ServizioDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Prendi il link solo se il tipo è CRM o Web
                link = ""
                if dialog.tipo_combo.currentText() in ["CRM", "Web"]:
                    link = dialog.link_edit.text().strip()
                
                self.credenziale_controller.crea_servizio(
                    cliente_id,
                    dialog.nome_edit.text(),
                    dialog.tipo_combo.currentText(),
                    dialog.descrizione_edit.toPlainText(),
                    link
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Servizio creato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def duplica_servizio(self):
        """Duplica il servizio selezionato"""
        if not self.servizio_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da duplicare")
            return
        
        if not self.cliente_corrente:
            QMessageBox.warning(self, "Attenzione", "Cliente non trovato")
            return
        
        try:
            # Apre il dialog in modalità duplica con il tipo del servizio originale
            dialog = ServizioDialog(self, self.servizio_corrente, duplica_mode=True)
            if dialog.exec_() == QDialog.Accepted:
                try:
                    # Prendi il link solo se il tipo è CRM o Web
                    link = ""
                    if dialog.tipo_combo.currentText() in ["CRM", "Web"]:
                        link = dialog.link_edit.text().strip()
                    
                    self.credenziale_controller.crea_servizio(
                        self.cliente_corrente.id,
                        dialog.nome_edit.text(),
                        dialog.tipo_combo.currentText(),
                        dialog.descrizione_edit.toPlainText(),
                        link
                    )
                    self.carica_dati()
                    QMessageBox.information(self, "Successo", "Servizio duplicato con successo!")
                except ValueError as e:
                    QMessageBox.warning(self, "Errore", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante la duplicazione del servizio:\n{str(e)}")
    
    def modifica_servizio(self):
        """Modifica il servizio selezionato"""
        if not self.servizio_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da modificare")
            return
        
        dialog = ServizioDialog(self, self.servizio_corrente)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Prendi il link solo se il tipo è CRM o Web
                link = ""
                if dialog.tipo_combo.currentText() in ["CRM", "Web"]:
                    link = dialog.link_edit.text().strip()
                
                self.credenziale_controller.modifica_servizio(
                    self.servizio_corrente.id,
                    dialog.nome_edit.text(),
                    dialog.tipo_combo.currentText(),
                    dialog.descrizione_edit.toPlainText(),
                    link
                )
                self.carica_dati()
                QMessageBox.information(self, "Successo", "Servizio modificato con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_servizio(self):
        """Elimina il servizio selezionato"""
        if not self.servizio_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da eliminare")
            return
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare il servizio '{self.servizio_corrente.nome}' "
            f"e tutte le sue credenziali?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            self.credenziale_controller.elimina_servizio(self.servizio_corrente.id)
            self.servizio_corrente = None
            self.carica_dati()
            self.tree_credenziali.clear()
            QMessageBox.information(self, "Successo", "Servizio eliminato con successo!")
    
    # ===== GESTIONE CREDENZIALI =====
    
    def nuova_credenziale(self):
        """Crea una nuova credenziale"""
        if not self.servizio_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio")
            return
        
        dialog = CredenzialeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                porta = dialog.porta_spin.value() if dialog.porta_spin.value() > 0 else None
                self.credenziale_controller.crea_credenziale(
                    self.servizio_corrente.id,
                    dialog.get_username(),  # Usa il metodo che costruisce username da dominio + utente
                    dialog.password_edit.text(),
                    dialog.get_host_or_file(),  # Usa il metodo che restituisce host o file
                    porta,
                    dialog.note_edit.toPlainText(),
                    dialog.rdp_configurata_check.isChecked()
                )
                self.carica_credenziali()
                QMessageBox.information(self, "Successo", "Credenziale creata con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def duplica_credenziale(self):
        """Duplica la credenziale selezionata"""
        if not self.credenziale_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona una credenziale da duplicare")
            return
        
        if not self.servizio_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio")
            return
        
        # Apre il dialog in modalità duplica con i dati della credenziale selezionata
        dialog = CredenzialeDialog(self, self.credenziale_corrente, duplica_mode=True)
        if dialog.exec_() == QDialog.Accepted:
            try:
                porta = dialog.porta_spin.value() if dialog.porta_spin.value() > 0 else None
                self.credenziale_controller.crea_credenziale(
                    self.servizio_corrente.id,
                    dialog.get_username(),  # Usa il metodo che costruisce username da dominio + utente
                    dialog.password_edit.text(),
                    dialog.get_host_or_file(),  # Usa il metodo che restituisce host o file
                    porta,
                    dialog.note_edit.toPlainText(),
                    dialog.rdp_configurata_check.isChecked()
                )
                self.carica_credenziali()
                QMessageBox.information(self, "Successo", "Credenziale duplicata con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def modifica_credenziale(self):
        """Modifica la credenziale selezionata"""
        if not self.credenziale_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona una credenziale da modificare")
            return
        
        dialog = CredenzialeDialog(self, self.credenziale_corrente)
        if dialog.exec_() == QDialog.Accepted:
            try:
                porta = dialog.porta_spin.value() if dialog.porta_spin.value() > 0 else None
                self.credenziale_controller.modifica_credenziale(
                    self.credenziale_corrente.id,
                    dialog.get_username(),  # Usa il metodo che costruisce username da dominio + utente
                    dialog.password_edit.text(),
                    dialog.get_host_or_file(),  # Usa il metodo che restituisce host o file
                    porta,
                    dialog.note_edit.toPlainText(),
                    dialog.rdp_configurata_check.isChecked()
                )
                self.carica_credenziali()
                QMessageBox.information(self, "Successo", "Credenziale modificata con successo!")
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def elimina_credenziale(self):
        """Elimina la credenziale selezionata"""
        if not self.credenziale_corrente:
            QMessageBox.warning(self, "Attenzione", "Seleziona una credenziale da eliminare")
            return
        
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare la credenziale per '{self.credenziale_corrente.username}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if risposta == QMessageBox.Yes:
            self.credenziale_controller.elimina_credenziale(self.credenziale_corrente.id)
            self.credenziale_corrente = None
            self.carica_credenziali()
            QMessageBox.information(self, "Successo", "Credenziale eliminata con successo!")
    
    # ===== UTILITY =====
    
    def lancia_vpn_exe(self):
        """Lancia VPN da file EXE"""
        try:
            if not self.cliente_corrente:
                QMessageBox.warning(self, "Attenzione", "Nessun cliente selezionato")
                return
            
            if not self.cliente_corrente.vpn_exe_path or not self.cliente_corrente.vpn_exe_path.strip():
                QMessageBox.warning(self, "Attenzione", "Nessun file VPN EXE configurato per questo cliente")
                return
            
            success, message = self.vpn_launcher.lancia_vpn_exe(self.cliente_corrente.vpn_exe_path)
            
            if success:
                QMessageBox.information(self, "VPN Lanciata", message)
            else:
                QMessageBox.warning(self, "Errore VPN", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante il lancio della VPN:\n{str(e)}")

    
    def lancia_vpn_windows(self):
        """Lancia VPN Windows"""
        try:
            if not self.cliente_corrente:
                QMessageBox.warning(self, "Attenzione", "Nessun cliente selezionato")
                return
            
            if not self.cliente_corrente.vpn_windows_name or not self.cliente_corrente.vpn_windows_name.strip():
                QMessageBox.warning(self, "Attenzione", "Nessuna VPN Windows configurata per questo cliente")
                return
            
            # Mostra un messaggio di attesa
            QMessageBox.information(self, "Connessione in corso", 
                                  f"Connessione alla VPN '{self.cliente_corrente.vpn_windows_name}' in corso...\n"
                                  "Questo potrebbe richiedere alcuni secondi.")
            
            success, message = self.vpn_launcher.connetti_vpn_windows(
                self.cliente_corrente.vpn_windows_name
            )
            
            if success:
                QMessageBox.information(self, "VPN Connessa", message)
            else:
                QMessageBox.warning(self, "Errore VPN", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante il lancio della VPN:\n{str(e)}")

    
    def apri_link_servizio(self):
        """Apre il link del servizio nel browser predefinito"""
        try:
            if not self.servizio_corrente:
                QMessageBox.warning(self, "Attenzione", "Nessun servizio selezionato")
                return
            
            if not self.servizio_corrente.link or not self.servizio_corrente.link.strip():
                QMessageBox.warning(self, "Attenzione", "Nessun link configurato per questo servizio")
                return
            
            # Apri il link nel browser predefinito
            url = self.servizio_corrente.link
            # Aggiungi https:// se manca il protocollo
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            QDesktopServices.openUrl(QUrl(url))
            
        except Exception as e:
            QMessageBox.critical(self, "Errore", 
                               f"Errore durante l'apertura del link:\n{str(e)}")
    
    def connetti_rdp(self):
        """Connette a RDP con le credenziali selezionate"""
        try:
            if not self.credenziale_corrente:
                QMessageBox.warning(self, "Attenzione", "Seleziona una credenziale")
                return
            
            if not self.credenziale_corrente.host or not self.credenziale_corrente.host.strip():
                QMessageBox.warning(self, "Attenzione", "La credenziale non ha un host configurato")
                return
            
            success, message = self.rdp_launcher.connetti_rdp(
                self.credenziale_corrente.host,
                self.credenziale_corrente.username,
                self.credenziale_corrente.password,
                self.credenziale_corrente.porta
            )
            
            if success:
                QMessageBox.information(self, "RDP Lanciato", message)
            else:
                QMessageBox.warning(self, "Errore RDP", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", 
                               f"Errore durante la connessione RDP:\n{str(e)}")
    
    def lancia_rdp_configurata(self):
        """Lancia una RDP già configurata aprendo direttamente il file .rdp"""
        try:
            if not self.credenziale_corrente:
                QMessageBox.warning(self, "Attenzione", "Seleziona una credenziale")
                return
            
            file_rdp = self.credenziale_corrente.host  # Il campo host contiene il percorso del file
            if not file_rdp or not file_rdp.strip():
                QMessageBox.warning(self, "Attenzione", "Nessun file RDP configurato")
                return
            
            # Verifica che il file esista
            import os
            if not os.path.exists(file_rdp):
                QMessageBox.warning(self, "Errore", f"File RDP non trovato:\n{file_rdp}")
                return
            
            # Lancia il file .rdp direttamente
            import subprocess
            subprocess.Popen([file_rdp], shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            
            QMessageBox.information(self, "RDP Lanciato", 
                                  f"File RDP lanciato:\n{os.path.basename(file_rdp)}")
                
        except Exception as e:
            QMessageBox.critical(self, "Errore", 
                               f"Errore durante il lancio della RDP:\n{str(e)}")

    
    def mostra_menu_contestuale(self, position):
        """Mostra menu contestuale sul tree"""
        item = self.tree_clienti.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        menu = QMenu()
        
        if data['tipo'] == 'cliente':
            azione_nuovo_servizio = menu.addAction("➕ Nuovo Servizio")
            menu.addSeparator()
            azione_gestione_consulenti = menu.addAction("👥 Gestisci Consulenti")
            azione_rubrica = menu.addAction("📇 Rubrica Contatti")
            menu.addSeparator()
            azione_modifica = menu.addAction("✏️ Modifica Cliente")
            azione_elimina = menu.addAction("🗑️ Elimina Cliente")
            
            azione = menu.exec_(self.tree_clienti.viewport().mapToGlobal(position))
            
            if azione == azione_nuovo_servizio:
                self.nuovo_servizio(data['id'])
            elif azione == azione_gestione_consulenti:
                self.gestisci_consulenti_cliente(data['id'])
            elif azione == azione_rubrica:
                self.apri_rubrica_contatti(data['id'])
            elif azione == azione_modifica:
                self.cliente_corrente = self.cliente_controller.ottieni_cliente(data['id'])
                self.modifica_cliente()
            elif azione == azione_elimina:
                self.cliente_corrente = self.cliente_controller.ottieni_cliente(data['id'])
                self.elimina_cliente()
        
        elif data['tipo'] == 'servizio':
            azione_duplica = menu.addAction("📋 Duplica Servizio")
            azione_modifica = menu.addAction("✏️ Modifica Servizio")
            azione_elimina = menu.addAction("🗑️ Elimina Servizio")
            
            azione = menu.exec_(self.tree_clienti.viewport().mapToGlobal(position))
            
            if azione == azione_duplica:
                self.servizio_corrente = self.credenziale_controller.ottieni_servizio(data['id'])
                self.cliente_corrente = self.cliente_controller.ottieni_cliente(data['cliente_id'])
                self.duplica_servizio()
            elif azione == azione_modifica:
                self.servizio_corrente = self.credenziale_controller.ottieni_servizio(data['id'])
                self.modifica_servizio()
            elif azione == azione_elimina:
                self.servizio_corrente = self.credenziale_controller.ottieni_servizio(data['id'])
                self.elimina_servizio()
    
    def closeEvent(self, event):
        """Chiude il database quando si chiude l'applicazione"""
        self.db.close()
        event.accept()


# ===== DIALOGS =====

class ClienteDialog(QDialog):
    """Dialog per creare/modificare un cliente"""
    
    def __init__(self, parent, cliente: Cliente = None):
        super().__init__(parent)
        self.cliente = cliente
        self.vpn_launcher = VPNLauncher()
        self.risorse_controller = parent.risorse_controller
        self.init_ui()
    
    def init_ui(self):
        titolo = "Modifica Cliente" if self.cliente else "Nuovo Cliente"
        self.setWindowTitle(titolo)
        self.setMinimumWidth(650)
        
        # Applica stile al dialog
        self.setStyleSheet(self.parent().styleSheet())
        
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Campo nome
        self.nome_edit = QLineEdit()
        if self.cliente:
            self.nome_edit.setText(self.cliente.nome)
        layout.addRow("Nome *:", self.nome_edit)
        
        # Campo descrizione
        self.descrizione_edit = QTextEdit()
        self.descrizione_edit.setMaximumHeight(80)
        if self.cliente and self.cliente.descrizione:
            self.descrizione_edit.setPlainText(self.cliente.descrizione)
        layout.addRow("Descrizione:", self.descrizione_edit)
        
        # PM di riferimento
        self.pm_combo = QComboBox()
        self.pm_combo.addItem("-- Nessun PM --", None)
        pms = self.risorse_controller.ottieni_tutti_pm()
        for pm in pms:
            self.pm_combo.addItem(f"👤 {pm.nome}", pm.id)
        
        if self.cliente and self.cliente.pm_id:
            index = self.pm_combo.findData(self.cliente.pm_id)
            if index >= 0:
                self.pm_combo.setCurrentIndex(index)
        
        layout.addRow("PM Riferimento:", self.pm_combo)
        
        # Consulenti associati
        consulenti_layout = QVBoxLayout()
        consulenti_layout.addWidget(QLabel("Consulenti:"))
        
        self.list_consulenti = QListWidget()
        self.list_consulenti.setMaximumHeight(120)
        self.list_consulenti.setSelectionMode(QListWidget.MultiSelection)
        
        # Carica tutti i consulenti
        tutti_consulenti = self.risorse_controller.ottieni_tutti_consulenti()
        consulenti_associati_ids = set()
        
        if self.cliente:
            consulenti_associati = self.risorse_controller.ottieni_consulenti_cliente(self.cliente.id)
            consulenti_associati_ids = {c.id for c in consulenti_associati}
        
        for consulente in tutti_consulenti:
            item = QListWidgetItem(f"{consulente.nome} - {consulente.competenza or 'N/A'}")
            item.setData(Qt.UserRole, consulente.id)
            self.list_consulenti.addItem(item)
            
            # Seleziona se già associato
            if consulente.id in consulenti_associati_ids:
                item.setSelected(True)
        
        consulenti_layout.addWidget(self.list_consulenti)
        consulenti_layout.addWidget(QLabel("<i>Tieni premuto Ctrl per selezione multipla</i>"))
        layout.addRow(consulenti_layout)
        
        # VPN EXE
        vpn_exe_layout = QHBoxLayout()
        self.vpn_exe_edit = QLineEdit()
        if self.cliente and self.cliente.vpn_exe_path:
            self.vpn_exe_edit.setText(self.cliente.vpn_exe_path)
        btn_sfoglia = QPushButton("📁 Sfoglia")
        btn_sfoglia.clicked.connect(self.sfoglia_vpn_exe)
        vpn_exe_layout.addWidget(self.vpn_exe_edit)
        vpn_exe_layout.addWidget(btn_sfoglia)
        layout.addRow("VPN EXE:", vpn_exe_layout)
        
        # VPN Windows - ComboBox con VPN disponibili
        vpn_win_layout = QHBoxLayout()
        self.vpn_win_combo = QComboBox()
        self.vpn_win_combo.setEditable(False)
        self.vpn_win_combo.addItem("-- Nessuna VPN --", "")
        
        # Carica le VPN Windows disponibili
        btn_ricarica_vpn = QPushButton("🔄")
        btn_ricarica_vpn.setMaximumWidth(40)
        btn_ricarica_vpn.setToolTip("Ricarica elenco VPN Windows")
        btn_ricarica_vpn.clicked.connect(self.carica_vpn_windows)
        
        vpn_win_layout.addWidget(self.vpn_win_combo)
        vpn_win_layout.addWidget(btn_ricarica_vpn)
        layout.addRow("VPN Windows:", vpn_win_layout)
        
        # Carica le VPN al primo avvio
        self.carica_vpn_windows()
        
        layout.addRow("", QLabel())  # Spaziatura
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.setObjectName("btn_success")
        btn_annulla.setObjectName("btn_neutral")
        btn_salva.setMinimumWidth(120)
        btn_annulla.setMinimumWidth(120)
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)
    
    def carica_vpn_windows(self):
        """Carica l'elenco delle VPN Windows configurate nel sistema"""
        # Salva la selezione corrente se presente
        vpn_corrente = self.cliente.vpn_windows_name if self.cliente else ""
        
        # Pulisci e reinizializza il combo
        self.vpn_win_combo.clear()
        self.vpn_win_combo.addItem("-- Nessuna VPN --", "")
        
        # Ottieni le VPN disponibili
        success, vpn_list = self.vpn_launcher.ottieni_vpn_disponibili()
        
        if success and vpn_list:
            # Aggiungi ogni VPN alla lista
            for vpn_name in vpn_list:
                self.vpn_win_combo.addItem(f"🔒 {vpn_name}", vpn_name)
            
            # Ripristina la selezione precedente se esiste
            if vpn_corrente:
                index = self.vpn_win_combo.findData(vpn_corrente)
                if index >= 0:
                    self.vpn_win_combo.setCurrentIndex(index)
            
            # Mostra messaggio di successo nella tooltip
            self.vpn_win_combo.setToolTip(f"Trovate {len(vpn_list)} VPN configurate")
        else:
            # Nessuna VPN trovata
            self.vpn_win_combo.setToolTip("Nessuna VPN Windows configurata nel sistema")
            
            # Se il cliente aveva una VPN impostata manualmente, permettiamo di mantenerla
            if vpn_corrente:
                self.vpn_win_combo.addItem(f"⚠️ {vpn_corrente} (non trovata)", vpn_corrente)
                self.vpn_win_combo.setCurrentIndex(1)
    
    def get_vpn_windows_selezionata(self) -> str:
        """Restituisce il nome della VPN Windows selezionata"""
        return self.vpn_win_combo.currentData() or ""
    
    def get_consulenti_selezionati(self) -> list:
        """Restituisce la lista degli ID dei consulenti selezionati"""
        consulenti_ids = []
        for i in range(self.list_consulenti.count()):
            item = self.list_consulenti.item(i)
            if item.isSelected():
                consulenti_ids.append(item.data(Qt.UserRole))
        return consulenti_ids
    
    def sfoglia_vpn_exe(self):
        """Apre dialog per selezionare file EXE"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona File VPN", "", "Eseguibili (*.exe);;Tutti i file (*.*)"
        )
        if file_path:
            self.vpn_exe_edit.setText(file_path)


class ServizioDialog(QDialog):
    """Dialog per creare/modificare un servizio"""
    
    def __init__(self, parent, servizio: Servizio = None, duplica_mode: bool = False):
        super().__init__(parent)
        self.servizio = servizio
        self.duplica_mode = duplica_mode
        self.init_ui()
    
    def init_ui(self):
        if self.duplica_mode:
            titolo = "Duplica Servizio"
        else:
            titolo = "Modifica Servizio" if self.servizio else "Nuovo Servizio"
        self.setWindowTitle(titolo)
        self.setMinimumWidth(500)
        
        # Applica stile al dialog
        self.setStyleSheet(self.parent().styleSheet())
        
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Campo nome
        self.nome_edit = QLineEdit()
        if self.servizio and not self.duplica_mode:
            self.nome_edit.setText(self.servizio.nome)
        layout.addRow("Nome *:", self.nome_edit)
        
        # Tipo servizio
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(Servizio.TIPI_DISPONIBILI)
        if self.servizio:
            index = self.tipo_combo.findText(self.servizio.tipo)
            if index >= 0:
                self.tipo_combo.setCurrentIndex(index)
        layout.addRow("Tipo *:", self.tipo_combo)
        
        # Link (solo per CRM e Web)
        self.link_edit = QLineEdit()
        self.link_edit.setPlaceholderText("https://...")
        if self.servizio and hasattr(self.servizio, 'link') and self.servizio.link and not self.duplica_mode:
            self.link_edit.setText(self.servizio.link)
        self.link_label = QLabel("Link:")
        layout.addRow(self.link_label, self.link_edit)
        
        # Descrizione
        self.descrizione_edit = QTextEdit()
        self.descrizione_edit.setMaximumHeight(80)
        if self.servizio and self.servizio.descrizione and not self.duplica_mode:
            self.descrizione_edit.setPlainText(self.servizio.descrizione)
        layout.addRow("Descrizione:", self.descrizione_edit)
        
        # Connetti il segnale DOPO aver creato tutti i widget
        self.tipo_combo.currentTextChanged.connect(self.on_tipo_changed)
        
        # Imposta visibilità iniziale del link
        self.on_tipo_changed(self.tipo_combo.currentText())
        
        layout.addRow("", QLabel())  # Spaziatura
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.setObjectName("btn_success")
        btn_annulla.setObjectName("btn_neutral")
        btn_salva.setMinimumWidth(120)
        btn_annulla.setMinimumWidth(120)
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)
    
    def on_tipo_changed(self, tipo):
        """Mostra/nascondi campo link in base al tipo di servizio"""
        mostra_link = tipo in ["CRM", "Web"]
        self.link_label.setVisible(mostra_link)
        self.link_edit.setVisible(mostra_link)
    
    def toggle_rdp_mode(self, is_rdp_configurata):
        """Mostra/nascondi campi in base al tipo di RDP"""
        # RDP Configurata: mostra file picker, nascondi host/porta
        self.file_rdp_label.setVisible(is_rdp_configurata)
        self.file_rdp_edit.setVisible(is_rdp_configurata)
        for i in range(self.file_rdp_layout.count()):
            widget = self.file_rdp_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_rdp_configurata)
        
        # RDP Normale: mostra host/porta, nascondi file picker
        self.host_label.setVisible(not is_rdp_configurata)
        self.host_edit.setVisible(not is_rdp_configurata)
        self.porta_label.setVisible(not is_rdp_configurata)
        self.porta_spin.setVisible(not is_rdp_configurata)
    
    def seleziona_file_rdp(self):
        """Apre dialog per selezionare file .rdp"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file RDP",
            "",
            "File RDP (*.rdp);;Tutti i file (*.*)"
        )
        if file_path:
            self.file_rdp_edit.setText(file_path)
    
    def get_host_or_file(self):
        """Restituisce host o percorso file in base al tipo"""
        if self.rdp_configurata_check.isChecked():
            return self.file_rdp_edit.text()
        else:
            return self.host_edit.text()


class CredenzialeDialog(QDialog):
    """Dialog per creare/modificare una credenziale"""
    
    def __init__(self, parent, credenziale: Credenziale = None, duplica_mode: bool = False):
        super().__init__(parent)
        self.credenziale = credenziale
        self.duplica_mode = duplica_mode
        self.init_ui()
    
    def init_ui(self):
        if self.duplica_mode:
            titolo = "Duplica Credenziale"
        else:
            titolo = "Modifica Credenziale" if self.credenziale else "Nuova Credenziale"
        self.setWindowTitle(titolo)
        self.setMinimumWidth(550)
        
        # Applica stile al dialog
        self.setStyleSheet(self.parent().styleSheet())
        
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Dominio
        self.dominio_edit = QLineEdit()
        self.dominio_edit.setPlaceholderText("es: AZIENDA")
        if self.credenziale and self.credenziale.username:
            # Estrai dominio da username se presente (formato DOMINIO\utente)
            if '\\' in self.credenziale.username:
                dominio, _ = self.credenziale.username.split('\\', 1)
                self.dominio_edit.setText(dominio)
        layout.addRow("Dominio:", self.dominio_edit)
        
        # Utente (separato da dominio)
        self.utente_edit = QLineEdit()
        if self.credenziale and self.credenziale.username:
            # Estrai utente da username
            if '\\' in self.credenziale.username:
                _, utente = self.credenziale.username.split('\\', 1)
                self.utente_edit.setText(utente if not self.duplica_mode else "")
            else:
                self.utente_edit.setText(self.credenziale.username if not self.duplica_mode else "")
        layout.addRow("Utente *:", self.utente_edit)
        
        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        if self.credenziale and not self.duplica_mode:
            self.password_edit.setText(self.credenziale.password)
        
        # Toggle mostra password
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_edit)
        btn_mostra = QPushButton("👁️")
        btn_mostra.setMaximumWidth(40)
        btn_mostra.pressed.connect(lambda: self.password_edit.setEchoMode(QLineEdit.Normal))
        btn_mostra.released.connect(lambda: self.password_edit.setEchoMode(QLineEdit.Password))
        password_layout.addWidget(btn_mostra)
        layout.addRow("Password *:", password_layout)
        
        # Checkbox RDP Configurata (prima degli altri campi per controllare visibilità)
        from PyQt5.QtWidgets import QCheckBox
        self.rdp_configurata_check = QCheckBox("RDP già configurata (file .rdp salvato)")
        self.rdp_configurata_check.setToolTip("Seleziona se questa è una RDP salvata come file .rdp")
        # NON connettere ancora il segnale - lo faremo dopo aver creato tutti i widget
        if self.credenziale:
            self.rdp_configurata_check.setChecked(self.credenziale.rdp_configurata)
        layout.addRow("", self.rdp_configurata_check)
        
        # Percorso File RDP (solo per RDP configurate)
        self.file_rdp_layout = QHBoxLayout()
        self.file_rdp_edit = QLineEdit()
        self.file_rdp_edit.setPlaceholderText("Seleziona il file .rdp...")
        btn_sfoglia = QPushButton("📁 Sfoglia")
        btn_sfoglia.clicked.connect(self.seleziona_file_rdp)
        self.file_rdp_layout.addWidget(self.file_rdp_edit)
        self.file_rdp_layout.addWidget(btn_sfoglia)
        self.file_rdp_label = QLabel("File .rdp:")
        layout.addRow(self.file_rdp_label, self.file_rdp_layout)
        
        # Host/IP (solo per RDP normali)
        self.host_edit = QLineEdit()
        if self.credenziale:
            # Se è RDP configurata, il campo host contiene il percorso del file
            if self.credenziale.rdp_configurata:
                self.file_rdp_edit.setText(self.credenziale.host or "")
            else:
                self.host_edit.setText(self.credenziale.host or "")
        self.host_label = QLabel("Host/IP:")
        layout.addRow(self.host_label, self.host_edit)
        
        # Porta (solo per RDP normali)
        self.porta_spin = QSpinBox()
        self.porta_spin.setRange(0, 65535)
        if self.credenziale and self.credenziale.porta:
            self.porta_spin.setValue(self.credenziale.porta)
        self.porta_label = QLabel("Porta:")
        layout.addRow(self.porta_label, self.porta_spin)
        
        # Ora che tutti i widget sono creati, connetti il segnale e imposta visibilità iniziale
        self.rdp_configurata_check.toggled.connect(self.toggle_rdp_mode)
        self.toggle_rdp_mode(self.rdp_configurata_check.isChecked())
        
        # Note
        self.note_edit = QTextEdit()
        self.note_edit.setMaximumHeight(80)
        if self.credenziale and self.credenziale.note:
            self.note_edit.setPlainText(self.credenziale.note)
        layout.addRow("Note:", self.note_edit)
        
        layout.addRow("", QLabel())  # Spaziatura
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_salva = QPushButton("💾 Salva")
        btn_annulla = QPushButton("❌ Annulla")
        btn_salva.setObjectName("btn_success")
        btn_annulla.setObjectName("btn_neutral")
        btn_salva.setMinimumWidth(120)
        btn_annulla.setMinimumWidth(120)
        btn_salva.clicked.connect(self.accept)
        btn_annulla.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_salva)
        btn_layout.addWidget(btn_annulla)
        layout.addRow(btn_layout)
    
    def toggle_rdp_mode(self, is_rdp_configurata):
        """Mostra/nascondi campi in base al tipo di RDP"""
        # RDP Configurata: mostra file picker, nascondi host/porta
        self.file_rdp_label.setVisible(is_rdp_configurata)
        self.file_rdp_edit.setVisible(is_rdp_configurata)
        for i in range(self.file_rdp_layout.count()):
            widget = self.file_rdp_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_rdp_configurata)
        
        # RDP Normale: mostra host/porta, nascondi file picker
        self.host_label.setVisible(not is_rdp_configurata)
        self.host_edit.setVisible(not is_rdp_configurata)
        self.porta_label.setVisible(not is_rdp_configurata)
        self.porta_spin.setVisible(not is_rdp_configurata)
    
    def seleziona_file_rdp(self):
        """Apre dialog per selezionare file .rdp"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file RDP",
            "",
            "File RDP (*.rdp);;Tutti i file (*.*)"
        )
        if file_path:
            self.file_rdp_edit.setText(file_path)
    
    def get_host_or_file(self):
        """Restituisce host o percorso file in base al tipo"""
        if self.rdp_configurata_check.isChecked():
            return self.file_rdp_edit.text()
        else:
            return self.host_edit.text()

    def get_username(self):
        """Costruisce username nel formato DOMINIO\\Utente"""
        dominio = self.dominio_edit.text().strip()
        utente = self.utente_edit.text().strip()
        
        if dominio and utente:
            return f"{dominio}\\{utente}"
        elif utente:
            return utente
        else:
            return ""
