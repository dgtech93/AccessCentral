"""
Modulo per import/export dati in formato CSV/Excel
"""

import csv
import os
from typing import List, Dict, Tuple
from models.database import DatabaseManager
from models.cliente import Cliente
from models.servizio import Servizio
from models.credenziale import Credenziale
from models.pm import PM
from models.consulente import Consulente


class ImportExportManager:
    """Gestisce import ed export di dati in formato CSV/Excel"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def export_to_csv(self, file_path: str) -> Tuple[bool, str]:
        """
        Esporta tutti i dati in formato CSV
        
        Args:
            file_path: Percorso file CSV di output
            
        Returns:
            Tupla (successo, messaggio)
        """
        try:
            clienti = Cliente.get_all(self.db)
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = [
                    'Cliente', 'Cliente_Descrizione', 'VPN_EXE', 'VPN_Windows',
                    'Servizio', 'Servizio_Tipo', 'Servizio_Descrizione', 'Servizio_Link',
                    'Dominio', 'Utente', 'Username', 'Password', 'Host', 'Porta', 
                    'Note', 'RDP_Configurata'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                rows_exported = 0
                
                for cliente in clienti:
                    servizi = Servizio.get_by_cliente(self.db, cliente.id)
                    
                    if not servizi:
                        # Cliente senza servizi
                        writer.writerow({
                            'Cliente': cliente.nome,
                            'Cliente_Descrizione': cliente.descrizione,
                            'VPN_EXE': cliente.vpn_exe_path,
                            'VPN_Windows': cliente.vpn_windows_name,
                            'Servizio': '',
                            'Servizio_Tipo': '',
                            'Servizio_Descrizione': '',
                            'Servizio_Link': '',
                            'Dominio': '',
                            'Utente': '',
                            'Username': '',
                            'Password': '',
                            'Host': '',
                            'Porta': '',
                            'Note': '',
                            'RDP_Configurata': ''
                        })
                        rows_exported += 1
                    
                    for servizio in servizi:
                        credenziali = Credenziale.get_by_servizio(self.db, servizio.id)
                        
                        if not credenziali:
                            # Servizio senza credenziali
                            writer.writerow({
                                'Cliente': cliente.nome,
                                'Cliente_Descrizione': cliente.descrizione,
                                'VPN_EXE': cliente.vpn_exe_path,
                                'VPN_Windows': cliente.vpn_windows_name,
                                'Servizio': servizio.nome,
                                'Servizio_Tipo': servizio.tipo,
                                'Servizio_Descrizione': servizio.descrizione,
                                'Servizio_Link': servizio.link if hasattr(servizio, 'link') else '',
                                'Dominio': '',
                                'Utente': '',
                                'Username': '',
                                'Password': '',
                                'Host': '',
                                'Porta': '',
                                'Note': '',
                                'RDP_Configurata': ''
                            })
                            rows_exported += 1
                        
                        for credenziale in credenziali:
                            # Estrai dominio e utente se presente il formato DOMINIO\Utente
                            username = credenziale.username
                            dominio = ''
                            utente = username
                            
                            if '\\' in username:
                                parts = username.split('\\', 1)
                                dominio = parts[0]
                                utente = parts[1]
                            
                            writer.writerow({
                                'Cliente': cliente.nome,
                                'Cliente_Descrizione': cliente.descrizione,
                                'VPN_EXE': cliente.vpn_exe_path,
                                'VPN_Windows': cliente.vpn_windows_name,
                                'Servizio': servizio.nome,
                                'Servizio_Tipo': servizio.tipo,
                                'Servizio_Descrizione': servizio.descrizione,
                                'Servizio_Link': servizio.link if hasattr(servizio, 'link') else '',
                                'Dominio': dominio,
                                'Utente': utente,
                                'Username': username,
                                'Password': credenziale.password,
                                'Host': credenziale.host,
                                'Porta': credenziale.porta if credenziale.porta else '',
                                'Note': credenziale.note,
                                'RDP_Configurata': 'Sì' if credenziale.rdp_configurata else 'No'
                            })
                            rows_exported += 1
                
                return True, f"Export completato: {rows_exported} righe esportate"
                
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def export_to_excel(self, file_path: str) -> Tuple[bool, str]:
        """
        Esporta tutti i dati in formato Excel
        
        Args:
            file_path: Percorso file Excel di output
            
        Returns:
            Tupla (successo, messaggio)
        """
        try:
            import pandas as pd
            
            clienti = Cliente.get_all(self.db)
            
            data = []
            
            for cliente in clienti:
                servizi = Servizio.get_by_cliente(self.db, cliente.id)
                
                if not servizi:
                    # Cliente senza servizi
                    data.append({
                        'Cliente': cliente.nome,
                        'Cliente_Descrizione': cliente.descrizione,
                        'VPN_EXE': cliente.vpn_exe_path,
                        'VPN_Windows': cliente.vpn_windows_name,
                        'Servizio': '',
                        'Servizio_Tipo': '',
                        'Servizio_Descrizione': '',
                        'Servizio_Link': '',
                        'Dominio': '',
                        'Utente': '',
                        'Username': '',
                        'Password': '',
                        'Host': '',
                        'Porta': '',
                        'Note': '',
                        'RDP_Configurata': ''
                    })
                
                for servizio in servizi:
                    credenziali = Credenziale.get_by_servizio(self.db, servizio.id)
                    
                    if not credenziali:
                        # Servizio senza credenziali
                        data.append({
                            'Cliente': cliente.nome,
                            'Cliente_Descrizione': cliente.descrizione,
                            'VPN_EXE': cliente.vpn_exe_path,
                            'VPN_Windows': cliente.vpn_windows_name,
                            'Servizio': servizio.nome,
                            'Servizio_Tipo': servizio.tipo,
                            'Servizio_Descrizione': servizio.descrizione,
                            'Servizio_Link': servizio.link if hasattr(servizio, 'link') else '',
                            'Dominio': '',
                            'Utente': '',
                            'Username': '',
                            'Password': '',
                            'Host': '',
                            'Porta': '',
                            'Note': '',
                            'RDP_Configurata': ''
                        })
                    
                    for credenziale in credenziali:
                        # Estrai dominio e utente se presente il formato DOMINIO\Utente
                        username = credenziale.username
                        dominio = ''
                        utente = username
                        
                        if '\\' in username:
                            parts = username.split('\\', 1)
                            dominio = parts[0]
                            utente = parts[1]
                        
                        data.append({
                            'Cliente': cliente.nome,
                            'Cliente_Descrizione': cliente.descrizione,
                            'VPN_EXE': cliente.vpn_exe_path,
                            'VPN_Windows': cliente.vpn_windows_name,
                            'Servizio': servizio.nome,
                            'Servizio_Tipo': servizio.tipo,
                            'Servizio_Descrizione': servizio.descrizione,
                            'Servizio_Link': servizio.link if hasattr(servizio, 'link') else '',
                            'Dominio': dominio,
                            'Utente': utente,
                            'Username': username,
                            'Password': credenziale.password,
                            'Host': credenziale.host,
                            'Porta': credenziale.porta if credenziale.porta else '',
                            'Note': credenziale.note,
                            'RDP_Configurata': 'Sì' if credenziale.rdp_configurata else 'No'
                        })
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            return True, f"Export completato: {len(data)} righe esportate"
            
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa export CSV."
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def import_from_file(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Importa dati da file CSV o Excel
        
        Args:
            file_path: Percorso file da importare
            
        Returns:
            Tupla (successo, messaggio, statistiche)
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            return self._import_from_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self._import_from_excel(file_path)
        else:
            return False, "Formato file non supportato. Usa .csv, .xlsx o .xls", {}
    
    def _import_from_csv(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa dati da file CSV"""
        try:
            stats = {'clienti': 0, 'servizi': 0, 'credenziali': 0, 'errori': 0}
            clienti_map = {}  # nome_cliente -> id
            servizi_map = {}  # (cliente_id, nome_servizio) -> id
            
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        cliente_nome = row.get('Cliente', '').strip()
                        if not cliente_nome:
                            continue
                        
                        # Crea o recupera cliente
                        if cliente_nome not in clienti_map:
                            # Verifica se il cliente esiste già
                            clienti_esistenti = Cliente.get_all(self.db)
                            cliente_esistente = next((c for c in clienti_esistenti if c.nome == cliente_nome), None)
                            
                            if cliente_esistente:
                                clienti_map[cliente_nome] = cliente_esistente.id
                            else:
                                cliente_id = Cliente.create(
                                    self.db,
                                    nome=cliente_nome,
                                    descrizione=row.get('Cliente_Descrizione', '').strip(),
                                    vpn_exe_path=row.get('VPN_EXE', '').strip(),
                                    vpn_windows_name=row.get('VPN_Windows', '').strip()
                                )
                                clienti_map[cliente_nome] = cliente_id
                                stats['clienti'] += 1
                        
                        cliente_id = clienti_map[cliente_nome]
                        
                        # Crea servizio se presente
                        servizio_nome = row.get('Servizio', '').strip()
                        if servizio_nome:
                            servizio_key = (cliente_id, servizio_nome)
                            
                            if servizio_key not in servizi_map:
                                # Verifica se il servizio esiste già
                                servizi_esistenti = Servizio.get_by_cliente(self.db, cliente_id)
                                servizio_esistente = next((s for s in servizi_esistenti if s.nome == servizio_nome), None)
                                
                                if servizio_esistente:
                                    servizi_map[servizio_key] = servizio_esistente.id
                                else:
                                    servizio_tipo = row.get('Servizio_Tipo', 'Altro').strip()
                                    if servizio_tipo not in Servizio.TIPI_DISPONIBILI:
                                        servizio_tipo = 'Altro'
                                    
                                    servizio_id = Servizio.create(
                                        self.db,
                                        cliente_id=cliente_id,
                                        nome=servizio_nome,
                                        tipo=servizio_tipo,
                                        descrizione=row.get('Servizio_Descrizione', '').strip(),
                                        link=row.get('Servizio_Link', '').strip()
                                    )
                                    servizi_map[servizio_key] = servizio_id
                                    stats['servizi'] += 1
                            
                            servizio_id = servizi_map[servizio_key]
                            
                            # Crea credenziale se presente
                            username = row.get('Username', '').strip()
                            password = row.get('Password', '').strip()
                            
                            # Se Username vuoto ma ci sono Dominio/Utente, costruisci username
                            if not username:
                                dominio = row.get('Dominio', '').strip()
                                utente = row.get('Utente', '').strip()
                                if dominio and utente:
                                    username = f"{dominio}\\{utente}"
                                elif utente:
                                    username = utente
                            
                            if username or password:
                                porta_str = row.get('Porta', '').strip()
                                porta = int(porta_str) if porta_str and porta_str.isdigit() else None
                                
                                rdp_config = row.get('RDP_Configurata', '').strip().lower()
                                rdp_configurata = rdp_config in ['sì', 'si', 'yes', '1', 'true']
                                
                                host = row.get('Host', '').strip()
                                note = row.get('Note', '').strip()
                                
                                # Verifica se la credenziale esiste già
                                credenziali_esistenti = Credenziale.get_by_servizio(self.db, servizio_id)
                                credenziale_duplicata = False
                                
                                for cred in credenziali_esistenti:
                                    if (cred.username == username and 
                                        cred.password == password and
                                        cred.host == host and
                                        cred.porta == porta and
                                        cred.note == note and
                                        cred.rdp_configurata == rdp_configurata):
                                        credenziale_duplicata = True
                                        break
                                
                                if not credenziale_duplicata:
                                    Credenziale.create(
                                        self.db,
                                        servizio_id=servizio_id,
                                        username=username,
                                        password=password,
                                        host=host,
                                        porta=porta,
                                        note=note,
                                        rdp_configurata=rdp_configurata
                                    )
                                    stats['credenziali'] += 1
                    
                    except Exception as e:
                        stats['errori'] += 1
                        print(f"Errore riga: {e}")
                        continue
            
            msg = f"Import completato:\n"
            msg += f"- Clienti: {stats['clienti']}\n"
            msg += f"- Servizi: {stats['servizi']}\n"
            msg += f"- Credenziali: {stats['credenziali']}\n"
            if stats['errori'] > 0:
                msg += f"- Errori: {stats['errori']}"
            
            return True, msg, stats
            
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
    
    def _import_from_excel(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa dati da file Excel"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.fillna('')  # Sostituisci NaN con stringhe vuote
            
            stats = {'clienti': 0, 'servizi': 0, 'credenziali': 0, 'errori': 0}
            clienti_map = {}  # nome_cliente -> id
            servizi_map = {}  # (cliente_id, nome_servizio) -> id
            
            for _, row in df.iterrows():
                try:
                    cliente_nome = str(row.get('Cliente', '')).strip()
                    if not cliente_nome:
                        continue
                    
                    # Crea o recupera cliente
                    if cliente_nome not in clienti_map:
                        # Verifica se il cliente esiste già
                        clienti_esistenti = Cliente.get_all(self.db)
                        cliente_esistente = next((c for c in clienti_esistenti if c.nome == cliente_nome), None)
                        
                        if cliente_esistente:
                            clienti_map[cliente_nome] = cliente_esistente.id
                        else:
                            cliente_id = Cliente.create(
                                self.db,
                                nome=cliente_nome,
                                descrizione=str(row.get('Cliente_Descrizione', '')).strip(),
                                vpn_exe_path=str(row.get('VPN_EXE', '')).strip(),
                                vpn_windows_name=str(row.get('VPN_Windows', '')).strip()
                            )
                            clienti_map[cliente_nome] = cliente_id
                            stats['clienti'] += 1
                    
                    cliente_id = clienti_map[cliente_nome]
                    
                    # Crea servizio se presente
                    servizio_nome = str(row.get('Servizio', '')).strip()
                    if servizio_nome:
                        servizio_key = (cliente_id, servizio_nome)
                        
                        if servizio_key not in servizi_map:
                            # Verifica se il servizio esiste già
                            servizi_esistenti = Servizio.get_by_cliente(self.db, cliente_id)
                            servizio_esistente = next((s for s in servizi_esistenti if s.nome == servizio_nome), None)
                            
                            if servizio_esistente:
                                servizi_map[servizio_key] = servizio_esistente.id
                            else:
                                servizio_tipo = str(row.get('Servizio_Tipo', 'Altro')).strip()
                                if servizio_tipo not in Servizio.TIPI_DISPONIBILI:
                                    servizio_tipo = 'Altro'
                                
                                servizio_id = Servizio.create(
                                    self.db,
                                    cliente_id=cliente_id,
                                    nome=servizio_nome,
                                    tipo=servizio_tipo,
                                    descrizione=str(row.get('Servizio_Descrizione', '')).strip(),
                                    link=str(row.get('Servizio_Link', '')).strip()
                                )
                                servizi_map[servizio_key] = servizio_id
                                stats['servizi'] += 1
                        
                        servizio_id = servizi_map[servizio_key]
                        
                        # Crea credenziale se presente
                        username = str(row.get('Username', '')).strip()
                        password = str(row.get('Password', '')).strip()
                        
                        # Se Username vuoto ma ci sono Dominio/Utente, costruisci username
                        if not username:
                            dominio = str(row.get('Dominio', '')).strip()
                            utente = str(row.get('Utente', '')).strip()
                            if dominio and utente:
                                username = f"{dominio}\\{utente}"
                            elif utente:
                                username = utente
                        
                        if username or password:
                            porta_val = row.get('Porta', '')
                            try:
                                porta = int(porta_val) if porta_val and str(porta_val).strip() else None
                            except:
                                porta = None
                            
                            rdp_config = str(row.get('RDP_Configurata', '')).strip().lower()
                            rdp_configurata = rdp_config in ['sì', 'si', 'yes', '1', 'true']
                            
                            host = str(row.get('Host', '')).strip()
                            note = str(row.get('Note', '')).strip()
                            
                            # Verifica se la credenziale esiste già
                            credenziali_esistenti = Credenziale.get_by_servizio(self.db, servizio_id)
                            credenziale_duplicata = False
                            
                            for cred in credenziali_esistenti:
                                if (cred.username == username and 
                                    cred.password == password and
                                    cred.host == host and
                                    cred.porta == porta and
                                    cred.note == note and
                                    cred.rdp_configurata == rdp_configurata):
                                    credenziale_duplicata = True
                                    break
                            
                            if not credenziale_duplicata:
                                Credenziale.create(
                                    self.db,
                                    servizio_id=servizio_id,
                                    username=username,
                                    password=password,
                                    host=host,
                                    porta=porta,
                                    note=note,
                                    rdp_configurata=rdp_configurata
                                )
                                stats['credenziali'] += 1
                
                except Exception as e:
                    stats['errori'] += 1
                    print(f"Errore riga: {e}")
                    continue
            
            msg = f"Import completato:\n"
            msg += f"- Clienti: {stats['clienti']}\n"
            msg += f"- Servizi: {stats['servizi']}\n"
            msg += f"- Credenziali: {stats['credenziali']}\n"
            if stats['errori'] > 0:
                msg += f"- Errori: {stats['errori']}"
            
            return True, msg, stats
            
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa import CSV.", {}
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
    
    def export_pm_to_csv(self, file_path: str) -> Tuple[bool, str]:
        """Esporta tutti i PM in formato CSV"""
        try:
            pms = PM.get_all(self.db)
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['Nome', 'Email', 'Telefono', 'Cellulare']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for pm in pms:
                    writer.writerow({
                        'Nome': pm.nome,
                        'Email': pm.email or '',
                        'Telefono': pm.telefono or '',
                        'Cellulare': pm.cellulare or ''
                    })
                
                return True, f"Export completato: {len(pms)} PM esportati"
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def export_pm_to_excel(self, file_path: str) -> Tuple[bool, str]:
        """Esporta tutti i PM in formato Excel"""
        try:
            import pandas as pd
            
            pms = PM.get_all(self.db)
            data = [{
                'Nome': pm.nome,
                'Email': pm.email or '',
                'Telefono': pm.telefono or '',
                'Cellulare': pm.cellulare or ''
            } for pm in pms]
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            return True, f"Export completato: {len(pms)} PM esportati"
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa export CSV."
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def import_pm_from_file(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa PM da file CSV o Excel"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            return self._import_pm_from_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self._import_pm_from_excel(file_path)
        else:
            return False, "Formato file non supportato", {}
    
    def _import_pm_from_csv(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa PM da file CSV"""
        try:
            stats = {'creati': 0, 'duplicati': 0, 'errori': 0}
            
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        nome = row.get('Nome', '').strip()
                        if not nome:
                            continue
                        
                        email = row.get('Email', '').strip()
                        telefono = row.get('Telefono', '').strip()
                        cellulare = row.get('Cellulare', '').strip()
                        
                        # Verifica duplicato
                        pms_esistenti = PM.get_all(self.db)
                        duplicato = False
                        
                        for pm in pms_esistenti:
                            if (pm.nome == nome and
                                pm.email == email and
                                pm.telefono == telefono and
                                pm.cellulare == cellulare):
                                duplicato = True
                                stats['duplicati'] += 1
                                break
                        
                        if not duplicato:
                            PM.create(self.db, nome, email, telefono, cellulare)
                            stats['creati'] += 1
                    
                    except Exception as e:
                        stats['errori'] += 1
                        print(f"Errore riga: {e}")
            
            msg = f"Import completato:\n- Creati: {stats['creati']}\n- Duplicati: {stats['duplicati']}"
            if stats['errori'] > 0:
                msg += f"\n- Errori: {stats['errori']}"
            
            return True, msg, stats
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
    
    def _import_pm_from_excel(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa PM da file Excel"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.fillna('')
            
            stats = {'creati': 0, 'duplicati': 0, 'errori': 0}
            
            for _, row in df.iterrows():
                try:
                    nome = str(row.get('Nome', '')).strip()
                    if not nome:
                        continue
                    
                    email = str(row.get('Email', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    cellulare = str(row.get('Cellulare', '')).strip()
                    
                    # Verifica duplicato
                    pms_esistenti = PM.get_all(self.db)
                    duplicato = False
                    
                    for pm in pms_esistenti:
                        if (pm.nome == nome and
                            pm.email == email and
                            pm.telefono == telefono and
                            pm.cellulare == cellulare):
                            duplicato = True
                            stats['duplicati'] += 1
                            break
                    
                    if not duplicato:
                        PM.create(self.db, nome, email, telefono, cellulare)
                        stats['creati'] += 1
                
                except Exception as e:
                    stats['errori'] += 1
                    print(f"Errore riga: {e}")
            
            msg = f"Import completato:\n- Creati: {stats['creati']}\n- Duplicati: {stats['duplicati']}"
            if stats['errori'] > 0:
                msg += f"\n- Errori: {stats['errori']}"
            
            return True, msg, stats
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa import CSV.", {}
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
    
    def export_consulenti_to_csv(self, file_path: str) -> Tuple[bool, str]:
        """Esporta tutti i Consulenti in formato CSV"""
        try:
            consulenti = Consulente.get_all(self.db)
            
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['Nome', 'Email', 'Telefono', 'Cellulare', 'Competenza']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for consulente in consulenti:
                    writer.writerow({
                        'Nome': consulente.nome,
                        'Email': consulente.email or '',
                        'Telefono': consulente.telefono or '',
                        'Cellulare': consulente.cellulare or '',
                        'Competenza': consulente.competenza or ''
                    })
                
                return True, f"Export completato: {len(consulenti)} Consulenti esportati"
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def export_consulenti_to_excel(self, file_path: str) -> Tuple[bool, str]:
        """Esporta tutti i Consulenti in formato Excel"""
        try:
            import pandas as pd
            
            consulenti = Consulente.get_all(self.db)
            data = [{
                'Nome': c.nome,
                'Email': c.email or '',
                'Telefono': c.telefono or '',
                'Cellulare': c.cellulare or '',
                'Competenza': c.competenza or ''
            } for c in consulenti]
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            return True, f"Export completato: {len(consulenti)} Consulenti esportati"
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa export CSV."
        except Exception as e:
            return False, f"Errore durante l'export: {str(e)}"
    
    def import_consulenti_from_file(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa Consulenti da file CSV o Excel"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            return self._import_consulenti_from_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self._import_consulenti_from_excel(file_path)
        else:
            return False, "Formato file non supportato", {}
    
    def _import_consulenti_from_csv(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa Consulenti da file CSV"""
        try:
            stats = {'creati': 0, 'duplicati': 0, 'errori': 0}
            
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        nome = row.get('Nome', '').strip()
                        if not nome:
                            continue
                        
                        email = row.get('Email', '').strip()
                        telefono = row.get('Telefono', '').strip()
                        cellulare = row.get('Cellulare', '').strip()
                        competenza = row.get('Competenza', '').strip()
                        
                        # Verifica duplicato
                        consulenti_esistenti = Consulente.get_all(self.db)
                        duplicato = False
                        
                        for cons in consulenti_esistenti:
                            if (cons.nome == nome and
                                cons.email == email and
                                cons.telefono == telefono and
                                cons.cellulare == cellulare and
                                cons.competenza == competenza):
                                duplicato = True
                                stats['duplicati'] += 1
                                break
                        
                        if not duplicato:
                            Consulente.create(self.db, nome, email, telefono, cellulare, competenza)
                            stats['creati'] += 1
                    
                    except Exception as e:
                        stats['errori'] += 1
                        print(f"Errore riga: {e}")
            
            msg = f"Import completato:\n- Creati: {stats['creati']}\n- Duplicati: {stats['duplicati']}"
            if stats['errori'] > 0:
                msg += f"\n- Errori: {stats['errori']}"
            
            return True, msg, stats
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
    
    def _import_consulenti_from_excel(self, file_path: str) -> Tuple[bool, str, Dict[str, int]]:
        """Importa Consulenti da file Excel"""
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path, engine='openpyxl')
            df = df.fillna('')
            
            stats = {'creati': 0, 'duplicati': 0, 'errori': 0}
            
            for _, row in df.iterrows():
                try:
                    nome = str(row.get('Nome', '')).strip()
                    if not nome:
                        continue
                    
                    email = str(row.get('Email', '')).strip()
                    telefono = str(row.get('Telefono', '')).strip()
                    cellulare = str(row.get('Cellulare', '')).strip()
                    competenza = str(row.get('Competenza', '')).strip()
                    
                    # Verifica duplicato
                    consulenti_esistenti = Consulente.get_all(self.db)
                    duplicato = False
                    
                    for cons in consulenti_esistenti:
                        if (cons.nome == nome and
                            cons.email == email and
                            cons.telefono == telefono and
                            cons.cellulare == cellulare and
                            cons.competenza == competenza):
                            duplicato = True
                            stats['duplicati'] += 1
                            break
                    
                    if not duplicato:
                        Consulente.create(self.db, nome, email, telefono, cellulare, competenza)
                        stats['creati'] += 1
                
                except Exception as e:
                    stats['errori'] += 1
                    print(f"Errore riga: {e}")
            
            msg = f"Import completato:\n- Creati: {stats['creati']}\n- Duplicati: {stats['duplicati']}"
            if stats['errori'] > 0:
                msg += f"\n- Errori: {stats['errori']}"
            
            return True, msg, stats
        except ImportError:
            return False, "Errore: pandas e openpyxl non installati. Usa import CSV.", {}
        except Exception as e:
            return False, f"Errore durante l'import: {str(e)}", {}
