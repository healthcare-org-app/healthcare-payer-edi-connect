# payer-edi-connect

payer-edi-connect — domain: insurance

- **Port:** 8804
- **Language:** Python 3.11 + Flask
- **Database:** `insurance` (Postgres, table `payer_edi_connect`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/payer_edi_connect/`          |
| POST      | `/api/payer_edi_connect/`          |
| GET       | `/api/payer_edi_connect/<id>`      |
| PUT/PATCH | `/api/payer_edi_connect/<id>`      |
| DELETE    | `/api/payer_edi_connect/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** claim.submitted

## HTTP peer dependencies

- `payer-directory`
- `secrets-vault`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
