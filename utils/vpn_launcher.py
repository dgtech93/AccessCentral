"""
Utility per lanciare VPN (EXE e Windows native)
"""

import subprocess
import os
from typing import Tuple


class VPNLauncher:
    """Gestisce il lancio di VPN"""
    
    def __init__(self):
        pass
    
    def lancia_vpn_exe(self, exe_path: str) -> Tuple[bool, str]:
        """
        Lancia un file EXE VPN
        
        Args:
            exe_path: Percorso del file .exe
            
        Returns:
            Tuple (successo, messaggio)
        """
        if not exe_path or not os.path.exists(exe_path):
            return False, f"File VPN non trovato: {exe_path}"
        
        if not exe_path.lower().endswith('.exe'):
            return False, "Il file deve essere un eseguibile (.exe)"
        
        try:
            # Lancia il processo in modo asincrono con finestra nascosta
            startupinfo = None
            if hasattr(subprocess, 'STARTUPINFO'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.Popen(
                [exe_path], 
                shell=True,
                startupinfo=startupinfo
            )
            return True, f"VPN lanciata con successo: {os.path.basename(exe_path)}"
        
        except Exception as e:
            return False, f"Errore nel lancio della VPN: {str(e)}"
    
    def connetti_vpn_windows(self, vpn_name: str) -> Tuple[bool, str]:
        """
        Connette a una VPN configurata in Windows
        
        Args:
            vpn_name: Nome della connessione VPN in Windows
            
        Returns:
            Tuple (successo, messaggio)
        """
        if not vpn_name or not vpn_name.strip():
            return False, "Nome VPN non specificato"
        
        try:
            # Usa rasdial per connettersi alla VPN
            # Comando: rasdial "Nome VPN"
            result = subprocess.run(
                ['rasdial', vpn_name],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            # Controlla se la connessione è riuscita
            if result.returncode == 0 or "già connesso" in result.stdout.lower() or "already connected" in result.stdout.lower():
                return True, f"Connesso alla VPN '{vpn_name}'"
            else:
                # Estrae il messaggio di errore
                error_msg = result.stdout if result.stdout else result.stderr
                if not error_msg:
                    error_msg = f"Codice errore: {result.returncode}"
                return False, f"Errore connessione VPN: {error_msg}"
        
        except subprocess.TimeoutExpired:
            return False, "Timeout: la connessione VPN ha impiegato troppo tempo"
        
        except FileNotFoundError:
            return False, "Comando 'rasdial' non trovato. Verifica che la VPN sia configurata in Windows"
        
        except Exception as e:
            return False, f"Errore nella connessione VPN: {str(e)}"
    
    def disconnetti_vpn_windows(self, vpn_name: str) -> Tuple[bool, str]:
        """
        Disconnette una VPN Windows
        
        Args:
            vpn_name: Nome della connessione VPN
            
        Returns:
            Tuple (successo, messaggio)
        """
        if not vpn_name or not vpn_name.strip():
            return False, "Nome VPN non specificato"
        
        try:
            # Comando: rasdial "Nome VPN" /disconnect
            result = subprocess.run(
                ['rasdial', vpn_name, '/disconnect'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, f"VPN '{vpn_name}' disconnessa"
            else:
                error_msg = result.stdout if result.stdout else result.stderr
                return False, f"Errore disconnessione VPN: {error_msg}"
        
        except Exception as e:
            return False, f"Errore nella disconnessione VPN: {str(e)}"
    
    def ottieni_vpn_disponibili(self) -> Tuple[bool, list]:
        """
        Ottiene la lista delle VPN configurate in Windows
        
        Returns:
            Tuple (successo, lista_vpn)
        """
        try:
            # Usa PowerShell per ottenere le connessioni VPN
            ps_command = "Get-VpnConnection | Select-Object -ExpandProperty Name"
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            if result.returncode == 0 and result.stdout:
                vpn_list = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                return True, vpn_list
            else:
                return False, []
        
        except subprocess.TimeoutExpired:
            return False, []
        except FileNotFoundError:
            return False, []
        except Exception as e:
            print(f"Errore nel recupero VPN: {e}")
            return False, []
    
    def verifica_stato_vpn(self, vpn_name: str) -> Tuple[bool, str]:
        """
        Verifica lo stato di una VPN Windows
        
        Args:
            vpn_name: Nome della connessione VPN
            
        Returns:
            Tuple (connesso, stato)
        """
        try:
            ps_command = f"Get-VpnConnection -Name '{vpn_name}' | Select-Object -ExpandProperty ConnectionStatus"
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            if result.returncode == 0 and result.stdout:
                stato = result.stdout.strip()
                connesso = "Connected" in stato or "Connesso" in stato
                return connesso, stato
            else:
                return False, "Sconosciuto"
        
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception:
            return False, "Errore"
