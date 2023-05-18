# Playtest

Playtest is a test automation solution for web testing using Playwright and Pytest.


## Key Objectives
- Data driven test capability
- High abstraction
- Informative reporting
- Easy configuration


## Docker usage

Start container
```bash
docker-compose up --build
```

Run the container
```bash
docker start playtest -a
```

> **⚠ WARNING:** Running headed inside Docker fails currently as it needs xvfb-run command which is not yet implemented. 


## Streamlit usage

Run streamlit app locally for an interactive web ui
```bash
streamlit run web/app.py
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
test_dir: null
test_file: null
test_case: null
rerun: 2
tracing: True
```