"""
Script per creare l'installer di AccessCentral v2.2
Genera un eseguibile standalone per Windows con PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

VERSION = "2.2.1"
APP_NAME = "AccessCentral"

def cleanup_build_folders():
    """Pulisce le cartelle di build precedenti"""
    print("🧹 Pulizia cartelle build precedenti...")
    folders_to_clean = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  ✓ Rimossa cartella: {folder}")
            except Exception as e:
                print(f"  ✗ Errore rimozione {folder}: {e}")
    
    # Rimuovi file .spec vecchi
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != f'{APP_NAME}.spec':
            try:
                spec_file.unlink()
                print(f"  ✓ Rimosso file: {spec_file}")
            except Exception as e:
                print(f"  ✗ Errore rimozione {spec_file}: {e}")

def check_dependencies():
    """Verifica che tutte le dipendenze siano installate"""
    print("\n📦 Verifica dipendenze...")
    
    dependencies = {
        'PyQt5': 'PyQt5',
        'cryptography': 'cryptography',
        'PyInstaller': 'PyInstaller'
    }
    
    missing = []
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package} installato")
        except ImportError:
            print(f"  ✗ {package} NON installato")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Dipendenze mancanti: {', '.join(missing)}")
        print("   Installale con: pip install " + " ".join(missing))
        return False
    
    return True

def create_spec_file():
    """Crea il file .spec per PyInstaller"""
    print("\n📝 Creazione file .spec...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),  # Include icona se esiste
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.backends',
        'cryptography.fernet',
        'pandas',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Non mostrare console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Icona applicazione
    version_file='version_info.txt',  # File versione Windows
)
'''
    
    with open(f'{APP_NAME}.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"  ✓ Creato file: {APP_NAME}.spec")

def create_version_file():
    """Crea il file di versione per Windows"""
    print("\n📄 Creazione file versione Windows...")
    
    version_content = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AccessCentral Development'),
        StringStruct(u'FileDescription', u'Gestione Credenziali e Accessi'),
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2026'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print("  ✓ Creato file: version_info.txt")

def build_executable():
    """Esegue PyInstaller per creare l'eseguibile"""
    print("\n🔨 Build eseguibile con PyInstaller...")
    print("   Questo potrebbe richiedere alcuni minuti...\n")
    
    try:
        # Esegui PyInstaller
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', f'{APP_NAME}.spec', '--clean'],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("  ✓ Build completata con successo!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Errore durante build:")
        print(e.stderr)
        return False

def create_installer_package():
    """Crea la struttura finale dell'installer"""
    print("\n📦 Creazione package installer...")
    
    installer_dir = Path(f'installer_{APP_NAME}_v{VERSION}')
    
    # Crea directory installer
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    # Copia eseguibile
    exe_path = Path('dist') / f'{APP_NAME}.exe'
    if exe_path.exists():
        shutil.copy(exe_path, installer_dir / f'{APP_NAME}.exe')
        print(f"  ✓ Copiato: {APP_NAME}.exe")
    else:
        print(f"  ✗ Eseguibile non trovato: {exe_path}")
        return False
    
    # Copia README
    if Path('README.md').exists():
        shutil.copy('README.md', installer_dir / 'README.md')
        print("  ✓ Copiato: README.md")
    
    # Copia Release Notes
    if Path('RELEASE_NOTES_v2.0.md').exists():
        shutil.copy('RELEASE_NOTES_v2.0.md', installer_dir / 'RELEASE_NOTES_v2.0.md')
        print("  ✓ Copiato: RELEASE_NOTES_v2.0.md")
    
    # Crea file ISTRUZIONI
    create_instructions_file(installer_dir)
    
    # Crea script di avvio
    create_launcher_script(installer_dir)
    
    print(f"\n✅ Package installer creato in: {installer_dir}")
    print(f"   Dimensione eseguibile: {get_file_size(exe_path)}")
    
    return True

def create_instructions_file(installer_dir):
    """Crea file istruzioni per l'utente"""
    instructions = f"""
╔══════════════════════════════════════════════════════════════╗
║           AccessCentral v{VERSION} - ISTRUZIONI                ║
╚══════════════════════════════════════════════════════════════╝

📦 INSTALLAZIONE
────────────────────────────────────────────────────────────────

1. Copia la cartella "installer_AccessCentral_v{VERSION}" 
   in una posizione permanente sul tuo PC
   
   Esempio: C:\\Programmi\\AccessCentral\\

2. Esegui AccessCentral.exe per avviare l'applicazione

3. Al primo avvio ti verrà chiesto di:
   - Impostare una Master Password (minimo 6 caratteri)
   - Salvare il Codice di Recupero (IMPORTANTE!)


⚠️  PRIMA CONFIGURAZIONE
────────────────────────────────────────────────────────────────

🔐 Master Password:
   - Scegli una password forte e memorabile
   - Verrà richiesta ad ogni avvio
   - Non dimenticarla!

🔑 Codice di Recupero:
   - Verrà mostrato SOLO UNA VOLTA durante setup
   - SALVALO in un posto sicuro (es: password manager)
   - Necessario se dimentichi la password
   - Formato: XXXX-XXXX-XXXX-XXXX


💾 DATABASE E FILE
────────────────────────────────────────────────────────────────

L'applicazione crea questi file nella stessa cartella:

📁 credenziali_suite.db
   Database con tutte le credenziali (criptate)
   
📁 security_config.json
   Configurazione sicurezza (hash master password)
   
📁 backup_config.json
   Configurazione backup automatico
   
📁 config.json
   Preferenze UI (tema selezionato)
   
📁 backups/
   Directory backup automatici del database


🔒 SICUREZZA
────────────────────────────────────────────────────────────────

✓ Tutte le password sono criptate con AES-256
✓ Master password protetta con SHA-256
✓ Derivazione chiavi con PBKDF2 (100.000 iterazioni)
✓ Backup automatico configurabile
✓ Codice recupero per emergenze


🆘 SUPPORTO
────────────────────────────────────────────────────────────────

📖 Documentazione completa: Vedi README.md
📋 Release Notes: Vedi RELEASE_NOTES_v2.0.md
🐛 Bug Report: https://github.com/dgtech93/AccessCentral/issues
📧 Contatti: Vedi repository GitHub


⚙️  REQUISITI SISTEMA
────────────────────────────────────────────────────────────────

• Windows 10 / 11 (64-bit)
• ~100 MB spazio disco
• Nessuna installazione Python richiesta (eseguibile standalone)


🔄 AGGIORNAMENTI
────────────────────────────────────────────────────────────────

Per aggiornare:
1. Fai backup del file credenziali_suite.db
2. Scarica nuova versione
3. Sostituisci solo AccessCentral.exe
4. I tuoi dati rimangono intatti


📝 NOTE IMPORTANTI
────────────────────────────────────────────────────────────────

⚠️  Fai backup regolari di credenziali_suite.db
⚠️  Non condividere security_config.json
⚠️  Salva il codice di recupero in un posto sicuro
✓  Usa backup automatico (Menu Backup → Gestisci Backup)


════════════════════════════════════════════════════════════════

Grazie per aver scelto AccessCentral! 🔐
Versione {VERSION} - Febbraio 2026

════════════════════════════════════════════════════════════════
"""
    
    with open(installer_dir / 'ISTRUZIONI.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("  ✓ Creato: ISTRUZIONI.txt")

def create_launcher_script(installer_dir):
    """Crea script batch per avvio rapido"""
    launcher = f"""@echo off
title AccessCentral v{VERSION}
cd /d "%~dp0"
start "" "{APP_NAME}.exe"
"""
    
    with open(installer_dir / 'Avvia_AccessCentral.bat', 'w', encoding='utf-8') as f:
        f.write(launcher)
    
    print("  ✓ Creato: Avvia_AccessCentral.bat")

def get_file_size(file_path):
    """Restituisce dimensione file formattata"""
    size_bytes = os.path.getsize(file_path)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"

def create_zip_archive():
    """Crea archivio ZIP dell'installer"""
    print("\n📦 Creazione archivio ZIP...")
    
    installer_dir = f'installer_{APP_NAME}_v{VERSION}'
    zip_name = f'{APP_NAME}_v{VERSION}_Windows_Installer'
    
    try:
        shutil.make_archive(zip_name, 'zip', '.', installer_dir)
        zip_path = Path(f'{zip_name}.zip')
        
        if zip_path.exists():
            print(f"  ✓ Creato: {zip_name}.zip")
            print(f"  Dimensione: {get_file_size(zip_path)}")
            return True
    except Exception as e:
        print(f"  ✗ Errore creazione ZIP: {e}")
        return False

def main():
    """Funzione principale"""
    print("╔══════════════════════════════════════════════════════════╗")
    print(f"║  AccessCentral v{VERSION} - Build Installer             ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # 1. Verifica dipendenze
    if not check_dependencies():
        return 1
    
    # 2. Pulizia
    cleanup_build_folders()
    
    # 3. Crea file .spec
    create_spec_file()
    
    # 4. Crea file versione Windows
    create_version_file()
    
    # 5. Build eseguibile
    if not build_executable():
        print("\n❌ Build fallita!")
        return 1
    
    # 6. Crea package installer
    if not create_installer_package():
        print("\n❌ Creazione package fallita!")
        return 1
    
    # 7. Crea archivio ZIP
    create_zip_archive()
    
    print("\n" + "="*60)
    print("✅ BUILD COMPLETATA CON SUCCESSO!")
    print("="*60)
    print(f"\n📦 Package: installer_{APP_NAME}_v{VERSION}/")
    print(f"📦 Archivio: {APP_NAME}_v{VERSION}_Windows_Installer.zip")
    print("\n🚀 Pronto per la distribuzione!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
