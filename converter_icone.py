"""
Script para converter o ícone PNG para ICO
"""

import os
from PIL import Image

def converter_png_para_ico():
    """Converte o arquivo PNG para ICO"""
    png_path = os.path.join("images", "ícone de área de tra.png")
    ico_path = os.path.join("images", "icone.ico")
    
    if not os.path.exists(png_path):
        print(f"✗ Arquivo não encontrado: {png_path}")
        return False
    
    try:
        # Abrir a imagem PNG
        img = Image.open(png_path)
        
        # Converter para ICO (múltiplos tamanhos para melhor compatibilidade)
        # Criar uma lista de tamanhos comuns para ícones Windows
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Salvar como ICO com múltiplos tamanhos
        img.save(ico_path, format='ICO', sizes=sizes)
        
        print(f"✓ Ícone convertido com sucesso!")
        print(f"✓ Arquivo criado: {ico_path}")
        return True
    except ImportError:
        print("⚠ Pillow não está instalado. Instalando...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
        # Tentar novamente
        img = Image.open(png_path)
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"✓ Ícone convertido com sucesso!")
        print(f"✓ Arquivo criado: {ico_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao converter: {str(e)}")
        return False

if __name__ == "__main__":
    converter_png_para_ico()
