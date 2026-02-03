@echo off
chcp 65001 >nul
echo ========================================
echo Gerador de Executável - Atualizador Shop9
echo ========================================
echo.
echo Este script criará um executável standalone
echo que pode ser usado em computadores SEM Python instalado.
echo.

echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale Python primeiro.
    pause
    exit /b 1
)
python --version

echo.
echo [2/4] Instalando dependências...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependências!
    pause
    exit /b 1
)
echo ✓ Dependências instaladas com sucesso

REM Verificar se PyInstaller foi instalado corretamente
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: PyInstaller não foi instalado corretamente!
    echo Tentando instalar novamente...
    python -m pip install pyinstaller --force-reinstall
    if errorlevel 1 (
        echo ERRO: Não foi possível instalar PyInstaller!
        pause
        exit /b 1
    )
)
echo ✓ PyInstaller verificado

echo.
echo [2.5/4] Convertendo ícone PNG para ICO...
python converter_icone.py
if errorlevel 1 (
    echo AVISO: Não foi possível converter o ícone, continuando sem ícone...
)

echo.
echo [3/4] Criando executável standalone com PyInstaller...
echo Isso pode levar alguns minutos, aguarde...
echo.

REM Limpar builds anteriores
if exist build rmdir /s /q build >nul 2>&1
if exist dist\AtualizadorShop9.exe del /q dist\AtualizadorShop9.exe >nul 2>&1

REM Verificar se o ícone existe
set ICONE_PARAM=
if exist images\icone.ico (
    set ICONE_PARAM=--icon=images\icone.ico
)

REM Criar executável usando PyInstaller através do arquivo .spec (recomendado)
REM O arquivo .spec já contém todas as configurações otimizadas para reduzir falsos positivos
python -m PyInstaller --clean --noconfirm AtualizadorShop9.spec

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao criar executável!
    echo Verifique os erros acima.
    pause
    exit /b 1
)

echo.
echo [4/4] Compilação concluída!
echo.
echo ========================================
echo ✓ SUCESSO! Executável criado!
echo ========================================
echo.
echo Localização: dist\AtualizadorShop9.exe
echo.
echo Este arquivo pode ser copiado para QUALQUER computador Windows
echo e executado SEM necessidade de Python instalado!
echo.
if exist dist\AtualizadorShop9.exe (
    echo Tamanho do arquivo:
    dir dist\AtualizadorShop9.exe | find "AtualizadorShop9.exe"
    echo.
    echo ========================================
    echo VERIFICAÇÃO DE ANTIVÍRUS
    echo ========================================
    echo.
    echo Para verificar se há falsos positivos, execute:
    echo   python verificar_antivirus.py
    echo.
    echo Ou acesse: https://www.virustotal.com/
    echo e faça upload do executável.
    echo.
    echo Se houver detecções, consulte SOLUCOES_ANTIVIRUS.md
    echo.
) else (
    echo AVISO: Arquivo não encontrado em dist\
)
echo ========================================
pause
