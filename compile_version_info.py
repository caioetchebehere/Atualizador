"""
Script para compilar version_info.rc para version_info.res
Necessário para adicionar informações de versão ao executável
"""
import os
import subprocess
import sys

def compile_version_info():
    """Compila version_info.rc para version_info.res"""
    rc_file = 'version_info.rc'
    res_file = 'version_info.res'
    
    if not os.path.exists(rc_file):
        print(f"AVISO: {rc_file} não encontrado. Pulando compilação de versão.")
        return False
    
    # Verificar se já existe um arquivo .res mais recente
    if os.path.exists(res_file):
        rc_time = os.path.getmtime(rc_file)
        res_time = os.path.getmtime(res_file)
        if res_time >= rc_time:
            print(f"✓ {res_file} já está atualizado.")
            return True
    
    # Tentar encontrar rc.exe (Resource Compiler do Windows SDK)
    rc_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\rc.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\x64\rc.exe",
        r"C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1\Bin\rc.exe",
        r"C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\rc.exe",
    ]
    
    # Tentar encontrar no PATH
    rc_exe = None
    for path in rc_paths:
        if os.path.exists(path):
            rc_exe = path
            break
    
    if not rc_exe:
        # Tentar encontrar no PATH
        try:
            result = subprocess.run(['where', 'rc.exe'], 
                                  capture_output=True, 
                                  text=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                rc_exe = result.stdout.strip().split('\n')[0]
        except:
            pass
    
    if not rc_exe or not os.path.exists(rc_exe):
        print("AVISO: rc.exe não encontrado. Tentando usar pywin32...")
        # Tentar usar pywin32 para compilar
        try:
            import win32rcparser
            import win32api
            # Pywin32 pode não ter essa funcionalidade, então vamos tentar outra abordagem
            print("AVISO: Compilação automática não disponível.")
            print("O PyInstaller tentará compilar automaticamente ou você pode:")
            print("1. Instalar Windows SDK")
            print("2. Usar o arquivo .rc diretamente (PyInstaller pode compilar)")
            return False
        except ImportError:
            print("AVISO: pywin32 não instalado.")
            print("O PyInstaller pode compilar o .rc automaticamente se tiver as ferramentas.")
            return False
    
    try:
        print(f"Compilando {rc_file} para {res_file}...")
        result = subprocess.run(
            [rc_exe, '/fo', res_file, rc_file],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0 and os.path.exists(res_file):
            print(f"✓ {res_file} compilado com sucesso!")
            return True
        else:
            print(f"ERRO ao compilar: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERRO ao compilar: {str(e)}")
        return False

if __name__ == '__main__':
    success = compile_version_info()
    sys.exit(0 if success else 1)
