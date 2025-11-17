# Discogs Scraper

Este repositório contém um scraper para coletar informações de artistas e álbuns do Discogs.

**Pré-requisitos**
- Python 3.10+ instalado no sistema
- Google Chrome instalado (para o Selenium)

**Observação:** o projeto usa Selenium; o ChromeDriver é gerenciado automaticamente em versões recentes do Selenium, mas em alguns sistemas pode ser necessário instalar um `chromedriver` compatível ou ajustar o `PATH`.

**Uso rápido**
- Clone o repositório e entre na pasta do projeto.

**Criar e ativar um ambiente virtual (Windows PowerShell)**

- Criar o venv:

	`py -3 -m venv .\venv`

- Ativar o venv:

	`& .\venv\Scripts\Activate.ps1`

**Instalar dependências**

- Instalar a partir do `requirements.txt`:

	`& .\venv\Scripts\python.exe -m pip install -r requirements.txt`

**Executar o scraper**

- Rodar o script principal (exemplo):

	`& .\venv\Scripts\python.exe -m src.main`

- Observações:
	- Por padrão o scraper cria um arquivo `./data/discogs_scraper.jsonl` com os resultados.
	- Se você quiser ver as janelas do navegador, verifique a função `get_driver()` em `src/services/selenium_service.py` — remova a flag `--headless` se for adicionada, ou chame a função com um parâmetro que controle o modo headless.

**Rodar os testes**

- Executar todos os testes:

	`& .\venv\Scripts\python.exe -m pytest -q`

- Executar um teste específico (ex.: teste do parser de álbum):

	`& .\venv\Scripts\python.exe -m pytest tests/test_parser.py::test_parse_album_info_tracks_styles_and_year -q`

**Estrutura do projeto (resumida)**
- `src/` — código fonte do scraper
	- `scraper/` — cliente, parser e modelos
	- `services/` — utilitários e criação do driver Selenium
- `tests/` — testes unitários e fixtures
- `requirements.txt` — dependências do projeto

