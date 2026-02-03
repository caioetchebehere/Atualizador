"""
Script de Instalação do Atualizador Shop9
Instala o programa em C:\Program Files (x86)\AtualizadorShop9
"""

import os
import sys
import shutil
import ctypes
import tkinter as tk
from tkinter import messagebox

# Caminhos
INSTALL_DIR = r"C:\Program Files (x86)\AtualizadorShop9"
PROGRAM_NAME = "AtualizadorShop9.exe"

def is_admin():
    """Verifica se o programa está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate():
    """Reexecuta o script com privilégios de administrador"""
    if is_admin():
        return True
    else:
        # Reexecutar com privilégios de administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return False

def install():
    """Instala o programa em C:\Program Files (x86)\AtualizadorShop9"""
    try:
        # Verificar privilégios de administrador
        if not is_admin():
            print("⚠️ Privilégios de administrador necessários!")
            print("Solicitando elevação de privilégios...")
            if not elevate():
                return False
            return True  # O script será reexecutado com privilégios
        
        # Obter caminho do executável atual
        if getattr(sys, 'frozen', False):
            # Executável compilado
            current_exe = sys.executable
        else:
            # Script Python - procurar o executável compilado
            current_exe = os.path.join(os.path.dirname(__file__), "dist", PROGRAM_NAME)
            if not os.path.exists(current_exe):
                current_exe = os.path.join(os.path.dirname(__file__), PROGRAM_NAME)
        
        if not os.path.exists(current_exe):
            print(f"✗ ERRO: Executável não encontrado: {current_exe}")
            return False
        
        print(f"Instalando de: {current_exe}")
        print(f"Instalando para: {INSTALL_DIR}")
        
        # Criar diretório de instalação
        os.makedirs(INSTALL_DIR, exist_ok=True)
        
        # Caminho de destino
        dest_exe = os.path.join(INSTALL_DIR, PROGRAM_NAME)
        
        # Copiar executável
        print("Copiando arquivos...")
        shutil.copy2(current_exe, dest_exe)
        
        print(f"✓ Instalação concluída!")
        print(f"✓ Programa instalado em: {INSTALL_DIR}")
        
        # Criar atalho na área de trabalho (opcional)
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Atualizador Shop9.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = dest_exe
            shortcut.WorkingDirectory = INSTALL_DIR
            shortcut.IconLocation = dest_exe  # Usar ícone do executável
            shortcut.save()
            
            print(f"✓ Atalho criado na área de trabalho")
        except ImportError:
            print("ℹ Bibliotecas para criar atalho não disponíveis (opcional)")
        except Exception as e:
            print(f"⚠ Não foi possível criar atalho: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO na instalação: {str(e)}")
        return False

def uninstall():
    """Desinstala o programa"""
    try:
        if not is_admin():
            print("⚠️ Privilégios de administrador necessários!")
            if not elevate():
                return False
            return True
        
        if os.path.exists(INSTALL_DIR):
            print(f"Removendo: {INSTALL_DIR}")
            shutil.rmtree(INSTALL_DIR)
            print("✓ Desinstalação concluída!")
        else:
            print("ℹ Programa não está instalado")
        
        return True
    except Exception as e:
        print(f"✗ ERRO na desinstalação: {str(e)}")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--uninstall":
            uninstall()
        elif sys.argv[1] == "--install":
            install()
        else:
            print("Uso: python instalador.py [--install|--uninstall]")
    else:
        # Modo interativo
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        
        if messagebox.askyesno(
            "Instalar Atualizador Shop9",
            f"Deseja instalar o Atualizador Shop9 em:\n{INSTALL_DIR}\n\n"
            "Será necessário executar como Administrador."
        ):
            if install():
                messagebox.showinfo("Sucesso", f"Instalação concluída!\n\nPrograma instalado em:\n{INSTALL_DIR}")
            else:
                messagebox.showerror("Erro", "Falha na instalação!\n\nVerifique se você tem privilégios de administrador.")
        
        root.destroy()

if __name__ == "__main__":
    main()
