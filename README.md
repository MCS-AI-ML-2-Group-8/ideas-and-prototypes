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

#### API server

API is avaialble at: http://127.0.0.1:8000 \
Swagger endpoint at: http://127.0.0.1:8000/docs

```sh
uv run main.py --api
```

or

```sh
uv run fastapi dev api.py
```

### Build standalone on Windows

1. Install Windows SDK (use Visual Studio Installer)
2. Open "x64 Native Tools Command Prompt"
3. Activate environment `.venv\Scripts\activate`

```
nuitka main.py --standalone --msvc=latest --enable-plugin=pyside6 --include-qt-plugins=sensible,platforms
```