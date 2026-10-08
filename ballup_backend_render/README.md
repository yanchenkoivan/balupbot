# БаллUP Backend

FastAPI backend for the БаллUP Telegram Mini App.

## Local run

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn server.main:app --reload
```

Health: `http://127.0.0.1:8000/api/health`

## Render

Render uses `render.yaml` and starts:

```text
uvicorn server.main:app --host 0.0.0.0 --port $PORT
```

Set these environment variables in Render:

- `BOT_TOKEN` — Telegram bot token
- `DATABASE_URL` — Render PostgreSQL connection string
- `APP_SECRET` — random private server secret
- `WEB_APP_URL` — GitHub Pages URL of the Mini App
- `INIT_DATA_MAX_AGE` — optional, default 86400

Never commit `.env` or real secrets to GitHub.
