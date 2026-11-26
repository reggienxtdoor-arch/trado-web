
import streamlit as st
import pandas as pd
import random
from datetime import datetime
#DEMO DATA ONLY
# ==========================================
# TRADO AI TRADER | VERSION 2.0
# ==========================================

st.set_page_config(
    page_title="TRADO AI Trader",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# TWELVE DATA - LIVE FOREX CONNECTION
# ==========================================

import requests
import pandas as pd
import streamlit as st

try:
    API_KEY = st.secrets["TWELVE_DATA_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = None

@st.cache_data(ttl=30)
def get_market_data(symbol, api_key):
    if not api_key:
        return None, "API key not configured."

    try:
        response = requests.get(
            "https://api.twelvedata.com/time_series",
            params={
                "symbol": symbol,
                "interval": "1min",
                "outputsize": 50,
                "apikey": api_key
            },
            timeout=15
        )

        response.raise_for_status()
        result = response.json()

        if "values" not in result:
            return None, result.get(
                "message",
                result.get("status", "Market data unavailable.")
            )

        df = pd.DataFrame(result["values"])

        df["datetime"] = pd.to_datetime(df["datetime"])
        df["close"] = pd.to_numeric(df["close"])

        df = df.sort_values("datetime")

        return df, None

    except requests.RequestException:
        return None, "Network connection failed."
    except (ValueError, KeyError):
        return None, "Could not process market data."

# Fetch actual EUR/USD data
chart_data, market_error = get_market_data(
    "EUR/USD", API_KEY
)


# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #080d17;
    color: #e8edf5;
}
[data-testid="stSidebar"] {
    background: #0c1422;
    border-right: 1px solid #1b2b3e;
}
h1, h2, h3 {
    color: #f3f6fc !important;
}
p, label {
    color: #aab7c8;
}
.metric-card {
    background: linear-gradient(135deg,#142238,#0d1727);
    border: 1px solid #233850;
    padding: 20px;
    border-radius: 13px;
    min-height: 115px;
}
.metric-label {
    color: #91a5bb;
    font-size: 13px;
}
.metric-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
}
.green {
    color: #00e6a0;
}
.red {
    color: #ff657a;
}
.panel {
    background: #101b2b;
    border: 1px solid #22344b;
    padding: 20px;
    border-radius: 13px;
}
.brand {
    color: #00e6a0;
    font-size: 29px;
    font-weight: 900;
    letter-spacing: 2px;
}
.small-text {
    color: #8093aa;
    font-size: 12px;
}
div.stButton > button {
    background: #00c98b;
    color: #06130f;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #00e6a0;
    color: #06130f;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown('<div class="brand">TRADO AI</div>',
                unsafe_allow_html=True)
    st.caption("INTELLIGENT TRADING PLATFORM")

    st.markdown("---")

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Market Analysis",
            "AI Signals",
            "Trade History",
            "Risk Management",
            "Settings"
        ]
    )

    st.markdown("---")
    st.success("● SYSTEM ONLINE")
    st.warning("DEMO MODE ACTIVE")

    st.markdown("---")
    st.caption("TRADO AI TRADER v2.0")
    st.caption("Developed by ReggieNextDoor")

# ==========================================
# HEADER
# ==========================================

c1, c2 = st.columns([3, 1])

with c1:
    st.markdown("# TRADO AI TRADER")
    st.caption("Your intelligent market analysis command center")

with c2:
    st.markdown("### 🟢 DEMO ACCOUNT")
    st.caption(datetime.now().strftime("%d %b %Y | %H:%M"))

st.markdown("---")

# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.subheader("Account Overview")

    cols = st.columns(4)

    cards = [
        ("ACCOUNT BALANCE", "$10,000.00", "Demo funds"),
        ("EQUITY", "$10,000.00", "Simulated account"),
        ("OPEN TRADES", "0", "No active positions"),
        ("DAILY P/L", "$0.00", "Simulated result")
    ]

    for col, (label, value, note) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="small-text">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## Market Overview")

    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### EUR/USD Price Chart")
        st.caption("Illustrative simulated price data")

        st.line_chart(
    chart_data,
    height=320
)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("### Market Watch")

        markets = [
            ("EUR/USD", "1.08500", "+0.24%"),
            ("GBP/USD", "1.27100", "+0.18%"),
            ("USD/JPY", "150.250", "-0.12%"),
            ("AUD/USD", "0.65400", "+0.31%"),
            ("XAU/USD", "2650.00", "-0.08%")
        ]
st.markdown("### EUR/USD LIVE MARKET CHART")

if chart_data is not None and not chart_data.empty:

    latest_price = float(chart_data["close"].iloc[-1])

    st.metric(
        "Latest EUR/USD Price",
        f"{latest_price:.5f}"
    )

    chart = chart_data.set_index("datetime")[["close"]]

    st.line_chart(chart)

    st.caption(
        "Source: Twelve Data | "
        "1-minute interval | Last 50 data points"
    )

    if st.button("Refresh Market Data"):
        st.cache_data.clear()
        st.rerun()

else:
    st.warning(
        "Market data is unavailable. "
        "Check your API key and internet connection."
    )


        for name, price, change in markets:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:10px">
                <b>{name}</b><br>
                <span style="font-size:20px">{price}</span>
                <span class="small-text">{change}</span>
            </div>
            """, unsafe_allow_html=True)

        st.caption("All market figures are illustrative.")

    st.markdown("## AI Trading Intelligence")

    a, b = st.columns(2)

    with a:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Market Status")
        st.success("Analysis interface online")
        st.write("Signal engine: Development mode")
        st.write("Market feed: Not connected")
        st.markdown('</div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 🛡️ Risk Protection")
        st.info("Demo trading only")
        st.write("Live execution: Disabled")
        st.write("Risk controls: Configuration pending")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MARKET ANALYSIS
# ==========================================

elif page == "Market Analysis":

    st.title("📊 Market Analysis")
    st.caption("Illustrative market analysis workspace")

    market = st.selectbox(
        "Select market",
        ["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD"]
    )

    st.subheader(market)
    st.line_chart(chart_data, height=350)

    st.info("Connect a verified market data provider to display live prices.")

# ==========================================
# AI SIGNALS
# ==========================================

elif page == "AI Signals":

    st.title("🤖 TRADO AI Signals")

    st.info("Signal engine is currently in development.")

    st.markdown("""
    | Feature | Status |
    |---|---|
    | Trend detection | Development |
    | Moving averages | Planned |
    | RSI analysis | Planned |
    | MACD analysis | Planned |
    | Signal validation | Planned |
    """)

    st.warning("No real BUY or SELL recommendations are generated.")

# ==========================================
# TRADE HISTORY
# ==========================================

elif page == "Trade History":

    st.title("📜 Trade History")
    st.info("No simulated trades have been recorded yet.")

    history = pd.DataFrame(
        columns=["Date", "Symbol", "Direction", "Entry", "Exit", "P/L"]
    )

    st.dataframe(history, use_container_width=True)

# ==========================================
# RISK MANAGEMENT
# ==========================================

elif page == "Risk Management":

    st.title("🛡️ Risk Management")

    st.write("Configure your demo risk-management preferences.")

    risk = st.slider(
        "Demo risk limit (%)",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.5
    )

    balance = st.number_input(
        "Illustrative account balance ($)",
        min_value=100.0,
        value=10000.0
    )

    st.metric(
        "Illustrative risk allowance",
        f"${balance * risk / 100:,.2f}"
    )

    st.caption("This is a planning calculation, not an order or trade.")

# ==========================================
# SETTINGS
# ==========================================

elif page == "Settings":

    st.title("⚙️ Platform Settings")

    st.text_input("Platform name", "TRADO AI Trader")
    st.text_input("Developer", "ReggieNextDoor")

    st.selectbox(
        "Trading environment",
        ["Demo only"]
    )

    st.selectbox(
        "Broker integration",
        ["Not connected", "MetaTrader 5 - planned"]
    )

    st.warning("Live trading is unavailable in this version.")

    st.button("Save demo preferences")

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<center>
<b style="color:#00e6a0">TRADO AI TRADER</b><br>
<span style="color:#8292a8">
Built with vision. Driven by innovation. Designed with discipline.
<br>Version 2.0 | ReggieNextDoor
</span>
</center>
""", unsafe_allow_html=True)


