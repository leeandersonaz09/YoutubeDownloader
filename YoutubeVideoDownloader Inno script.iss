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
; Adicionar o executável do seu aplicativo
Source: "C:\Users\Lee Brasil\Desktop\Python\dist\YoutubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion
; Adicionar o diretório ffmpeg na pasta do aplicativo
Source: "C:\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: recursesubdirs createallsubdirs

[Icons]
; Criar atalho na área de trabalho
Name: "{autoprograms}\Conversor de Vídeos"; Filename: "{app}\YoutubeDownloader.exe"
Name: "{userdesktop}\Conversor de Vídeos"; Filename: "{app}\YoutubeDownloader.exe"

[Run]
; Não é necessário alterar nada aqui
Filename: "{app}\YoutubeDownloader.exe"; Description: "Iniciar o Conversor de Vídeos"; Flags: nowait postinstall skipifsilent
