"""
Utility per lanciare connessioni RDP
"""

import subprocess
import os
import tempfile
from typing import Tuple, Optional


class RDPLauncher:
    """Gestisce il lancio di connessioni Remote Desktop (RDP)"""
    
    def __init__(self):
        self.mstsc_path = "mstsc.exe"  # Client RDP di Windows
    
    def connetti_rdp(self, host: str, username: str = "", password: str = "",
                    porta: Optional[int] = None) -> Tuple[bool, str]:
        """
        Apre una connessione RDP
        
        Args:
            host: Indirizzo IP o hostname
            username: Nome utente (opzionale)
            password: Password (opzionale)
            porta: Porta RDP (default: 3389)
            
        Returns:
            Tuple (successo, messaggio)
        """
        if not host or not host.strip():
            return False, "Host non specificato"
        
        host = host.strip()
        porta_rdp = porta if porta else 3389
        
        # Costruisce l'indirizzo completo
        if porta_rdp != 3389:
            indirizzo_completo = f"{host}:{porta_rdp}"
        else:
            indirizzo_completo = host
        
        try:
            # Se abbiamo username e password, usa cmdkey per salvare le credenziali
            # e poi crea un file .rdp temporaneo
            if username and password:
                # Salva le credenziali nel Windows Credential Manager
                target = f"TERMSRV/{host}"
                cmdkey_command = f'cmdkey /generic:{target} /user:{username} /pass:{password}'
                subprocess.run(cmdkey_command, shell=True, capture_output=True)
                
                rdp_file = self.crea_file_rdp(host, username, password, porta_rdp)
                
                # Lancia mstsc con il file .rdp
                subprocess.Popen([self.mstsc_path, rdp_file], shell=True)
                
                return True, f"Connessione RDP lanciata a {indirizzo_completo} come {username}"
            
            else:
                # Lancia mstsc direttamente con l'indirizzo
                # L'utente dovrà inserire le credenziali manualmente
                command = [self.mstsc_path, '/v:' + indirizzo_completo]
                subprocess.Popen(command, shell=True)
                
                return True, f"Connessione RDP lanciata a {indirizzo_completo}"
        
        except FileNotFoundError:
            return False, "Client RDP (mstsc.exe) non trovato"
        
        except Exception as e:
            return False, f"Errore nel lancio di RDP: {str(e)}"
    
    def crea_file_rdp(self, host: str, username: str, password: str,
                     porta: int = 3389) -> str:
        """
        Crea un file .rdp temporaneo con le credenziali
        
        Args:
            host: Indirizzo host
            username: Nome utente
            password: Password
            porta: Porta RDP
            
        Returns:
            Percorso del file .rdp creato
        """
        # Contenuto del file .rdp
        rdp_content = f"""screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
winposstr:s:0,3,0,0,800,600
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:{host}:{porta}
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
username:s:{username}
"""
        
        # Crea un file temporaneo
        temp_dir = tempfile.gettempdir()
        rdp_filename = f"temp_rdp_{hash(host)}_{hash(username)}.rdp"
        rdp_path = os.path.join(temp_dir, rdp_filename)
        
        # Scrive il file
        with open(rdp_path, 'w', encoding='utf-8') as f:
            f.write(rdp_content)
        
        return rdp_path
    
    def connetti_rdp_semplice(self, host: str, porta: Optional[int] = None) -> Tuple[bool, str]:
        """
        Apre una connessione RDP semplice senza credenziali pre-compilate
        
        Args:
            host: Indirizzo IP o hostname
            porta: Porta RDP (default: 3389)
            
        Returns:
            Tuple (successo, messaggio)
        """
        return self.connetti_rdp(host, "", "", porta)
    
    def connetti_rdp_con_file(self, rdp_file_path: str) -> Tuple[bool, str]:
        """
        Apre una connessione RDP usando un file .rdp esistente
        
        Args:
            rdp_file_path: Percorso del file .rdp
            
        Returns:
            Tuple (successo, messaggio)
        """
        if not os.path.exists(rdp_file_path):
            return False, f"File .rdp non trovato: {rdp_file_path}"
        
        if not rdp_file_path.lower().endswith('.rdp'):
            return False, "Il file deve essere un file .rdp"
        
        try:
            subprocess.Popen([self.mstsc_path, rdp_file_path], shell=True)
            return True, f"Connessione RDP lanciata con file {os.path.basename(rdp_file_path)}"
        
        except Exception as e:
            return False, f"Errore nel lancio di RDP: {str(e)}"
    
    def verifica_disponibilita_rdp(self) -> bool:
        """
        Verifica se il client RDP è disponibile sul sistema
        
        Returns:
            True se mstsc.exe è disponibile
        """
        try:
            result = subprocess.run(
                ['where', 'mstsc.exe'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
