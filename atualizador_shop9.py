"""
Atualizador Shop9
Programa para baixar e extrair atualizações do Shop9
Interface Gráfica
"""

import os
import sys
import subprocess
import shutil
import time
import tempfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import hashlib

# Tentar importar requests, se não estiver disponível, tentar instalar
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import requests

# URL do arquivo de configuração remoto (JSON com link de download do Shop9)
# Repositório de atualização automática: https://github.com/caioetchebehere/AtualizadorAutomatico
CONFIG_URL = "https://raw.githubusercontent.com/caioetchebehere/AtualizadorAutomatico/main/version.json"
# Alternativa: Se o arquivo tiver outro nome ou estiver em outro branch/pasta:
# CONFIG_URL = "https://raw.githubusercontent.com/caioetchebehere/AtualizadorAutomatico/main/versao.json"

TARGET_DIR = r"C:\Shop9"
TEMP_DIR = os.path.join(tempfile.gettempdir(), "shop9_update")
INSTALL_DIR = r"C:\Program Files (x86)\AtualizadorShop9"
PROGRAM_NAME = "AtualizadorShop9.exe"

def create_desktop_shortcut(target_path, shortcut_name="Atualizador Shop9.lnk", icon_path=None):
    """Cria um atalho na área de trabalho usando múltiplos métodos"""
    try:
        import ctypes
        from ctypes import wintypes
        
        # Obter caminho da área de trabalho
        CSIDL_DESKTOP = 0x0000
        SHGFP_TYPE_CURRENT = 0
        
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOP, 0, SHGFP_TYPE_CURRENT, buf)
        desktop_path = buf.value
        shortcut_path = os.path.join(desktop_path, shortcut_name)
        
        # Tentar método 1: winshell + win32com (mais confiável)
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, shortcut_name)
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = os.path.dirname(target_path)
            shortcut.IconLocation = icon_path if icon_path else target_path
            shortcut.save()
            
            return True, "Método winshell/win32com"
        except ImportError:
            pass
        except Exception:
            pass
        
        # Método 2: Usar PowerShell para criar atalho
        try:
            ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{target_path}"
$Shortcut.WorkingDirectory = "{os.path.dirname(target_path)}"
$Shortcut.IconLocation = "{icon_path if icon_path else target_path}"
$Shortcut.Save()
'''
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0 and os.path.exists(shortcut_path):
                return True, "Método PowerShell"
        except Exception:
            pass
        
        # Método 3: Usar VBScript
        try:
            vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_path}"
oLink.WorkingDirectory = "{os.path.dirname(target_path)}"
oLink.IconLocation = "{icon_path if icon_path else target_path}"
oLink.Save
'''
            vbs_file = os.path.join(tempfile.gettempdir(), "create_shortcut.vbs")
            with open(vbs_file, 'w', encoding='utf-8') as f:
                f.write(vbs_script)
            
            result = subprocess.run(
                ["cscript", "//nologo", vbs_file],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Limpar arquivo temporário
            try:
                os.remove(vbs_file)
            except:
                pass
            
            if result.returncode == 0 and os.path.exists(shortcut_path):
                return True, "Método VBScript"
        except Exception:
            pass
        
        return False, "Nenhum método funcionou"
        
    except Exception as e:
        return False, f"Erro: {str(e)}"

class AtualizadorShop9:
    def __init__(self, root):
        self.root = root
        self.root.title("Atualizador Shop9")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Centralizar janela
        self.center_window()
        
        # Variáveis
        self.is_running = False
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para iniciar")
        
        # Criar interface
        self.create_widgets()
        
        # Verificar se está instalado, se não, oferecer instalação
        self.check_installation()
        
        # Verificar privilégios de administrador
        if not self.is_admin():
            self.log_message("⚠️ AVISO: Execute como Administrador para garantir funcionamento completo")
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Atualizador Shop9", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(status_frame, text="Status:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=("Arial", 10))
        status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(progress_frame, text="Progresso:").pack(anchor=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=560)
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(anchor=tk.E, pady=(5, 0))
        
        # Área de log
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(log_frame, text="Log de Operações:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70, 
                                                  wrap=tk.WORD, state=tk.DISABLED,
                                                  font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(button_frame, text="Iniciar Atualização", 
                                       command=self.start_update, width=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.close_button = ttk.Button(button_frame, text="Fechar", 
                                       command=self.root.quit, width=20)
        self.close_button.pack(side=tk.LEFT)
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def update_status(self, status):
        """Atualiza o status"""
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def update_progress(self, value, text=None):
        """Atualiza a barra de progresso"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=text)
        else:
            self.progress_label.config(text=f"{int(value)}%")
        self.root.update_idletasks()
    
    def is_admin(self):
        """Verifica se o programa está sendo executado como administrador"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_desktop_shortcut(self, target_path, shortcut_name="Atualizador Shop9.lnk", icon_path=None):
        """Cria um atalho na área de trabalho usando múltiplos métodos"""
        return create_desktop_shortcut(target_path, shortcut_name, icon_path)
    
    def is_installed(self):
        """Verifica se o programa está instalado em C:\Program Files (x86)\AtualizadorShop9"""
        installed_path = os.path.join(INSTALL_DIR, PROGRAM_NAME)
        return os.path.exists(installed_path)
    
    def check_installation(self):
        """Verifica se o programa está instalado e oferece instalação se necessário"""
        # Se já estiver instalado e executando da pasta de instalação, não fazer nada
        if getattr(sys, 'frozen', False):
            current_exe = sys.executable
            if current_exe.lower() == os.path.join(INSTALL_DIR, PROGRAM_NAME).lower():
                return  # Já está executando da pasta de instalação
        
        # Se não estiver instalado, oferecer instalação
        if not self.is_installed():
            self.log_message("ℹ Programa não está instalado")
            if messagebox.askyesno(
                "Instalação",
                f"O Atualizador Shop9 não está instalado.\n\n"
                f"Deseja instalar em:\n{INSTALL_DIR}\n\n"
                f"Será necessário executar como Administrador."
            ):
                self.install_program()
    
    def install_program(self):
        """Instala o programa em C:\Program Files (x86)\AtualizadorShop9"""
        try:
            if not self.is_admin():
                self.log_message("⚠️ Privilégios de administrador necessários!")
                self.log_message("Solicitando elevação de privilégios...")
                
                # Reexecutar com privilégios de administrador
                import ctypes
                if getattr(sys, 'frozen', False):
                    current_exe = sys.executable
                else:
                    current_exe = os.path.abspath(__file__)
                
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", current_exe, "--install", None, 1
                )
                self.root.after(500, self.root.quit)
                return
            
            # Obter caminho do executável atual
            if getattr(sys, 'frozen', False):
                current_exe = sys.executable
            else:
                current_exe = os.path.abspath(__file__)
            
            self.log_message(f"Instalando de: {current_exe}")
            self.log_message(f"Instalando para: {INSTALL_DIR}")
            
            # Criar diretório de instalação
            os.makedirs(INSTALL_DIR, exist_ok=True)
            
            # Caminho de destino
            dest_exe = os.path.join(INSTALL_DIR, PROGRAM_NAME)
            
            # Copiar executável
            self.log_message("Copiando arquivos...")
            shutil.copy2(current_exe, dest_exe)
            
            # Copiar ícone se existir (para referência futura)
            try:
                icon_source = os.path.join(os.path.dirname(current_exe), "images", "icone.ico")
                if not os.path.exists(icon_source):
                    icon_source = os.path.join(os.path.dirname(__file__), "images", "icone.ico")
                if os.path.exists(icon_source):
                    icon_dir = os.path.join(INSTALL_DIR, "images")
                    os.makedirs(icon_dir, exist_ok=True)
                    shutil.copy2(icon_source, os.path.join(icon_dir, "icone.ico"))
            except Exception as e:
                pass  # Ícone é opcional
            
            self.log_message(f"✓ Instalação concluída!")
            self.log_message(f"✓ Programa instalado em: {INSTALL_DIR}")
            
            # Criar atalho na área de trabalho
            self.log_message("Criando atalho na área de trabalho...")
            success, method = self.create_desktop_shortcut(dest_exe, "Atualizador Shop9.lnk", dest_exe)
            if success:
                self.log_message(f"✓ Atalho criado na área de trabalho ({method})")
            else:
                self.log_message(f"⚠ Não foi possível criar atalho: {method}")
            
            messagebox.showinfo(
                "Instalação Concluída",
                f"Instalação concluída com sucesso!\n\n"
                f"Programa instalado em:\n{INSTALL_DIR}\n\n"
                f"O programa será reiniciado."
            )
            
            # Reiniciar o programa da pasta de instalação
            subprocess.Popen([dest_exe], creationflags=subprocess.CREATE_NO_WINDOW)
            self.root.after(500, self.root.quit)
            
        except Exception as e:
            self.log_message(f"✗ ERRO na instalação: {str(e)}")
            messagebox.showerror("Erro na Instalação", f"Erro ao instalar:\n{str(e)}")
    
    def get_remote_config(self):
        """Obtém a configuração remota (link de download do Shop9)"""
        try:
            response = requests.get(CONFIG_URL, timeout=10)
            response.raise_for_status()
            config = response.json()
            
            # Normalizar diferentes formatos de JSON para compatibilidade
            # URL de download do Shop9 (múltiplos formatos suportados)
            shop9_url = (
                config.get("shop9_download_url") or 
                config.get("shop9_url") or 
                config.get("url_shop9") or
                config.get("shop9_download") or
                config.get("url") or
                ""
            )
            
            # Retornar apenas o que é necessário para atualizar o Shop9
            return {
                "shop9_download_url": shop9_url,
                "description": config.get("description", ""),
                "last_updated": config.get("last_updated", "")
            }
        except requests.exceptions.RequestException as e:
            self.log_message(f"⚠️ Não foi possível verificar configuração remota: {str(e)}")
            return None
        except json.JSONDecodeError:
            self.log_message("⚠️ Erro ao decodificar configuração remota")
            return None
        except Exception as e:
            self.log_message(f"⚠️ Erro ao processar configuração remota: {str(e)}")
            return None
    
    
    def kill_processes(self):
        """Encerra os processos Shop9.exe e S9_Otica.exe"""
        processes_to_kill = ["Shop9.exe", "S9_Otica.exe"]
        
        try:
            import psutil
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in processes_to_kill:
                        self.log_message(f"Encerrando processo: {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.kill()
                        killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if killed:
                time.sleep(2)
                self.log_message("✓ Processos encerrados com sucesso")
            else:
                self.log_message("ℹ Nenhum processo encontrado para encerrar")
        except ImportError:
            # Fallback usando taskkill do Windows
            self.log_message("Usando método alternativo para encerrar processos...")
            for proc_name in processes_to_kill:
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/IM", proc_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False
                    )
                except Exception:
                    pass
            time.sleep(2)
            self.log_message("✓ Processos encerrados")
    
    def download_files(self):
        """Baixa arquivos do Google Drive usando URL do JSON remoto"""
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        # URL padrão (fallback)
        url = "https://drive.google.com/drive/folders/1aeVHZumfFEb8ac5vQIAP1ePn8OdCO3dI?usp=sharing"
        
        # Tentar obter URL da configuração remota
        self.log_message("Verificando configuração remota...")
        try:
            config = self.get_remote_config()
            if config and config.get("shop9_download_url"):
                url = config.get("shop9_download_url")
                self.log_message("✓ URL de download obtida da configuração remota")
                if config.get("description"):
                    self.log_message(f"ℹ {config.get('description')}")
            else:
                self.log_message("⚠ URL não encontrada no JSON, usando URL padrão")
        except Exception as e:
            self.log_message(f"⚠ Não foi possível obter configuração remota: {str(e)}")
            self.log_message("ℹ Usando URL padrão")
        
        try:
            import gdown
        except ImportError:
            self.log_message("gdown não disponível. Instalando...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown", "-q"], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                import gdown
                self.log_message("✓ gdown instalado com sucesso")
            except Exception as e:
                self.log_message(f"✗ Erro ao instalar gdown: {str(e)}")
                return False
        
        try:
            self.log_message("Iniciando download dos arquivos...")
            self.log_message("Isso pode levar alguns minutos dependendo da velocidade da internet...")
            self.update_progress(30, "30%")
            
            # Download com gdown
            gdown.download_folder(url, output=TEMP_DIR, quiet=True, use_cookies=False)
            
            self.update_progress(60, "60%")
            self.log_message("✓ Download concluído!")
            return True
        except Exception as e:
            self.log_message(f"✗ Erro ao baixar: {str(e)}")
            return False
    
    def extract_rar_files(self, rar_files):
        """Extrai arquivos RAR para o diretório de destino"""
        # Encontrar arquivo part1
        part1_file = None
        for rar_file in rar_files:
            full_path = os.path.join(TEMP_DIR, rar_file)
            if os.path.exists(full_path) and "part1" in rar_file.lower():
                part1_file = full_path
                break
        
        if not part1_file:
            self.log_message("✗ ERRO: Arquivo part1.rar não encontrado!")
            return False
        
        # Verificar se temos 7zip disponível
        sevenzip_paths = [
            r"C:\Program Files\7-Zip\7z.exe",
            r"C:\Program Files (x86)\7-Zip\7z.exe",
        ]
        
        sevenzip_in_path = shutil.which("7z.exe")
        if sevenzip_in_path:
            sevenzip_paths.insert(0, sevenzip_in_path)
        
        extractor = None
        for path in sevenzip_paths:
            if os.path.exists(path):
                extractor = path
                break
        
        # Método 3: Verificar WinRAR
        if not extractor:
            unrar_paths = [
                r"C:\Program Files\WinRAR\UnRAR.exe",
                r"C:\Program Files (x86)\WinRAR\UnRAR.exe",
            ]
            for path in unrar_paths:
                if os.path.exists(path):
                    extractor = path
                    break
        
        if extractor:
            try:
                os.makedirs(TARGET_DIR, exist_ok=True)
                
                if "7z" in extractor.lower() or "7-zip" in extractor.lower():
                    cmd = [extractor, "x", "-y", f"-o{TARGET_DIR}", part1_file]
                else:
                    cmd = [extractor, "x", "-o+", "-y", part1_file, TARGET_DIR]
                
                self.log_message(f"Usando {os.path.basename(extractor)} para extrair...")
                result = subprocess.run(cmd, capture_output=True, text=True, 
                                      cwd=os.path.dirname(part1_file))
                
                if result.returncode == 0:
                    self.log_message("✓ Extração concluída com sucesso!")
                    return True
                else:
                    self.log_message(f"✗ Erro na extração: {result.stderr}")
                    return False
            except Exception as e:
                self.log_message(f"✗ Erro ao extrair: {str(e)}")
                return False
        else:
            self.log_message("✗ ERRO: Nenhum extrator RAR encontrado!")
            self.log_message("Por favor, instale WinRAR ou 7-Zip no sistema")
            messagebox.showerror("Extrator não encontrado", 
                               "Nenhum extrator RAR foi encontrado!\n\n"
                               "Por favor, instale uma das opções:\n"
                               "• 7-Zip (recomendado - gratuito)\n"
                               "• WinRAR\n\n"
                               "Download 7-Zip: https://www.7-zip.org/")
            return False
    
    def cleanup(self):
        """Limpa arquivos temporários"""
        try:
            if os.path.exists(TEMP_DIR):
                shutil.rmtree(TEMP_DIR)
            self.log_message("✓ Limpeza concluída!")
        except Exception as e:
            self.log_message(f"⚠ Aviso: Não foi possível limpar arquivos temporários: {str(e)}")
    
    def open_shop9(self):
        """Abre o programa Shop9.exe"""
        shop9_path = os.path.join(TARGET_DIR, "Shop9.exe")
        if os.path.exists(shop9_path):
            try:
                self.log_message(f"Abrindo {shop9_path}...")
                subprocess.Popen([shop9_path], cwd=TARGET_DIR)
                self.log_message("✓ Shop9.exe aberto com sucesso!")
                return True
            except Exception as e:
                self.log_message(f"✗ Erro ao abrir Shop9.exe: {str(e)}")
                return False
        else:
            self.log_message(f"✗ Shop9.exe não encontrado em {shop9_path}")
            return False
    
    def run_update(self):
        """Executa o processo de atualização em thread separada"""
        try:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            
            # Passo 1: Encerrar processos
            self.update_status("Encerrando processos...")
            self.update_progress(10, "10%")
            self.log_message("=" * 50)
            self.log_message("Passo 1: Encerrando processos...")
            self.kill_processes()
            
            # Passo 2: Baixar arquivos
            self.update_status("Baixando arquivos...")
            self.update_progress(25, "25%")
            self.log_message("")
            self.log_message("Passo 2: Baixando arquivos do Google Drive...")
            if not self.download_files():
                self.log_message("✗ Falha no download!")
                messagebox.showerror("Erro", "Falha ao baixar os arquivos.\nVerifique sua conexão com a internet.")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                return
            
            # Verificar se os arquivos foram baixados
            rar_files_found = []
            if os.path.exists(TEMP_DIR):
                for file in os.listdir(TEMP_DIR):
                    if file.endswith('.rar'):
                        rar_files_found.append(file)
            
            if not rar_files_found:
                self.log_message("✗ ERRO: Nenhum arquivo RAR foi baixado!")
                messagebox.showerror("Erro", "Nenhum arquivo RAR foi baixado!")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                return
            
            self.log_message(f"✓ Arquivos encontrados: {len(rar_files_found)}")
            
            # Passo 3: Extrair arquivos
            self.update_status("Extraindo arquivos...")
            self.update_progress(65, "65%")
            self.log_message("")
            self.log_message("Passo 3: Extraindo arquivos...")
            if not self.extract_rar_files(rar_files_found):
                self.log_message("✗ Falha na extração!")
                messagebox.showerror("Erro", "Falha na extração dos arquivos!")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                return
            
            self.log_message(f"✓ Arquivos extraídos para: {TARGET_DIR}")
            
            # Passo 4: Limpar arquivos temporários
            self.update_status("Limpando arquivos temporários...")
            self.update_progress(90, "90%")
            self.log_message("")
            self.log_message("Passo 4: Limpando arquivos temporários...")
            self.cleanup()
            
            # Concluído
            self.update_status("Atualização concluída!")
            self.update_progress(100, "100%")
            self.log_message("")
            self.log_message("=" * 50)
            self.log_message("✓ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
            self.log_message("=" * 50)
            
            # Abrir Shop9.exe automaticamente
            self.log_message("")
            self.log_message("Abrindo Shop9.exe...")
            self.open_shop9()
            
            messagebox.showinfo("Sucesso", "Atualização concluída com sucesso!")
            
            # Fechar a aplicação após clicar em OK
            self.root.after(100, self.root.quit)
            
        except Exception as e:
            self.log_message(f"✗ ERRO CRÍTICO: {str(e)}")
            import traceback
            error_details = traceback.format_exc()
            self.log_message(error_details)
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro:\n{str(e)}")
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
    
    def start_update(self):
        """Inicia o processo de atualização"""
        if self.is_running:
            return
        
        # Limpar log anterior
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Confirmar ação
        if not messagebox.askyesno("Confirmar", 
                                   "Deseja iniciar a atualização do Shop9?\n\n"
                                   "O programa irá:\n"
                                   "• Encerrar processos Shop9.exe e S9_Otica.exe\n"
                                   "• Baixar arquivos do Google Drive\n"
                                   "• Extrair para C:\\Shop9"):
            return
        
        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=self.run_update, daemon=True)
        thread.start()

def main():
    """Função principal"""
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        # Modo de instalação silenciosa (já com privilégios de admin)
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return
            
            if getattr(sys, 'frozen', False):
                current_exe = sys.executable
            else:
                current_exe = os.path.abspath(__file__)
            
            os.makedirs(INSTALL_DIR, exist_ok=True)
            dest_exe = os.path.join(INSTALL_DIR, PROGRAM_NAME)
            shutil.copy2(current_exe, dest_exe)
            
            # Copiar ícone se existir
            try:
                icon_source = os.path.join(os.path.dirname(current_exe), "images", "icone.ico")
                if not os.path.exists(icon_source):
                    icon_source = os.path.join(os.path.dirname(__file__), "images", "icone.ico")
                if os.path.exists(icon_source):
                    icon_dir = os.path.join(INSTALL_DIR, "images")
                    os.makedirs(icon_dir, exist_ok=True)
                    shutil.copy2(icon_source, os.path.join(icon_dir, "icone.ico"))
            except:
                pass
            
            # Criar atalho na área de trabalho
            success, method = create_desktop_shortcut(dest_exe, "Atualizador Shop9.lnk", dest_exe)
            if not success:
                # Se falhar, tentar novamente sem especificar método
                pass
            
            # Executar o programa instalado
            subprocess.Popen([dest_exe], creationflags=subprocess.CREATE_NO_WINDOW)
            return
        except Exception as e:
            print(f"Erro na instalação: {str(e)}")
            return
    
    # Esconder console (se disponível)
    try:
        import ctypes
        if sys.platform == "win32":
            # Esconder console do Windows
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    root = tk.Tk()
    
    # Tentar definir o ícone da janela
    try:
        # Primeiro, tentar usar o ícone do executável (se estiver incorporado)
        if getattr(sys, 'frozen', False):
            # Executável compilado - o ícone já está incorporado
            try:
                import ctypes
                # Definir ícone do executável para a janela
                hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
                if hwnd:
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AtualizadorShop9.1.0.0")
            except:
                pass
        else:
            # Script Python - tentar carregar o ícone da pasta images
            icon_path = os.path.join(os.path.dirname(__file__), "images", "ícone de área de tra.png")
            if os.path.exists(icon_path):
                try:
                    root.iconphoto(False, tk.PhotoImage(file=icon_path))
                except:
                    pass
    except:
        pass
    
    app = AtualizadorShop9(root)
    root.mainloop()

if __name__ == "__main__":
    main()
