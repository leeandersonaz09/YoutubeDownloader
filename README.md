# Youtubedownloader
 
Baixe o ffmpeg e descompacte na raiz do disco C ou qualquer outro local desejado

Mude o caminho da pasta no codigo para onde vc extraiu caso queira usar o script ao inves do exe           
# Caminho alternativo ou erro, se necessário
ffmpeg_location = r"C:\Program Files (x86)\YoutubeVideoDownloader\ffmpeg\bin" # MUDE ESSA LINHA SE QUSIER USAR O SCRIPT PARA O DISCO C OU QUALQUER DIRETÓRIO QUE TIVER EXTRAIDO A PASTA DO FFMPEG

Caso queria criar um exe e usar no pc sem criar instalador basta fazer o processo acima e criar o exe 
Caso queira criar um instalador deixe como está e baixe o inno setup compiler e execute o seguinte script YoutubeVideoDownloader Inno script que esta na pasta do github

# Mude as opções para sua preferencia 
Source: "C:\ffmpeg\*" defina o diretorio onde vc extraiu o ffmpeg
# Caminho do Icon
SetupIconFile=C:\Users\Lee Brasil\Desktop\Python\seu_icone.ico   