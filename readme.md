Watchtower-AI
=============

## Installation
```bash
uv sync
```

## Run
```bash
uv run flask db upgrade
```
```bash
uv run flask --app src.main run --debug
```

## Environment
```python
import secrets
print(secrets.token_hex())
print(secrets.SystemRandom().getrandbits(128))
```