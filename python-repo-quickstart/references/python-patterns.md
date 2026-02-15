# Python Project Structure Patterns

## Common File Indicators

### Entry Points
- `main.py` - Main entry point
- `__main__.py` - Package entry point (python -m package)
- `app.py` / `run.py` - Application entry (Flask/FastAPI)
- `manage.py` - Django management script
- `cli.py` - Command-line interface
- `setup.py` - Installation script (legacy)
- `pyproject.toml` - Modern Python project configuration

### Configuration Files
- `requirements.txt` - pip dependencies
- `requirements-dev.txt` - Development dependencies
- `Pipfile` / `Pipfile.lock` - Pipenv dependencies
- `poetry.lock` / `pyproject.toml` - Poetry dependencies
- `environment.yml` - Conda environment
- `setup.cfg` - Setup configuration
- `tox.ini` - Testing automation
- `.env` / `.env.example` - Environment variables

### Documentation
- `README.md` - Project overview
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - License information
- `CHANGELOG.md` - Version history
- `docs/` - Documentation directory

### Testing
- `tests/` - Test directory
- `test_*.py` - Test files
- `*_test.py` - Alternative test naming
- `conftest.py` - pytest configuration
- `pytest.ini` - pytest settings
- `.coveragerc` - Coverage configuration

## Project Type Indicators

### Web Framework
**Flask:**
- `app.py` with Flask imports
- `templates/` directory
- `static/` directory
- `flask run` in README

**Django:**
- `manage.py`
- `settings.py`
- `urls.py`
- `wsgi.py` / `asgi.py`
- Django apps structure

**FastAPI:**
- `main.py` with FastAPI imports
- `routers/` directory
- `uvicorn` in dependencies
- Async/await patterns

### Data Science
- `notebooks/` - Jupyter notebooks
- `data/` - Data directory
- `models/` - ML models
- pandas, numpy, scikit-learn in dependencies
- `.ipynb` files

### CLI Tool
- `cli.py` or `__main__.py`
- `argparse` / `click` / `typer` imports
- Console scripts in setup.py/pyproject.toml

### Library/Package
- `src/` directory structure
- `__init__.py` files
- `setup.py` or `pyproject.toml`
- No main entry point

## Dependency Management Patterns

### pip (requirements.txt)
```
package==1.0.0
package>=1.0.0,<2.0.0
package~=1.0.0
```

### Poetry (pyproject.toml)
```toml
[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"
```

### Pipenv (Pipfile)
```toml
[packages]
requests = "*"
django = "~=4.0"
```

### Conda (environment.yml)
```yaml
dependencies:
  - python=3.9
  - numpy
  - pip:
    - requests
```

## Setup Instructions Patterns

### Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Installation
```bash
pip install -r requirements.txt
pip install -e .
poetry install
pipenv install
conda env create -f environment.yml
```

### Running
```bash
python main.py
python -m package_name
flask run
uvicorn main:app --reload
python manage.py runserver
```

## Common Directory Structures

### Simple Script
```
project/
├── main.py
├── requirements.txt
└── README.md
```

### Package
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

### Web Application
```
project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── templates/
├── tests/
├── requirements.txt
├── config.py
└── run.py
```

### Data Science
```
project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── models/
├── requirements.txt
└── README.md
```
