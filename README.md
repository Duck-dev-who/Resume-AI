# Resume AI

## Setup

### Clone the repository

```bash
git clone <repo-url>
cd resume-ai
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the API

```bash
uvicorn app.main:app --reload
```

### API Docs

Open:

http://127.0.0.1:8000/docs