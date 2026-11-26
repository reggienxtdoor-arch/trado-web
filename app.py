import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from openai import OpenAI

st.set_page_config(page_title="TRADO AI v4.0", page_icon="📈", layout="wide")

def get_secret(key, default=""):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

OPENAI_KEY = get_secret("OPENAI_API_KEY")
OPENAI_MODEL = get_secret("OPENAI_MODEL", "gpt-5.5")
DATA_KEY = get_secret("TWELVE_DATA_API_KEY")

st.markdown("""
<style>
.stApp{background:#07111f;color:#eef5ff}
[data-testid="stSidebar"]{background:#0b1727}
div[data-testid="stMetric"]{background:#122238;border:1px solid #29405b;padding:14px;border-radius:14px}
div.stButton>button{background:#19d6a0;color:#04130f;border:0;border-radius:9px;font-weight:700}
h1,h2,h3{letter-spacing:-.03em}
.brand{color:#19d6a0;font-size:29px;font-weight:900;letter-spacing:3px}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60, show_spinner=False)
def market_data(symbol, key):
    if not key:
        return None, "Market-data key is not configured."
    try:
        r = requests.get(
            "https://api.twelvedata.com/time_series",
            params={"symbol": symbol, "interval": "5min", "outputsize": 100, "apikey": key},
            timeout=20,
        )
        r.raise_for_status()
        payload = r.json()
        if "values" not in payload:
            return None, payload.get("message", "No data returned.")
        df = pd.DataFrame(payload["values"])
        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df = df.dropna().sort_values("datetime").reset_index(drop=True)
        return (df, None) if not df.empty else (None, "No usable price data.")
    except requests.RequestException as e:
        return None, f"Network/provider error: {type(e).__name__}"
    except Exception:
        return None, "Could not process market-data response."

def indicators(df):
    d = df.copy()
    d["EMA20"] = d.close.ewm(span=20, adjust=False).mean()
    d["EMA50"] = d.close.ewm(span=50, adjust=False).mean()
    delta = d.close.diff()
    up = delta.clip(lower=0).rolling(14).mean()
    down = (-delta.clip(upper=0)).rolling(14).mean()
    rs = up / down.replace(0, pd.NA)
    d["RSI14"] = 100 - 100 / (1 + rs)
    return d

def make_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.datetime, open=df.open, high=df.high,
        low=df.low, close=df.close, name=symbol
    ))
    fig.add_trace(go.Scatter(x=df.datetime, y=df.EMA20, name="EMA 20",
                             line=dict(color="#19d6a0", width=1.5)))
    fig.add_trace(go.Scatter(x=df.datetime, y=df.EMA50, name="EMA 50",
                             line=dict(color="#f2b84b", width=1.5)))
    fig.update_layout(template="plotly_dark", height=480,
                      paper_bgcolor="#07111f", plot_bgcolor="#07111f",
                      xaxis_rangeslider_visible=False)
    return fig

with st.sidebar:
    st.markdown('<div class="brand">TRADO AI</div>', unsafe_allow_html=True)
    st.caption("MARKET INTELLIGENCE LAB")
    page = st.radio("WORKSPACE", ["Overview", "Market Explorer", "AI Analyst", "Learn", "Settings"])
    st.divider()
    st.success("EDUCATIONAL DEMO MODE")
    st.caption("No broker connection • No order execution")

st.title("TRADO AI v4.0")
st.caption("Understand markets. Explore data. Learn with AI.")
st.warning("Educational demo only. No investment recommendations, broker connection, or trading execution.")

if page == "Overview":
    st.subheader("Market research command centre")
    a,b,c,d = st.columns(4)
    a.metric("AI engine", "Ready" if OPENAI_KEY else "Needs API key")
    b.metric("Market feed", "Ready" if DATA_KEY else "Optional key missing")
    c.metric("Broker connection", "Disabled")
    d.metric("Order execution", "Disabled")
    st.markdown("### What TRADO can do")
    st.write("- Explain market concepts using an AI model.\n- Display provider-supplied historical candles.\n- Calculate EMA 20, EMA 50 and RSI 14.\n- Help users learn how indicators work and where they can fail.")
    st.info("This app has no function to place real or simulated broker orders.")

elif page == "Market Explorer":
    st.subheader("Market Explorer")
    choices = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "XAU/USD"]
    symbol = st.selectbox("Instrument", choices)
    if st.button("Load / refresh data"):
        market_data.clear()
    with st.spinner("Requesting provider data..."):
        df, error = market_data(symbol, DATA_KEY)
    if df is None:
        st.info(error)
        st.caption("Market Explorer requires a configured Twelve Data key.")
    else:
        df = indicators(df)
        last = df.iloc[-1]
        x,y,z = st.columns(3)
        x.metric("Latest returned close", f"{last.close:.5f}")
        y.metric("EMA 20", f"{last.EMA20:.5f}")
        z.metric("EMA 50", f"{last.EMA50:.5f}")
        st.plotly_chart(make_chart(df, symbol), use_container_width=True)
        st.caption(f"Twelve Data • 5-minute interval • Latest returned candle: {last.datetime}")
        st.dataframe(df[["datetime","open","high","low","close","EMA20","EMA50","RSI14"]].tail(12),
                     use_container_width=True, hide_index=True)

elif page == "AI Analyst":
    st.subheader("🧠 TRADO AI Analyst")
    st.caption("Ask for educational explanations of indicators, market structure, and financial terminology.")
    if not OPENAI_KEY:
        st.error("Add OPENAI_API_KEY in Streamlit Community Cloud → App settings → Secrets.")
    else:
        question = st.text_area("Ask TRADO AI", placeholder="Explain how EMA 20 and EMA 50 differ.")
        if st.button("Ask TRADO AI", type="primary") and question.strip():
            try:
                client = OpenAI(api_key=OPENAI_KEY)
                response = client.responses.create(
                    model=OPENAI_MODEL,
                    instructions=(
                        "You are TRADO AI, an educational market-learning assistant. "
                        "Explain concepts clearly and cautiously. Do not provide personalized financial advice, "
                        "buy/sell recommendations, trade entries/exits, leverage suggestions, or profit promises. "
                        "Do not claim to have live market data unless data is explicitly supplied. "
                        "Explain uncertainty and limitations. This app is demo-only and cannot execute trades."
                    ),
                    input=question.strip(),
                    max_output_tokens=700,
                )
                st.session_state["last_ai_answer"] = response.output_text
                st.session_state["last_ai_question"] = question.strip()
            except Exception as e:
                st.error(f"AI request failed ({type(e).__name__}). Check your API key, model access and API billing.")
        if st.session_state.get("last_ai_answer"):
            st.markdown("### TRADO AI response")
            st.markdown(st.session_state["last_ai_answer"])
            with st.expander("Your question"):
                st.write(st.session_state.get("last_ai_question", ""))

elif page == "Learn":
    st.subheader("Market learning library")
    with st.expander("Candlesticks"):
        st.write("A candlestick shows open, high, low and close prices for a time interval. It describes past data, not the future.")
    with st.expander("Exponential moving average (EMA)"):
        st.write("An EMA weights recent observations more heavily. It can help describe a trend, but it lags price and can mislead in sideways markets.")
    with st.expander("Relative Strength Index (RSI)"):
        st.write("RSI is a momentum oscillator often displayed from 0 to 100. Common thresholds are not automatic instructions to buy or sell.")
    with st.expander("Risk and uncertainty"):
        st.write("Prices can move unpredictably. Leverage, volatility, spreads, fees and gaps can magnify losses. This project is restricted to education and data viewing.")

elif page == "Settings":
    st.subheader("Configuration & security")
    st.write("Add keys in Streamlit Community Cloud → your app → Settings → Secrets.")
    st.code('OPENAI_API_KEY = "your-private-key"\nOPENAI_MODEL = "gpt-5.5"\nTWELVE_DATA_API_KEY = "optional-private-data-key"', language="toml")
    st.write(f"OpenAI key: {'Configured' if OPENAI_KEY else 'Missing'}")
    st.write(f"Market data key: {'Configured' if DATA_KEY else 'Missing (optional)'}")
    st.write(f"Model: {OPENAI_MODEL}")
    st.error("Never commit API keys to GitHub. This app does not collect broker passwords.")

st.divider()
st.caption("TRADO AI v4.0 • Educational demo • No broker login • No trade execution")
