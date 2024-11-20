import os
import openpyxl
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
import sys

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    # Obter as dimensões da tela
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()

    # Calcular as coordenadas para centralizar a janela
    pos_x = (tela_largura - largura) // 2
    pos_y = (tela_altura - altura) // 2

    # Definir a posição da janela
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


# Funções para download (não alteradas)
def baixar_mp3_yt_dlp(video_url, pasta_destino, janela_loading, label_status):
    try:
        print(f"Baixando MP3: {video_url}")
        
        # Determina o caminho do FFmpeg relativo ao diretório do script ou exe
        ffmpeg_path = os.path.join(os.path.dirname(sys.executable), 'ffmpeg', 'bin')
        if os.path.exists(ffmpeg_path):
            ffmpeg_location = ffmpeg_path
        else:
            # Caminho alternativo ou erro, se necessário
            ffmpeg_location = r"C:\Program Files (x86)\YoutubeVideoDownloader\ffmpeg\bin"

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_location,  # Caminho dinâmico para FFmpeg
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        label_status.config(text=f"Download concluído: {video_url}")
        janela_loading.update()  # Atualiza a janela de carregamento
        print("Download concluído!")
    except Exception as e:
        print(f"Erro ao baixar {video_url}: {e}")
        label_status.config(text=f"Erro ao baixar: {video_url}")
        janela_loading.update()

def baixar_mp4_yt_dlp(video_url, pasta_destino, qualidade, janela_loading, label_status):
    try:
        print(f"Baixando MP4: {video_url} na qualidade {qualidade}")
        qualidade_format = {
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "4K": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
        }
        format_string = qualidade_format.get(qualidade, "bestvideo+bestaudio/best")
        
        ydl_opts = {
            'format': format_string,
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'ffmpeg_location': os.path.join(os.path.dirname(sys.executable), 'ffmpeg', 'bin'),  # Caminho do FFmpeg
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        label_status.config(text=f"Download concluído: {video_url}")
        janela_loading.update()  # Atualiza a janela de carregamento
        print("Download concluído!")
    except Exception as e:
        print(f"Erro ao baixar {video_url}: {e}")
        label_status.config(text=f"Erro ao baixar: {video_url}")
        janela_loading.update()

def ler_lista_excel(caminho_excel, coluna_urls):
    try:
        wb = openpyxl.load_workbook(caminho_excel)
        sheet = wb.active
        urls = [row[0] for row in sheet.iter_rows(min_col=coluna_urls, max_col=coluna_urls, values_only=True) if row[0]]
        return urls
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return []

# Função para selecionar arquivo Excel
def selecionar_arquivo_excel():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo Excel",
        filetypes=[("Arquivos Excel", "*.xlsx")])
    entrada_arquivo.delete(0, tk.END)
    entrada_arquivo.insert(0, caminho)

# Função para selecionar pasta destino
def selecionar_pasta_destino():
    caminho = filedialog.askdirectory(title="Selecione o local para salvar os arquivos")
    if caminho:
        caminho_pasta_final = os.path.join(caminho, "ArquivosConvertidos")
        if not os.path.exists(caminho_pasta_final):
            os.makedirs(caminho_pasta_final)
        entrada_pasta.delete(0, tk.END)
        entrada_pasta.insert(0, caminho_pasta_final)
        messagebox.showinfo("Pasta Criada", f"Os arquivos serão salvos em: {caminho_pasta_final}")

# Função para iniciar a conversão
def iniciar_conversao():
    caminho_excel = entrada_arquivo.get()
    pasta_destino = entrada_pasta.get()
    coluna_urls = 1  # Coluna de URLs no Excel
    qualidade_video = menu_qualidade.get()

    # Validações de entrada
    if not caminho_excel or not os.path.exists(caminho_excel):
        messagebox.showerror("Erro", "Selecione um arquivo Excel válido.")
        return
    
    if not pasta_destino or not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    urls = ler_lista_excel(caminho_excel, coluna_urls)
    if not urls:
        messagebox.showerror("Erro", "Nenhuma URL encontrada no arquivo Excel.")
        return

    # Criar a janela de "Aguarde"
    janela_loading = tk.Toplevel()
    janela_loading.title("Aguarde")
    janela_loading.geometry("400x150")
    janela_loading.resizable(False, False)
    janela_loading.config(bg="#f0f0f0")  # Cor de fundo suave
    tk.Label(janela_loading, text="Aguarde enquanto o download é realizado...", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    label_status = tk.Label(janela_loading, text="", font=("Arial", 10), bg="#f0f0f0")
    label_status.pack(pady=10)

    # Centralizar a janela de loading
    centralizar_janela(janela_loading, 400, 150)

    # Garantir que a janela "Aguarde" fique no topo
    janela_loading.grab_set()  # Captura os eventos de input para a janela de "Aguarde"
    janela_loading.transient(janela)  # Faz a janela ser "filha" da janela principal
    janela_loading.focus_set()  # Garante que a janela de "Aguarde" tenha foco

    # Função para cancelar o download
    def cancelar_download():
        janela_loading.destroy()
        messagebox.showinfo("Cancelado", "O processo de download foi cancelado.")

    # Botão de cancelamento
    botao_cancelar = ttk.Button(janela_loading, text="Cancelar", command=cancelar_download)
    botao_cancelar.pack(pady=10)

    # Iniciar os downloads
    for url in urls:
        if variavel_opcao.get() == "mp3":
            label_status.config(text=f"Baixando MP3: {url}")
            janela_loading.update()
            baixar_mp3_yt_dlp(url, pasta_destino, janela_loading, label_status)
        elif variavel_opcao.get() == "video":
            label_status.config(text=f"Baixando Vídeo: {url}")
            janela_loading.update()
            baixar_mp4_yt_dlp(url, pasta_destino, qualidade_video, janela_loading, label_status)

    messagebox.showinfo("Concluído", "Processo de download concluído!")
    janela_loading.destroy()  # Fecha a janela de "Aguarde" após terminar

# Criar a interface gráfica
janela = ThemedTk()  # Usar a janela com tema
janela.title("Conversor de Vídeos")
janela.geometry("500x400")
janela.set_theme("arc")  # Definir o tema

# Centralizar a janela principal
centralizar_janela(janela, 500, 400)

# Tornar as colunas e linhas responsivas
janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)
janela.grid_rowconfigure(5, weight=1)
janela.grid_columnconfigure(1, weight=1)

# Estilo de botões com bordas arredondadas
style = ttk.Style()
style.configure(
    "Rounded.TButton",
    font=("Arial", 11),  # Tamanho da fonte
    padding=(6, 6),  # Reduzir padding interno
    background="#4CAF50",  # Fundo verde
    foreground="white",    # Texto branco
    relief="flat"
)
style.map(
    "Rounded.TButton",
    background=[('active', '#45a049')],  # Fundo verde claro ao pressionar
    foreground=[('disabled', 'gray')]   # Texto cinza se desabilitado
)

# Simulação de borda arredondada ao redor do botão
style.element_create("Rounded.Button", "from", "clam")
style.layout("Rounded.TButton", [
    ("Rounded.Button", {
        "sticky": "nswe", 
        "children": [
            ("Button.focus", {
                "children": [
                    ("Button.padding", {
                        "children": [
                            ("Button.label", {"sticky": "nswe"})
                        ]
                    })
                ]
            })
        ]
    })
])
# Layout da interface principal
tk.Label(janela, text="Arquivo Excel:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
entrada_arquivo = ttk.Entry(janela, width=50)
entrada_arquivo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(janela, text="Selecionar", style="Rounded.TButton", command=selecionar_arquivo_excel).grid(row=0, column=2, padx=10, pady=5)

tk.Label(janela, text="Pasta de Destino:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
entrada_pasta = ttk.Entry(janela, width=50)
entrada_pasta.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
ttk.Button(janela, text="Selecionar", style="Rounded.TButton", command=selecionar_pasta_destino).grid(row=1, column=2, padx=10, pady=5)

tk.Label(janela, text="Qualidade do Vídeo:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
menu_qualidade = ttk.Combobox(janela, values=["720p", "1080p", "4K"], state="readonly", width=48)
menu_qualidade.set("1080p")
menu_qualidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

tk.Label(janela, text="Escolha o tipo de arquivo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
variavel_opcao = ttk.Combobox(janela, values=["mp3", "video"], state="readonly", width=48)
variavel_opcao.set("mp3")
variavel_opcao.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Botão de iniciar conversão
ttk.Button(janela, text="Iniciar Conversão", style="Rounded.TButton", command=iniciar_conversao).grid(row=4, column=0, columnspan=3, pady=20)
# Informações do desenvolvedor
tk.Label(janela, text="Made by Lee Brasil 71992616055", font=("Arial", 8)).grid(row=6, column=0, columnspan=3, pady=10)

# Rodar a interface
janela.mainloop()
