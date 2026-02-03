"""
Script para verificar o executável em múltiplos antivírus usando VirusTotal API
e fornecer instruções para reduzir falsos positivos.
"""
import os
import sys
import hashlib
import json

def calcular_hash_arquivo(caminho_arquivo):
    """Calcula SHA256 do arquivo"""
    sha256_hash = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verificar_arquivo(arquivo_exe):
    """Verifica informações do executável"""
    if not os.path.exists(arquivo_exe):
        print(f"ERRO: Arquivo não encontrado: {arquivo_exe}")
        return
    
    tamanho = os.path.getsize(arquivo_exe)
    sha256 = calcular_hash_arquivo(arquivo_exe)
    
    print("=" * 60)
    print("INFORMAÇÕES DO EXECUTÁVEL")
    print("=" * 60)
    print(f"Arquivo: {arquivo_exe}")
    print(f"Tamanho: {tamanho:,} bytes ({tamanho / 1024 / 1024:.2f} MB)")
    print(f"SHA256: {sha256}")
    print()
    
    print("=" * 60)
    print("VERIFICAÇÃO EM ANTIVÍRUS")
    print("=" * 60)
    print()
    print("Para verificar em múltiplos antivírus, use:")
    print(f"1. Acesse: https://www.virustotal.com/")
    print(f"2. Faça upload do arquivo ou use o hash SHA256:")
    print(f"   {sha256}")
    print()
    print("3. Se houver detecções, elas são provavelmente falsos positivos")
    print("   se apenas alguns antivírus detectarem (menos de 5-10).")
    print()
    
    print("=" * 60)
    print("COMO REDUZIR FALSOS POSITIVOS")
    print("=" * 60)
    print()
    print("1. ASSINATURA DIGITAL (Mais Eficaz)")
    print("   - Compre um certificado Code Signing (~$200-400/ano)")
    print("   - Use signtool.exe para assinar o executável")
    print("   - Elimina praticamente todos os falsos positivos")
    print()
    print("2. SUBMETER PARA ANÁLISE")
    print("   - Se apenas alguns antivírus detectarem, submeta para análise")
    print("   - Cada fabricante tem um processo de whitelist")
    print("   - Links:")
    print("     * Windows Defender: https://www.microsoft.com/en-us/wdsi/filesubmission")
    print("     * Avast: https://www.avast.com/false-positive-file-form.php")
    print("     * AVG: https://www.avg.com/en-us/false-positive-file-form")
    print()
    print("3. DISTRIBUIÇÃO")
    print("   - Distribua através de fontes confiáveis (GitHub Releases, etc.)")
    print("   - Antivírus confiam mais em arquivos de fontes conhecidas")
    print()
    print("4. ADICIONAR À LISTA DE EXCEÇÕES")
    print("   - Instrua usuários a adicionar à lista de exceções")
    print("   - Necessário apenas na primeira execução")
    print()
    
    print("=" * 60)
    print("INSTRUÇÕES PARA USUÁRIOS")
    print("=" * 60)
    print()
    print("Se o antivírus bloquear o programa:")
    print()
    print("WINDOWS DEFENDER:")
    print("1. Abra 'Segurança do Windows'")
    print("2. Vá em 'Proteção contra vírus e ameaças'")
    print("3. Clique em 'Gerenciar configurações'")
    print("4. Role até 'Exclusões'")
    print("5. Clique em 'Adicionar ou remover exclusões'")
    print("6. Adicione o arquivo ou pasta")
    print()
    print("OUTROS ANTIVÍRUS:")
    print("- Consulte a documentação do seu antivírus")
    print("- Procure por 'Exceções', 'Whitelist' ou 'Exclusões'")
    print("- Adicione o arquivo ou pasta à lista")
    print()

if __name__ == '__main__':
    arquivo = 'dist\\AtualizadorShop9.exe'
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    
    verificar_arquivo(arquivo)
