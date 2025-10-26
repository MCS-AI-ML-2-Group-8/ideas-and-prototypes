## Installing uv

### Windows

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### MacOS and Linux

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Installing dependencies

### Using uv

```sh
uv sync
```

### Using pip

```sh
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Running application

### Using uv

#### CLI mode

```sh
uv run main.py
```

#### UI mode

```sh
uv run main.py --ui
```
