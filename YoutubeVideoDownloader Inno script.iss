[Setup]
AppName=YoutubeVideoDownloader
AppVersion=1.0
DefaultDirName={pf}\YoutubeVideoDownloader
DefaultGroupName=YoutubeVideoDownloader
OutputDir=.
OutputBaseFilename=YoutubeVideoDownloader
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\Lee Brasil\Desktop\Python\seu_icone.ico


[Files]
; Adicionar o execut�vel do seu aplicativo
Source: "C:\Users\Lee Brasil\Desktop\Python\dist\YoutubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion
; Adicionar o diret�rio ffmpeg na pasta do aplicativo
Source: "C:\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: recursesubdirs createallsubdirs

[Icons]
; Criar atalho na �rea de trabalho
Name: "{autoprograms}\Conversor de V�deos"; Filename: "{app}\YoutubeDownloader.exe"
Name: "{userdesktop}\Conversor de V�deos"; Filename: "{app}\YoutubeDownloader.exe"

[Run]
; N�o � necess�rio alterar nada aqui
Filename: "{app}\YoutubeDownloader.exe"; Description: "Iniciar o Conversor de V�deos"; Flags: nowait postinstall skipifsilent
