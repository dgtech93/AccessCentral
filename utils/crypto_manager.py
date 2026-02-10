"""
Gestore crittografia per proteggere le password
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class CryptoManager:
    """Gestisce la crittografia delle password"""
    
    def __init__(self):
        self.cipher = None
        self.master_password_hash = None
    
    def genera_chiave_da_password(self, password: str, salt: bytes = None) -> tuple:
        """
        Genera una chiave di crittografia da una password
        
        Args:
            password: Password master
            salt: Sale per KDF (se None, ne genera uno nuovo)
            
        Returns:
            Tupla (chiave, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def inizializza_con_password(self, password: str, salt: bytes = None) -> bytes:
        """
        Inizializza il sistema di crittografia con una password master
        
        Args:
            password: Password master
            salt: Sale (opzionale, per caricare configurazione esistente)
            
        Returns:
            Salt utilizzato
        """
        key, salt = self.genera_chiave_da_password(password, salt)
        self.cipher = Fernet(key)
        
        # Salva hash della password per verifiche future
        self.master_password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        return salt
    
    def verifica_password(self, password: str) -> bool:
        """
        Verifica se una password corrisponde alla master password
        
        Args:
            password: Password da verificare
            
        Returns:
            True se corretta
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == self.master_password_hash
    
    @staticmethod
    def calcola_hash_password(password: str) -> str:
        """
        Calcola l'hash SHA256 di una password
        
        Args:
            password: Password da cui calcolare l'hash
            
        Returns:
            Hash esadecimale della password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def genera_recovery_code() -> str:
        """
        Genera un codice di recupero casuale
        
        Returns:
            Codice di recupero (formato: XXXX-XXXX-XXXX-XXXX)
        """
        import secrets
        import string
        
        # Genera 4 gruppi di 4 caratteri alfanumerici
        chars = string.ascii_uppercase + string.digits
        gruppi = []
        for _ in range(4):
            gruppo = ''.join(secrets.choice(chars) for _ in range(4))
            gruppi.append(gruppo)
        
        return '-'.join(gruppi)
    
    def cripta(self, testo: str) -> str:
        """
        Cripta un testo
        
        Args:
            testo: Testo in chiaro
            
        Returns:
            Testo criptato (base64)
        """
        if not self.cipher:
            raise ValueError("Sistema di crittografia non inizializzato")
        
        if not testo:
            return ""
        
        encrypted = self.cipher.encrypt(testo.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decripta(self, testo_criptato: str) -> str:
        """
        Decripta un testo
        
        Args:
            testo_criptato: Testo criptato (base64)
            
        Returns:
            Testo in chiaro
        """
        if not self.cipher:
            raise ValueError("Sistema di crittografia non inizializzato")
        
        if not testo_criptato:
            return ""
        
        try:
            encrypted = base64.urlsafe_b64decode(testo_criptato.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            # Se fallisce la decrittazione, potrebbe essere già in chiaro (migrazione)
            return testo_criptato
    
    def cripta_se_necessario(self, testo: str) -> str:
        """
        Cripta solo se il testo non è già criptato
        
        Args:
            testo: Testo da criptare
            
        Returns:
            Testo criptato
        """
        if not testo:
            return ""
        
        # Prova a decriptare, se fallisce allora è in chiaro
        try:
            self.decripta(testo)
            return testo  # Già criptato
        except:
            return self.cripta(testo)  # Cripta
    
    @staticmethod
    def genera_password_sicura(lunghezza: int = 16, 
                               usa_maiuscole: bool = True,
                               usa_numeri: bool = True,
                               usa_simboli: bool = True) -> str:
        """
        Genera una password sicura casuale
        
        Args:
            lunghezza: Lunghezza della password
            usa_maiuscole: Include lettere maiuscole
            usa_numeri: Include numeri
            usa_simboli: Include simboli speciali
            
        Returns:
            Password generata
        """
        import random
        import string
        
        caratteri = string.ascii_lowercase
        
        if usa_maiuscole:
            caratteri += string.ascii_uppercase
        if usa_numeri:
            caratteri += string.digits
        if usa_simboli:
            caratteri += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Genera password assicurando almeno un carattere di ogni tipo richiesto
        password = []
        if usa_maiuscole:
            password.append(random.choice(string.ascii_uppercase))
        if usa_numeri:
            password.append(random.choice(string.digits))
        if usa_simboli:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Riempi il resto
        for _ in range(lunghezza - len(password)):
            password.append(random.choice(caratteri))
        
        # Mescola
        random.shuffle(password)
        
        return ''.join(password)
