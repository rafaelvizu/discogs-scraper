# Discogs Scraper

Scraper para coletar informações de artistas e álbuns do Discogs usando Playwright (Chromium).

## Pré-requisitos

- Python 3.10+ instalado
- Playwright instalado e navegadores preparados (Chromium)

> Observação: o projeto foi migrado de Selenium para Playwright. É necessário instalar o pacote `playwright` e baixar o Chromium gerenciado.

## Uso no Windows (PowerShell)

1) Criar e ativar o ambiente virtual

```powershell
py -3 -m venv .\venv
& .\venv\Scripts\Activate.ps1
```

2) Instalar dependências e preparar Playwright

```powershell
& .\venv\Scripts\python.exe -m pip install -r requirements.txt
& .\venv\Scripts\python.exe -m playwright install chromium
```

3) Executar o scraper

```powershell
& .\venv\Scripts\python.exe -m src.main
```

Observações:
- Por padrão o scraper salva em `./data/discogs_scraper.jsonl`.
- Para modo headless, ajuste o `headless` no lançamento do navegador (veja `src/main.py`).

4) Rodar os testes

```powershell
& .\venv\Scripts\python.exe -m pytest -q
```

## Uso no Ubuntu

1) Dependências do sistema

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

2) Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Instalar dependências e preparar Playwright

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

4) Executar o scraper

```bash
python -m src.main
```

5) Rodar os testes

```bash
pytest -q
```

## Estrutura do projeto

- `src/` — código fonte
  - `scraper/` — cliente (Playwright), parser e modelos
  - `services/` — utilitários e gerenciamento do navegador Playwright
- `tests/` — testes unitários e fixtures
- `requirements.txt` — dependências
