# Atualizador Shop9

Programa para baixar e instalar atualizações do Shop9 automaticamente.

## Funcionalidades

- ✅ Interface gráfica simples e intuitiva
- ✅ Baixa arquivos do Google Drive automaticamente
- ✅ Encerra processos Shop9.exe e S9_Otica.exe antes da atualização
- ✅ Extrai arquivos RAR para C:\Shop9
- ✅ Sobrescreve arquivos existentes automaticamente
- ✅ Executável standalone (não requer Python instalado)
- ✅ Console roda em segundo plano (sem janela de terminal)

## Como Gerar o Executável

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o script de build:
```bash
build_exe.bat
```

3. O executável será criado em `dist\AtualizadorShop9.exe`

## Requisitos do Sistema

- Windows 10 ou superior
- WinRAR ou 7-Zip instalado (para extrair arquivos RAR)
- Conexão com internet (para baixar arquivos)

## Uso

1. Execute `AtualizadorShop9.exe` (duplo clique)
2. Uma janela gráfica será aberta
3. Clique em "Iniciar Atualização"
4. O programa irá:
   - Encerrar processos do Shop9
   - Baixar arquivos do Google Drive
   - Extrair para C:\Shop9
   - Limpar arquivos temporários
5. Acompanhe o progresso na interface gráfica

## Notas

- O programa precisa de acesso à internet para baixar os arquivos
- Certifique-se de que WinRAR ou 7-Zip está instalado no sistema
- O programa criará a pasta C:\Shop9 se ela não existir
