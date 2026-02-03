# Como Configurar a Atualização Automática do Shop9

## Visão Geral

O sistema de atualização automática permite que você atualize o link de download do Shop9 sem precisar recompilar o programa. Basta atualizar um arquivo JSON remoto quando quiser disponibilizar novos arquivos do Shop9.

## Como Funciona

1. O programa verifica automaticamente um arquivo JSON remoto ao iniciar a atualização
2. Obtém o link de download mais recente do Shop9 do JSON
3. Baixa os arquivos do link especificado no JSON
4. Extrai e instala os arquivos no diretório C:\Shop9

## Passo a Passo para Configurar

### 1. Criar o Arquivo de Configuração

Crie um arquivo JSON com o seguinte formato (veja `version.json.example`):

```json
{
  "shop9_download_url": "https://drive.google.com/drive/folders/1aeVHZumfFEb8ac5vQIAP1ePn8OdCO3dI?usp=sharing",
  "description": "Nova versão do Shop9 com melhorias",
  "last_updated": "2024-01-15"
}
```

**Importante:** O campo `shop9_download_url` é obrigatório. Os outros campos são opcionais.

### 2. Hospedar o Arquivo JSON

Você pode hospedar o arquivo JSON em qualquer lugar acessível via HTTP/HTTPS:

#### Opção A: GitHub (Recomendado - Gratuito e Fácil)

1. Crie um repositório no GitHub (pode ser privado ou público)
2. Faça upload do arquivo `version.json`
3. Clique em "Raw" para obter o link direto
4. Copie a URL (exemplo: `https://raw.githubusercontent.com/seu-usuario/repo/main/version.json`)

#### Opção B: Google Drive

1. Faça upload do arquivo `version.json` no Google Drive
2. Clique com botão direito > Compartilhar > Qualquer pessoa com o link
3. Obtenha o ID do arquivo da URL
4. Use o formato: `https://drive.google.com/uc?export=download&id=SEU_FILE_ID`

#### Opção C: Servidor Próprio

1. Faça upload do arquivo para seu servidor web
2. Use a URL completa do arquivo

### 3. Configurar a URL no Código

O programa já está configurado para usar o repositório:
**https://github.com/caioetchebehere/AtualizadorAutomatico**

A URL do JSON está definida em `atualizador_shop9.py`:
```python
CONFIG_URL = "https://raw.githubusercontent.com/caioetchebehere/AtualizadorAutomatico/main/version.json"
```

Se precisar alterar para outro repositório ou arquivo, edite a constante `CONFIG_URL` no código.

### 4. Atualizar o Link de Download do Shop9

Quando quiser disponibilizar uma nova versão do Shop9:

1. Faça upload dos novos arquivos do Shop9 para o Google Drive (ou outro serviço)
2. Compartilhe a pasta/link publicamente
3. Atualize o arquivo `version.json` remoto com:
   - Novo link de download (`shop9_download_url`)
   - Descrição opcional das mudanças
   - Data da atualização

**Não é necessário recompilar o atualizador!** Basta atualizar o JSON.

## Campos do Arquivo JSON

O programa suporta múltiplos formatos de nomes de campos para maior compatibilidade:

### Campo Obrigatório:
- **shop9_download_url** (ou **shop9_url**, **url_shop9**, **shop9_download**, **url**): Link do Google Drive para download do Shop9

### Campos Opcionais:
- **description**: Descrição opcional das mudanças/atualizações
- **last_updated**: Data da última atualização (opcional)

### Exemplo de JSON compatível:

```json
{
  "shop9_download_url": "https://drive.google.com/drive/folders/1aeVHZumfFEb8ac5vQIAP1ePn8OdCO3dI?usp=sharing",
  "description": "Nova versão do Shop9 com correções e melhorias",
  "last_updated": "2024-01-15"
}
```

Ou usando formato alternativo:
```json
{
  "shop9_url": "https://drive.google.com/drive/folders/1aeVHZumfFEb8ac5vQIAP1ePn8OdCO3dI?usp=sharing",
  "description": "Atualização do Shop9"
}
```

## Exemplo de Fluxo de Atualização

1. Você prepara uma nova versão do Shop9
2. Faz upload dos arquivos para o Google Drive
3. Obtém o link compartilhado da pasta
4. Atualiza o `version.json` remoto no repositório:
   ```json
   {
     "shop9_download_url": "https://drive.google.com/drive/folders/NOVO_LINK?usp=sharing",
     "description": "Nova versão com correções importantes",
     "last_updated": "2024-01-20"
   }
   ```
5. Quando os usuários executarem o atualizador e clicarem em "Iniciar Atualização", o programa:
   - Verificará o JSON remoto
   - Obterá o link mais recente
   - Baixará os arquivos do link especificado
   - Instalará no C:\Shop9

## Vantagens

- ✅ Não precisa recompilar o atualizador para mudar o link de download
- ✅ Controle centralizado do link de download via JSON
- ✅ Fácil de atualizar - basta editar o JSON no GitHub
- ✅ Os usuários sempre baixam a versão mais recente do Shop9
- ✅ Pode incluir descrições das atualizações no JSON

## Notas Importantes

- O arquivo JSON deve estar sempre acessível via HTTP/HTTPS
- O link de download do executável deve ser direto (não página de compartilhamento)
- Para Google Drive, use o formato com `uc?export=download&id=`
- Teste sempre após configurar para garantir que está funcionando
