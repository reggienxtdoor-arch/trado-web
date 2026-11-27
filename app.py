import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import secrets
from supabase import create_client
from openai import OpenAI

# ============================================================
# TRADO AI — AUTHENTICATED LEARNING TERMINAL
# Real user authentication via Supabase.
# Broker connection and live trading are not included.
# ============================================================

st.set_page_config(
    page_title="TRADO AI | Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- CSS ---------------------------
# Keep every CSS rule inside this triple-quoted Python string.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --bg:#080d13; --panel:#111923; --line:#263342; --text:#edf4fa; --muted:#91a1b2; --teal:#19d6b4; }
html, body, [class*="css"] { font-family:'Inter',sans-serif; }
.stApp {
  background:radial-gradient(circle at 15% 0%,rgba(25,214,180,.09),transparent 30%),
  radial-gradient(circle at 90% 15%,rgba(93,169,255,.08),transparent 25%),#080d13;
  color:var(--text);
}
header[data-testid="stHeader"] { background:rgba(8,13,19,.8); }
.block-container { padding-top:1.2rem; max-width:1500px; }
h1,h2,h3 { color:var(--text)!important; }
div[data-testid="stMetric"] {
  background:linear-gradient(145deg,#151f2b,#101720);
  border:1px solid #283746; padding:16px 18px; border-radius:15px;
}
div[data-testid="stMetricLabel"] { color:#91a1b2!important; }
div[data-testid="stMetricValue"] { color:#edf4fa!important; }
div.stButton>button,div.stFormSubmitButton>button {
  background:linear-gradient(100deg,#13bfa5,#168caa); color:#04110f;
  border:0; border-radius:10px; font-weight:800; min-height:42px;
}
div[data-testid="stTextInput"] input {
  background:#0e1721; color:#edf4fa; border:1px solid #304153; border-radius:10px;
}
.trado-card {
  background:linear-gradient(145deg,rgba(21,31,43,.98),rgba(13,20,29,.98));
  border:1px solid #263342; border-radius:16px; padding:18px; margin-bottom:12px;
}
.trado-brand {
  font-size:1.8rem; font-weight:800; letter-spacing:.13em;
  background:linear-gradient(90deg,#eafefa,#19d6b4,#5da9ff);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.trado-kicker { color:#19d6b4; font-size:.72rem; letter-spacing:.22em; font-weight:800; }
.trado-intro-overlay {
  position:fixed; inset:0; z-index:999999; display:flex; align-items:center;
  justify-content:center; flex-direction:column; text-align:center;
  background:radial-gradient(ellipse at 50% 42%,#123b42 0%,#0a1c28 38%,#05090e 78%,#020407 100%);
  animation:tradoIntroFade 5.5s ease forwards; pointer-events:none;
}
.trado-intro-logo {
  font-size:clamp(2.5rem,8vw,6rem); font-weight:800; letter-spacing:.18em;
  color:#effffb; text-shadow:0 0 18px #19d6b4,0 0 55px rgba(25,214,180,.55);
  animation:tradoLogoEnter 1.2s ease-out both;
}
.trado-intro-sub { color:#a9c8ca; letter-spacing:.3em; font-size:.75rem; margin-top:14px; }
.trado-orb {
  width:90px; height:90px; border-radius:50%; border:1px solid #19d6b4;
  box-shadow:0 0 22px #19d6b4,inset 0 0 22px rgba(25,214,180,.3);
  margin-bottom:30px; animation:tradoOrb 2s ease-in-out infinite;
}
@keyframes tradoIntroFade { 0%,78%{opacity:1;visibility:visible} 100%{opacity:0;visibility:hidden} }
@keyframes tradoLogoEnter { 0%{opacity:0;transform:scale(.82) rotate(-4deg);filter:blur(12px)} 100%{opacity:1;transform:scale(1) rotate(0);filter:blur(0)} }
@keyframes tradoOrb { 0%,100%{transform:scale(.94);box-shadow:0 0 18px #19d6b4} 50%{transform:scale(1.08);box-shadow:0 0 48px #19d6b4} }
</style>
""", unsafe_allow_html=True)

# -------------------------- SECRETS --------------------------
def get_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        return create_client(url, key)
    except Exception:
        return None

supabase = get_supabase()

# ------------------------ SESSION STATE ----------------------
for key, default in {
    "intro_seen": False,
    "user_email": "",
    "authenticated": False,
    "auth_session": None,
    "auth_tab": "Sign in",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Process OAuth return code, if present.
if supabase is not None:
    try:
        oauth_code = st.query_params.get("code")
        if oauth_code:
            auth_result = supabase.auth.exchange_code_for_session({"auth_code": oauth_code})
            st.session_state.auth_session = auth_result.session
            st.session_state.user_email = auth_result.user.email or ""
            st.session_state.authenticated = True
            st.query_params.clear()
            st.rerun()
    except Exception as exc:
        st.error("Could not complete the sign-in redirect. Please try signing in again.")
        st.caption("Check the Supabase redirect URL configuration.")

# --------------------------- INTRO ---------------------------
if not st.session_state.intro_seen:
    st.markdown("""
    <div class="trado-intro-overlay">
      <div class="trado-orb"></div>
      <div class="trado-intro-logo">TRADO AI</div>
      <div class="trado-intro-sub">MARKET INTELLIGENCE TERMINAL</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(5.6)
    st.session_state.intro_seen = True
    st.rerun()

# --------------------------- AUTH UI -------------------------
if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.15, 1])
    with center:
        st.markdown('<div class="trado-card">', unsafe_allow_html=True)
        st.markdown('<div class="trado-kicker">SECURE ACCOUNT ACCESS</div>', unsafe_allow_html=True)
        st.markdown('<div class="trado-brand">TRADO AI</div>', unsafe_allow_html=True)
        st.subheader("Welcome back")
        st.caption("Sign in to your TRADO AI account. Your Google or Apple password is never entered here.")

        if supabase is None:
            st.error("Authentication is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit Secrets.")
        else:
            tab_login, tab_signup, tab_reset = st.tabs(["Sign in", "Create account", "Reset password"])

            with tab_login:
                with st.form("email_login"):
                    email = st.text_input("Email address", key="login_email")
                    password = st.text_input("TRADO AI password", type="password", key="login_password")
                    submitted = st.form_submit_button("Sign in with email", use_container_width=True)
                if submitted:
                    try:
                        result = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
                        st.session_state.auth_session = result.session
                        st.session_state.user_email = result.user.email or email.strip()
                        st.session_state.authenticated = True
                        st.rerun()
                    except Exception:
                        st.error("Sign-in failed. Check your email and password, then try again.")

                st.divider()
                st.markdown("**Or continue with**")
                col_google, col_apple = st.columns(2)
                with col_google:
                    if st.button("Continue with Google", use_container_width=True):
                        try:
                            result = supabase.auth.sign_in_with_oauth({
                                "provider": "google",
                                "options": {"redirect_to": st.get_option("server.address") or ""}
                            })
                            st.markdown(
                                f'<meta http-equiv="refresh" content="0;url={result.url}">',
                                unsafe_allow_html=True,
                            )
                            st.link_button("Continue to Google", result.url, use_container_width=True)
                        except Exception:
                            st.error("Google sign-in is not enabled in your Supabase authentication settings.")
                with col_apple:
                    if st.button("Continue with Apple", use_container_width=True):
                        try:
                            result = supabase.auth.sign_in_with_oauth({
                                "provider": "apple",
                                "options": {"redirect_to": st.get_option("server.address") or ""}
                            })
                            st.link_button("Continue to Apple", result.url, use_container_width=True)
                        except Exception:
                            st.error("Apple sign-in is not enabled in your Supabase authentication settings.")

            with tab_signup:
                st.caption("Create a TRADO AI account using an email and a new TRADO AI password.")
                with st.form("email_signup"):
                    new_email = st.text_input("Email address", key="signup_email")
                    new_password = st.text_input("Create password", type="password", key="signup_password")
                    confirm_password = st.text_input("Confirm password", type="password")
                    create = st.form_submit_button("Create account", use_container_width=True)
                if create:
                    if len(new_password) < 8:
                        st.error("Use a password with at least 8 characters.")
                    elif new_password != confirm_password:
                        st.error("The passwords do not match.")
                    else:
                        try:
                            supabase.auth.sign_up({"email": new_email.strip(), "password": new_password})
                            st.success("Account request submitted. Check your email for the verification link or code.")
                        except Exception:
                            st.error("Account creation failed. Check the email address or try again.")

            with tab_reset:
                with st.form("password_reset"):
                    reset_email = st.text_input("Account email")
                    reset = st.form_submit_button("Send password reset email", use_container_width=True)
                if reset:
                    try:
                        supabase.auth.reset_password_for_email(reset_email.strip())
                        st.success("If the account exists, a password reset email has been sent.")
                    except Exception:
                        st.error("Could not send the reset email. Check your Supabase email settings.")

        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ------------------------ DASHBOARD --------------------------
head_left, head_right = st.columns([3, 1])
with head_left:
    st.markdown('<div class="trado-brand">TRADO AI</div>', unsafe_allow_html=True)
    st.caption("MARKET INTELLIGENCE • LEARNING WORKSPACE")
with head_right:
    st.caption(f"Signed in: {st.session_state.user_email}")
    if st.button("Sign out", use_container_width=True):
        try:
            if supabase is not None:
                supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.authenticated = False
        st.session_state.auth_session = None
        st.session_state.user_email = ""
        st.rerun()

st.divider()
st.sidebar.markdown("## TRADO AI")
st.sidebar.caption("Market learning workspace")
page = st.sidebar.radio("Navigation", [
    "Overview", "Market Explorer", "AI Learning Assistant", "Trading Principles", "Account"
])
st.sidebar.divider()
st.sidebar.markdown("**Broker status**")
st.sidebar.warning("Not connected")
st.sidebar.caption("No broker password or trading credentials are collected.")

# ----------------------- SAMPLE CHART DATA --------------------
@st.cache_data
def build_sample_data():
    rng = np.random.default_rng(24)
    dates = pd.date_range(end=datetime.now(), periods=120, freq="h")
    close = 1.085 + np.cumsum(rng.normal(0.0001, 0.005, len(dates)))
    open_price = np.r_[close[0], close[:-1]]
    high = np.maximum(open_price, close) + rng.uniform(0.0002, 0.0015, len(dates))
    low = np.minimum(open_price, close) - rng.uniform(0.0002, 0.0015, len(dates))
    frame = pd.DataFrame({
        "Open": open_price, "High": high, "Low": low, "Close": close
    }, index=dates)
    frame["EMA 20"] = frame["Close"].ewm(span=20, adjust=False).mean()
    frame["EMA 50"] = frame["Close"].ewm(span=50, adjust=False).mean()
    delta = frame["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    frame["RSI 14"] = 100 - (100 / (1 + rs))
    return frame

market = build_sample_data()
last = market.iloc[-1]
prior = market.iloc[-2]
pct = (last["Close"] / prior["Close"] - 1) * 100

if page == "Overview":
    st.subheader("Market overview")
    st.caption("The chart below uses generated sample data, not live quotes.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Workspace", "Active", "Account signed in")
    m2.metric("Sample EUR/USD", f"{last['Close']:.5f}", f"{pct:+.2f}%")
    m3.metric("EMA 20", f"{last['EMA 20']:.5f}")
    m4.metric("RSI 14", f"{last['RSI 14']:.1f}" if pd.notna(last["RSI 14"]) else "—")

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=market.index, open=market["Open"], high=market["High"],
        low=market["Low"], close=market["Close"], name="Sample candles"
    ))
    fig.add_trace(go.Scatter(x=market.index, y=market["EMA 20"], name="EMA 20"))
    fig.add_trace(go.Scatter(x=market.index, y=market["EMA 50"], name="EMA 50"))
    fig.update_layout(
        template="plotly_dark", height=470, xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#080d13",
        margin=dict(l=10, r=10, t=20, b=10), legend_orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown('<div class="trado-card"><b>Market watch</b><p>Sample instruments • illustrative values only</p></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Instrument": ["EUR/USD", "GBP/USD", "USD/JPY", "GOLD"],
            "Feed": ["Sample data"] * 4,
            "Connection": ["Local simulation"] * 4
        }), use_container_width=True, hide_index=True)
    with right:
        st.markdown('<div class="trado-card"><b>Broker indicators</b><p>MetaTrader 5: Not connected</p><p>Exness: Not connected</p><p>Broker integration is not enabled in this version.</p></div>', unsafe_allow_html=True)

elif page == "Market Explorer":
    st.subheader("Market Explorer")
    st.info("Explore generated sample prices. These are not real-time market data.")
    st.line_chart(market[["Close", "EMA 20", "EMA 50"]], height=380)
    st.line_chart(market[["RSI 14"]], height=200)
    st.dataframe(market.tail(15).round(5), use_container_width=True)

elif page == "AI Learning Assistant":
    st.subheader("TRADO AI Learning Assistant")
    st.caption("AI explanations for learning market concepts only. It does not issue buy/sell calls, price predictions, or personalized financial instructions.")
    lesson = st.selectbox("Select a learning topic", [
        "EMA 20 and EMA 50", "RSI 14", "Candlestick charts",
        "Market volatility", "Risk management", "Support and resistance",
        "Trading psychology", "Economic news"
    ])
    lessons = {
        "EMA 20 and EMA 50": "An EMA gives more weight to recent prices. A 20-period EMA reacts faster than a 50-period EMA. Comparing them can help learners study trend behaviour, but a crossover does not guarantee a future move.",
        "RSI 14": "RSI is a momentum indicator commonly displayed from 0 to 100. Levels around 70 and 30 are often studied as potential momentum extremes, not automatic buy or sell instructions.",
        "Candlestick charts": "Each candle summarizes open, high, low and close values for a time interval. The body compares open and close; the wicks show the interval's high and low.",
        "Market volatility": "Volatility describes the degree of price variation over time. Higher volatility means larger or faster price changes may occur, without revealing their direction.",
        "Risk management": "Risk management is the study of uncertainty and ways to limit exposure. Leverage can magnify losses as well as gains; no indicator removes market risk.",
        "Support and resistance": "Support and resistance are chart-analysis concepts describing areas where price has previously paused or changed direction. They are zones of interest, not guaranteed barriers.",
        "Trading psychology": "Trading psychology studies how emotions, expectations and cognitive biases can affect financial decisions. A written learning journal can help identify patterns in reasoning.",
        "Economic news": "Economic releases can affect markets because they change expectations. The direction and size of any reaction are uncertain and depend on context."
    }
    st.markdown(f'<div class="trado-card"><b>{lesson}</b><p>{lessons[lesson]}</p></div>', unsafe_allow_html=True)
    user_question = st.text_area("Ask TRADO AI to explain a market-learning concept", placeholder="Example: What is the difference between EMA and SMA?")
    if st.button("Ask AI", use_container_width=True):
        if not user_question.strip():
            st.warning("Enter a question first.")
        else:
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
                model_name = st.secrets.get("OPENAI_MODEL", "gpt-5.5")
                client = OpenAI(api_key=api_key)
                response = client.responses.create(
                    model=model_name,
                    instructions=(
                        "You are TRADO AI, an educational market-literacy tutor. "
                        "Explain concepts clearly for a beginner. You may explain indicators, "
                        "candles, market structure, volatility, risk concepts and trading history. "
                        "Do not provide personalized financial advice, buy/sell/hold instructions, "
                        "price targets, signals, leverage settings, broker login guidance, or "
                        "instructions to place real-money trades. Do not claim to predict markets. "
                        "If asked for a trade recommendation, politely redirect to general education."
                    ),
                    input=user_question.strip(),
                )
                st.markdown('<div class="trado-card">', unsafe_allow_html=True)
                st.markdown("**TRADO AI explanation**")
                st.write(response.output_text)
                st.markdown("</div>", unsafe_allow_html=True)
            except KeyError:
                st.error("AI is not configured. Add OPENAI_API_KEY to Streamlit Secrets.")
            except Exception:
                st.error("The AI service could not respond. Check the API key, model setting and usage limits.")

elif page == "Trading Principles":
    st.subheader("Trading principles")
    for title, detail in [
        ("Learn the mechanics", "Understand spreads, fees, order types, market hours and volatility."),
        ("Indicators are not guarantees", "Technical indicators summarize past price behaviour; they cannot ensure a result."),
        ("Respect uncertainty", "Markets can move unexpectedly. Leverage can magnify losses."),
        ("Keep a learning journal", "Write down what you studied, the evidence and what could challenge your assumptions."),
        ("Review the process", "A single outcome does not prove that a decision process was sound.")
    ]:
        st.markdown(f'<div class="trado-card"><b>{title}</b><p>{detail}</p></div>', unsafe_allow_html=True)
    st.warning("This is educational content, not financial advice or a trading service.")

elif page == "Account":
    st.subheader("Account")
    st.write("Authenticated email:", st.session_state.user_email)
    st.write("Authentication provider: Supabase Auth")
    st.write("Broker connection: Disabled")
    st.write("Live trading: Not available")
    st.caption("Your TRADO AI account password is managed by Supabase Authentication. Never share it in chat or commit it to GitHub.")

st.divider()
st.caption(
    "TRADO AI provides market education and sample visualizations. "
    "It does not connect to Exness or MetaTrader 5, accept broker credentials, "
    "place orders, or provide individualized investment instructions."
)
