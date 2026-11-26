# TRADO AI v4.0

Educational market-data explorer and AI market-learning assistant.

## Features
- Streamlit dark dashboard
- Optional Twelve Data read-only market feed
- Interactive candlestick chart
- EMA 20, EMA 50 and RSI 14
- OpenAI Responses API educational assistant
- No broker login, no order placement, no live-money trading

## Deploy
1. Upload `app.py`, `requirements.txt`, and `README.md` to GitHub.
2. Deploy the repository on Streamlit Community Cloud with main file `app.py`.
3. Open App settings → Secrets and add:

```toml
OPENAI_API_KEY = "your-private-openai-api-key"
OPENAI_MODEL = "gpt-5.5"
TWELVE_DATA_API_KEY = "your-private-twelve-data-key"
```

The Twelve Data key is optional. The AI Analyst requires an OpenAI API key.

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

For local use, place the same TOML settings in `.streamlit/secrets.toml`.
Never commit real secrets to GitHub.

## Important
This is an educational application. AI output may be incorrect and is not financial advice.
The app does not connect to brokers, collect broker credentials, or execute orders.
Market data depends on provider availability, instrument coverage and plan limits.

## API documentation
- OpenAI Responses API: https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI Python SDK: https://developers.openai.com/api/docs/libraries
- Twelve Data: https://twelvedata.com/docs
