; Script generato con Inno Setup
; AccessCentral v2.2 - Installer Windows

#define MyAppName "AccessCentral"
#define MyAppVersion "2.2.0"
#define MyAppPublisher "DiegoG Corporate"
#define MyAppExeName "AccessCentral.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".creds"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; Informazioni base
AppId={{8B7A3C5D-2F4E-4A6B-9C8D-1E5F7A9B3C2D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer_output
OutputBaseFilename=AccessCentral_v2.2.0_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=force
CloseApplicationsFilter=*.exe

; Impostazioni per l'installer
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Eseguibile principale
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Database (solo se non esiste già)
Source: "credenziali_suite.db"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist uninsneveruninstall

; Documentazione
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "RELEASE_NOTES_v2.0.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "RELEASE_NOTES_v2.2.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "BUILD_README.md"; DestDir: "{app}"; Flags: ignoreversion

; Icona (se esiste)
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; NOTA: File di configurazione NON inclusi nell'installer
; security_config.json, backup_config.json, config.json
; Questi file vengono creati al primo avvio dall'applicazione

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; File database
Type: files; Name: "{app}\credenziali_suite.db"
Type: files; Name: "{app}\credenziali_suite.db-journal"

; File di configurazione v2.0
Type: files; Name: "{app}\security_config.json"
Type: files; Name: "{app}\backup_config.json"
Type: files; Name: "{app}\config.json"

; Directory backup
Type: filesandordirs; Name: "{app}\backups"

; File temporanei
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: files; Name: "{app}\temp_rdp_*.rdp"
Type: filesandordirs; Name: "{app}\__pycache__"

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Code]
var
  DeleteDatabase: Boolean;
  DeleteSecurityConfig: Boolean;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Controlla se l'applicazione è già in esecuzione
  if CheckForMutexes('CredenzialiSuiteAppMutex') then
  begin
    if MsgBox('AccessCentral è attualmente in esecuzione. Chiudere l''applicazione prima di continuare l''installazione?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Termina il processo se in esecuzione
      Exec('taskkill', '/F /IM AccessCentral.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Exec('taskkill', '/F /IM CredenzialiSuite.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Sleep(2000);
      Result := True;
    end
    else
      Result := False;
  end;
end;

function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
  MsgText: String;
  ProcessRunning: Boolean;
  RetryCount: Integer;
begin
  Result := True;
  DeleteDatabase := False;
  DeleteSecurityConfig := False;
  ProcessRunning := False;
  
  // Controlla se l'applicazione è in esecuzione
  if CheckForMutexes('CredenzialiSuiteAppMutex') then
  begin
    ProcessRunning := True;
    MsgText := 'AccessCentral è attualmente in esecuzione.' + #13#10 + 
               'L''applicazione verrà chiusa automaticamente per procedere con la disinstallazione.';
    MsgBox(MsgText, mbInformation, MB_OK);
  end;
  
  // Termina il processo con retry
  if ProcessRunning then
  begin
    RetryCount := 0;
    while (RetryCount < 3) do
    begin
      Exec('taskkill', '/F /IM AccessCentral.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Exec('taskkill', '/F /IM CredenzialiSuite.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Sleep(1500);
      
      // Verifica se il processo è ancora in esecuzione
      if not CheckForMutexes('CredenzialiSuiteAppMutex') then
        break;
        
      RetryCount := RetryCount + 1;
    end;
    
    // Attesa finale per assicurarsi che il processo sia terminato
    Sleep(1000);
  end;
  
  // Chiede conferma per eliminare il database e i dati
  MsgText := '⚠️ ATTENZIONE - Eliminazione Dati' + #13#10 + #13#10 +
             'Vuoi eliminare TUTTI i dati dell''applicazione?' + #13#10 + #13#10 +
             'Questo include:' + #13#10 +
             '• Database con tutte le credenziali salvate' + #13#10 +
             '• Configurazione sicurezza (master password)' + #13#10 +
             '• Tutti i backup automatici' + #13#10 +
             '• Preferenze e configurazioni' + #13#10 + #13#10 +
             'Seleziona:' + #13#10 +
             '• SI per ELIMINARE TUTTO (non recuperabile!)' + #13#10 +
             '• NO per mantenere i dati (potrai reinstallare dopo)';
             
  if MsgBox(MsgText, mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
  begin
    DeleteDatabase := True;
    DeleteSecurityConfig := True;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Elimina tutti i dati se richiesto
    if DeleteDatabase then
    begin
      // Database
      DeleteFile(ExpandConstant('{app}\credenziali_suite.db'));
      DeleteFile(ExpandConstant('{app}\credenziali_suite.db-journal'));
      
      // File di configurazione
      DeleteFile(ExpandConstant('{app}\security_config.json'));
      DeleteFile(ExpandConstant('{app}\backup_config.json'));
      DeleteFile(ExpandConstant('{app}\config.json'));
      
      // Directory backup
      DelTree(ExpandConstant('{app}\backups'), True, True, True);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  InfoMsg: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Mostra informazioni importanti dopo l'installazione
    InfoMsg := 'AccessCentral v2.0 è stato installato con successo!' + #13#10 + #13#10 +
               '🔐 PRIMA CONFIGURAZIONE:' + #13#10 +
               'Al primo avvio ti verrà chiesto di:' + #13#10 +
               '1. Impostare una Master Password (min 6 caratteri)' + #13#10 +
               '2. Salvare il Codice di Recupero (IMPORTANTE!)' + #13#10 + #13#10 +
               '⚠️ SALVA IL CODICE DI RECUPERO!' + #13#10 +
               'Verrà mostrato solo UNA volta e serve per' + #13#10 +
               'recuperare l''accesso se dimentichi la password.' + #13#10 + #13#10 +
               '💾 BACKUP AUTOMATICO:' + #13#10 +
               'Il sistema di backup automatico è attivo.' + #13#10 +
               'Configura da Menu → Backup → Gestisci Backup' + #13#10 + #13#10 +
               'Buon lavoro con AccessCentral! 🚀';
    
    MsgBox(InfoMsg, mbInformation, MB_OK);
  end;
end;
