; Script generato con Inno Setup
; AccessCentral - Installer Windows

#define MyAppName "AccessCentral"
#define MyAppVersion "1.3.1"
#define MyAppPublisher "DiegoG Corporate"
#define MyAppExeName "CredenzialiSuite.exe"
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
OutputBaseFilename=CredenzialiSuite_Setup
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
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "credenziali_suite.db"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\credenziali_suite.db"
Type: files; Name: "{app}\credenziali_suite.db-journal"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
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
  
  // Chiede conferma per eliminare il database
  MsgText := 'Vuoi eliminare anche il database con tutte le credenziali salvate?' + #13#10 + #13#10 +
             'Seleziona:' + #13#10 +
             '• SI per eliminare tutto (il database non sarà recuperabile)' + #13#10 +
             '• NO per mantenere il database';
             
  if MsgBox(MsgText, mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
  begin
    DeleteDatabase := True;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Elimina il database se richiesto
    if DeleteDatabase then
    begin
      DeleteFile(ExpandConstant('{app}\credenziali_suite.db'));
      DeleteFile(ExpandConstant('{app}\credenziali_suite.db-journal'));
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Operazioni post-installazione
  end;
end;
