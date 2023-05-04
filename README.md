# Playtest

Playtest is a test automation solution for web testing using Playwright and Pytest.


## Key Objectives
- Data driven test capability
- High abstraction
- Informative reporting
- Easy configuration


## Usage

Run all tests
```bash
python -m pytest
```

Run tests with a given mark e.g. smoke
```bash
python -m pytest -m smoke
```

Run with verbose terminal output
```bash
python -m pytest -v
```

Run with the playtest report plugin to generate a json report
```bash
python -m pytest --playtest-report
```

Run tests in parallel with `pytest-xdist`
```bash
python -m pytest --numprocesses auto
```

## Docker usage

Start container
```bash
docker-compose up --build
```

Run the container
```bash
docker start playtest -a
```

## Streamlit usage

Run streamlit app for an interactive web ui
```bash
streamlit run ./web/app.py
```

## Config
Example of `config.yaml` file usage
```yaml
verbose: True
parallel: False
playtest-report: False
marks:
  - smoke
  - regression
```