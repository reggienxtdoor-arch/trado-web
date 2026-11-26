
import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# TRADO AI TRADER v3.0
# ==========================================

st.set_page_config(
    page_title="TRADO AI TRADER",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SECURE CONFIGURATION
# ==========================================

def get_secret(name):
    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None

APP_USERNAME = get_secret("TRADO_APP_USERNAME")
APP_PASSWORD = get_secret("TRADO_APP_PASSWORD")
API_KEY = get_secret("TWELVE_DATA_API_KEY")

# ==========================================
# LOGIN SYSTEM
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.markdown("""
<style>
.stApp {
    background: #080e19;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #101a2a;
}
.login-box {
    background: #111e30;
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #263c54;
}
h1, h2, h3 {
    color: #ffffff !important;
}
div.stButton > button {
    background: #00d69b;
    color: #06120f;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if not APP_USERNAME or not APP_PASSWORD:
    st.error("App login credentials are not configured.")
    st.info("Add TRADO_APP_USERNAME and TRADO_APP_PASSWORD under Streamlit Secrets.")
    st.stop()

if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        st.markdown("# 🚀 TRADO AI")
        st.subheader("Intelligent Trading Platform")
        st.caption("SMART TRADING. CONTROLLED RISK.")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "LOGIN TO TRADO",
                use_container_width=True
            )

            if submitted:
                if (
                    username == APP_USERNAME
                    and password == APP_PASSWORD
                ):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

        st.caption("TRADO AI TRADER v3.0")
        st.caption("Developed by ReggieNextDoor")

    st.stop()

# ==========================================
# MARKET DATA CONNECTION
# ==========================================

@st.cache_data(ttl=60)
def get_market_data(symbol, api_key):

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": "1min",
        "outputsize": 100,
        "apikey": api_key
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        if "values" not in data:
            return None, data.get(
                "message",
                "Market data unavailable"
            )

        df = pd.DataFrame(data["values"])

        for column in ["open", "high", "low", "close"]:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df["datetime"] = pd.to_datetime(df["datetime"])

        df = df.sort_values("datetime")
        df = df.dropna()

        return df, None

    except requests.RequestException:
        return None, "Connection error. Check your internet."

    except (ValueError, KeyError):
        return None, "Unable to process market data."

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🟢 TRADO AI")
    st.caption("TRADING INTELLIGENCE")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Live Markets",
            "AI Analysis",
            "Risk Management",
            "Settings"
        ]
    )

    st.divider()

    st.success("APPLICATION ONLINE")
    st.warning("READ-ONLY MODE")

    if st.button("LOG OUT", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.caption("TRADO AI TRADER v3.0")

# ==========================================
# HEADER
# ==========================================

col1, col2 = st.columns([3, 1])

with col1:
    st.title("TRADO AI TRADER")
    st.caption("Your intelligent trading command center")

with col2:
    st.success("● CONNECTED TO APP")

st.divider()

# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.header("Trading Dashboard")

    st.info(
        "Welcome to TRADO. Your trading intelligence "
        "workspace is ready."
    )

    symbols = [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "XAU/USD"
    ]

    if API_KEY:

        cols = st.columns(3)

        for index, symbol in enumerate(symbols):
            df, error = get_market_data(symbol, API_KEY)

            with cols[index % 3]:

                st.markdown(f"### {symbol}")

                if df is not None and not df.empty:

                    price = df["close"].iloc[-1]

                    st.metric(
                        "Latest available price",
                        f"{price:.5f}"
                    )

                else:
                    st.warning("Data unavailable")

    else:
        st.warning("Market API key is not configured.")

    st.divider()

    st.subheader("Platform Status")

    a, b, c = st.columns(3)

    a.metric("Trading Environment", "Read-only")
    b.metric("Live Orders", "Disabled")
    c.metric("Broker Connection", "Not connected")

    st.caption(
        "Market data is supplied by Twelve Data. "
        "Quotes may be delayed or subject to provider limits."
    )

# ==========================================
# LIVE MARKETS
# ==========================================

elif page == "Live Markets":

    st.header("📊 Live Market Data")

    symbol = st.selectbox(
        "Choose trading instrument",
        [
            "EUR/USD",
            "GBP/USD",
            "USD/JPY",
            "AUD/USD",
            "USD/CAD",
            "XAU/USD"
        ]
    )

    if not API_KEY:
        st.error("Configure your Twelve Data API key in Secrets.")

    else:

        df, error = get_market_data(symbol, API_KEY)

        if df is not None and not df.empty:

            latest = df.iloc[-1]

            st.metric(
                f"{symbol} Latest Available Price",
                f"{latest['close']:.5f}"
            )

            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=df["datetime"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name=symbol
                )
            )

            fig.update_layout(
                template="plotly_dark",
                height=500,
                xaxis_rangeslider_visible=False,
                title=f"{symbol} Price Chart",
                paper_bgcolor="#080e19",
                plot_bgcolor="#080e19"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.caption(
                "Provider: Twelve Data | "
                "Interval: 1 minute | "
                "Historical market data"
            )

            if st.button("Refresh Market Data"):
                st.cache_data.clear()
                st.rerun()

        else:
            st.error(error)

# ==========================================
# AI ANALYSIS
# ==========================================

elif page == "AI Analysis":

    st.header("🤖 TRADO AI Analysis")

    st.info("Technical analysis workspace")

    if API_KEY:

        symbol = st.selectbox(
            "Select instrument",
            ["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD"]
        )

        df, error = get_market_data(symbol, API_KEY)

        if df is not None and len(df) >= 30:

            close = df["close"]

            ema20 = close.ewm(
                span=20,
                adjust=False
            ).mean()

            ema50 = close.ewm(
                span=50,
                adjust=False
            ).mean()

            current = close.iloc[-1]

            st.metric("Latest price", f"{current:.5f}")
            st.metric("EMA 20", f"{ema20.iloc[-1]:.5f}")
            st.metric("EMA 50", f"{ema50.iloc[-1]:.5f}")

            if ema20.iloc[-1] > ema50.iloc[-1]:
                st.success("Short-term trend: Upward")
            elif ema20.iloc[-1] < ema50.iloc[-1]:
                st.warning("Short-term trend: Downward")
            else:
                st.info("Trend: Neutral")

            st.caption(
                "Educational technical indicators, "
                "not guaranteed trading signals."
            )

        else:
            st.warning(error or "Insufficient market data.")

    else:
        st.warning("Configure the market data API first.")

# ==========================================
# RISK MANAGEMENT
# ==========================================

elif page == "Risk Management":

    st.header("🛡️ Risk Management")

    balance = st.number_input(
        "Illustrative account balance ($)",
        min_value=100.0,
        value=10000.0
    )

    risk = st.slider(
        "Hypothetical risk percentage",
        0.5,
        2.0,
        1.0,
        0.5
    )

    risk_amount = balance * risk / 100

    st.metric(
        "Illustrative risk allowance",
        f"${risk_amount:,.2f}"
    )

    st.info(
        "This is a planning calculator. "
        "It does not place orders."
    )

# ==========================================
# SETTINGS
# ==========================================

elif page == "Settings":

    st.header("⚙️ Settings")

    st.write("TRADO AI Trader v3.0")

    st.text("Developer: ReggieNextDoor")

    st.text("Market data: Twelve Data")

    st.text("Environment: Read-only")

    st.text("MT5 integration: Not connected")

    st.warning(
        "Broker credentials and live order execution "
        "are not enabled in this application."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <center>
    <h3 style="color:#00d69b">TRADO AI TRADER</h3>
    SMART TRADING. CONTROLLED RISK. BIGGER VISION.
    <br><br>
    Developed by ReggieNextDoor | Version 3.0
    </center>
    """,
    unsafe_allow_html=True
)



