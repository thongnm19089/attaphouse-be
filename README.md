## Install venv

```bash
python -m venv env
```

## Active venv

```bash
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
## Install libraries

```bash
pip install -r requirements.txt
```

## Make migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run server(http://127.0.0.1:8000/)

```bash
python manage.py run server
```