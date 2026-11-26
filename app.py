import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from openai import OpenAI

st.set_page_config(page_title="TRADO AI v7.0", page_icon="📈", layout="wide")

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
@keyframes tradoIntroFade {
    0%, 94% {
        opacity: 1;
        visibility: visible;
    }
    100% {
        opacity: 0;
        visibility: hidden;
    }
}

/* Put the rest of your CSS here */

.trado-intro-overlay {
    position: fixed;
    inset: 0;
    z-index: 999999;
}
</style>
""", unsafe_allow_html=True)
:root{--bg:#090b10;--panel:#11151d;--panel2:#151b24;--line:#252d38;--mint:#19d6a0;--muted:#8995a5}
.stApp{background:radial-gradient(ellipse at 78% 0%,#132b2b 0%,#090b10 42%);color:#eef4f8}
[data-testid="stSidebar"]{background:#0c1017;border-right:1px solid #202833}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#9ba8b6}
div[data-testid="stMetric"]{background:linear-gradient(145deg,#151c25,#10151c);border:1px solid #28323e;padding:16px 18px;border-radius:15px;min-height:108px}
div[data-testid="stMetric"] label{color:#8d9aaa!important;font-size:11px!important}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#f4f7fa;font-weight:750}
div.stButton>button{background:linear-gradient(90deg,#17d49b,#20e4b0);color:#04130f;border:0;border-radius:9px;font-weight:800;min-height:40px}
div.stButton>button:hover{background:#6af3cb;color:#06140f;border:0}
h1,h2,h3{letter-spacing:-.035em}
h1{font-size:27px!important}
h2{font-size:21px!important}
h3{font-size:15px!important;color:#dce7ed}
.brand{color:#19d6a0;font-size:25px;font-weight:950;letter-spacing:3px}
[data-testid="stVerticalBlockBorderWrapper"]{background:#11151d;border-color:#27313c;border-radius:15px}
[data-testid="stDataFrame"]{border:1px solid #28323e;border-radius:12px;overflow:hidden}
.stTabs [data-baseweb="tab-list"]{gap:9px}
.stTabs [data-baseweb="tab"]{background:#151b24;border-radius:8px;padding:7px 14px}
.stTabs [aria-selected="true"]{background:#15372f!important;color:#28e5ae!important}
small,.stCaption{color:#8492a1}

.dashboard-top{display:flex;align-items:center;justify-content:space-between;padding:5px 2px 18px;border-bottom:1px solid #202833;margin-bottom:20px}
.dash-kicker{font-size:10px;letter-spacing:2px;color:#19d6a0;font-weight:800}
.dash-title{font-size:25px;font-weight:800;color:#f4f7fa;margin-top:4px}
.dash-sub{font-size:12px;color:#83909e;margin-top:4px}
.panel-title{font-size:13px;font-weight:750;color:#e8eef3;margin-bottom:12px}
.panel-note{font-size:10px;color:#81909e}
.practice-balance{background:linear-gradient(145deg,#171f29,#10151d);border:1px solid #293541;border-radius:16px;padding:20px;height:100%}
.practice-value{font-size:31px;font-weight:850;letter-spacing:-1px;color:#f5f8fb;margin:8px 0}
.practice-label{font-size:11px;color:#96a4b1}
.practice-pill{display:inline-block;background:#123b31;color:#3de5b2;padding:4px 8px;border-radius:20px;font-size:10px;font-weight:800}
.activity-row{display:flex;justify-content:space-between;gap:8px;padding:9px 0;border-bottom:1px solid #202833;font-size:11px}
.activity-row:last-child{border-bottom:0}
.activity-symbol{font-weight:750;color:#dfe8ee}
.activity-meta{color:#7f8d9b;font-size:10px;margin-top:2px}
.activity-tag{color:#24d8a2;font-weight:700}
.broker-chip{border:1px solid #293641;background:#141b24;border-radius:10px;padding:11px 13px}

</style>


@keyframes tradoIntroFade {
  0%, 94% { opacity:1; visibility:visible; }
  100% { opacity:0; visibility:hidden; }
}
@keyframes tradoLogoEnter {
  0% { opacity:0; transform:scale(.18) rotate(-35deg); filter:blur(18px); }
  12% { opacity:1; transform:scale(1.12) rotate(5deg); filter:blur(0); }
  17%, 90% { opacity:1; transform:scale(1) rotate(0); }
  100% { opacity:1; }
}
@keyframes tradoOrbPulse {
  0%,100% { box-shadow:0 0 22px #19d6a055, inset 0 0 22px #19d6a022; }
  50% { box-shadow:0 0 65px #19d6a0aa, 0 0 125px #087cff66, inset 0 0 38px #19d6a044; }
}
@keyframes tradoRing {
  from { transform:rotateX(68deg) rotateZ(0deg); }
  to { transform:rotateX(68deg) rotateZ(360deg); }
}
@keyframes tradoRingReverse {
  from { transform:rotateY(68deg) rotateZ(0deg); }
  to { transform:rotateY(68deg) rotateZ(-360deg); }
}
@keyframes tradoScan {
  0% { transform:translateY(-55vh); opacity:0; }
  12%,88% { opacity:.85; }
  100% { transform:translateY(55vh); opacity:0; }
}
@keyframes tradoProgress {
  from { width:0%; }
  to { width:100%; }
}
@keyframes tradoGrid {
  from { transform:perspective(500px) rotateX(62deg) translateY(0); }
  to { transform:perspective(500px) rotateX(62deg) translateY(90px); }
}
@keyframes tradoStatus1 {
  0%,15% { opacity:0; transform:translateY(8px); }
  18%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoStatus2 {
  0%,27% { opacity:0; transform:translateY(8px); }
  30%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoStatus3 {
  0%,39% { opacity:0; transform:translateY(8px); }
  42%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoStatus4 {
  0%,51% { opacity:0; transform:translateY(8px); }
  54%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoStatus5 {
  0%,63% { opacity:0; transform:translateY(8px); }
  66%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoStatus6 {
  0%,75% { opacity:0; transform:translateY(8px); }
  78%,90% { opacity:1; transform:translateY(0); }
  100% { opacity:0; }
}
@keyframes tradoSpark {
  0% { opacity:0; transform:translate3d(0,18px,0) scale(.3); }
  30% { opacity:1; }
  100% { opacity:0; transform:translate3d(var(--dx),-110px,0) scale(1.2); }
}
@keyframes tradoTitleReveal {
  0%,9% { opacity:0; letter-spacing:22px; filter:blur(10px); }
  18%,90% { opacity:1; letter-spacing:8px; filter:blur(0); }
  100% { opacity:0; }
}
.trado-intro-overlay {
  position:fixed; inset:0; z-index:999999;
  display:flex; align-items:center; justify-content:center; flex-direction:column;
  overflow:hidden; pointer-events:none; isolation:isolate;
  background:
    radial-gradient(ellipse at 50% 42%, #123b48 0%, #0a1c2b 28%, #050b15 62%, #02040a 100%);
  animation:tradoIntroFade 42s cubic-bezier(.7,0,.2,1) forwards;
}
.trado-intro-overlay:before {
  content:""; position:absolute; inset:-40%;
  z-index:-2; opacity:.22;
  background-image:linear-gradient(#20dcb01b 1px,transparent 1px),linear-gradient(90deg,#20dcb01b 1px,transparent 1px);
  background-size:48px 48px;
  transform:perspective(500px) rotateX(62deg) scale(1.6);
  animation:tradoGrid 5s linear infinite;
  mask-image:linear-gradient(to bottom,transparent 5%,black 55%,transparent 100%);
}
.trado-intro-overlay:after {
  content:""; position:absolute; inset:0; z-index:-1;
  background:radial-gradient(ellipse at center,transparent 20%,#02050bd9 82%);
}
.trado-intro-scan {
  position:absolute; top:0; left:0; width:100%; height:2px;
  background:linear-gradient(90deg,transparent,#19d6a0,transparent);
  box-shadow:0 0 22px #19d6a0; animation:tradoScan 5s ease-in-out infinite;
}
.trado-intro-topline {
  position:absolute; top:7%; left:0; width:100%; text-align:center;
  color:#8aa7b8; font:600 10px/1.4 monospace; letter-spacing:5px;
  opacity:0; animation:tradoStatus1 42s linear forwards;
}
.trado-reactor {
  position:relative; width:190px; height:190px; display:flex;
  align-items:center; justify-content:center; margin-bottom:28px;
  animation:tradoLogoEnter 7s ease-out both;
}
.trado-reactor-core {
  width:104px; height:104px; border-radius:50%; border:1px solid #6fffe0;
  display:flex; align-items:center; justify-content:center;
  color:#dffff7; font:900 54px/1 Arial,sans-serif;
  text-shadow:0 0 24px #19d6a0;
  background:radial-gradient(circle at 35% 28%,#246b6b,#09222d 58%,#030a12);
  animation:tradoOrbPulse 2.4s ease-in-out infinite;
}
.trado-reactor-ring {
  position:absolute; inset:3px; border:1px solid #19d6a077; border-radius:50%;
  box-shadow:0 0 24px #19d6a022; animation:tradoRing 8s linear infinite;
}
.trado-reactor-ring.r2 {
  inset:17px; border-color:#4e9fff88; transform:rotateY(68deg);
  animation:tradoRingReverse 6s linear infinite;
}
.trado-reactor-ring.r3 {
  inset:-11px; border-style:dashed; border-color:#19d6a044;
  animation:tradoRingReverse 18s linear infinite;
}
.trado-intro-title {
  color:#f5fbff; font:900 clamp(30px,5vw,48px)/1 Arial,sans-serif;
  text-transform:uppercase; text-shadow:0 0 32px #19d6a055;
  animation:tradoTitleReveal 42s ease-out forwards;
}
.trado-intro-sub {
  color:#6df5d2; font:600 10px/1.6 monospace; letter-spacing:5px;
  margin-top:13px; text-align:center;
}
.trado-intro-tagline {
  color:#c0d0dc; font:400 12px/1.6 Arial,sans-serif;
  margin-top:17px; letter-spacing:2px; opacity:0;
  animation:tradoStatus2 42s linear forwards;
}
.trado-console {
  width:min(390px,82vw); margin-top:34px; padding:17px 20px;
  border:1px solid #4bd9bd44; border-radius:12px;
  background:linear-gradient(135deg,#0a1d29dd,#07111ddd);
  box-shadow:0 14px 55px #0008,inset 0 1px #ffffff0b;
  color:#b9d5dc; font:11px/1.9 monospace;
}
.trado-console-line { opacity:0; white-space:nowrap; }
.trado-console-line:nth-child(1) { animation:tradoStatus1 42s linear forwards; }
.trado-console-line:nth-child(2) { animation:tradoStatus2 42s linear forwards; }
.trado-console-line:nth-child(3) { animation:tradoStatus3 42s linear forwards; }
.trado-console-line:nth-child(4) { animation:tradoStatus4 42s linear forwards; }
.trado-console-line:nth-child(5) { animation:tradoStatus5 42s linear forwards; }
.trado-console-line:nth-child(6) { animation:tradoStatus6 42s linear forwards; }
.trado-check { color:#19d6a0; padding-right:8px; }
.trado-progress-wrap {
  height:3px; width:min(390px,82vw); margin-top:15px;
  background:#ffffff16; border-radius:10px; overflow:hidden;
}
.trado-progress {
  height:100%; width:0; background:linear-gradient(90deg,#087cff,#19d6a0,#b4ffe9);
  box-shadow:0 0 15px #19d6a0; animation:tradoProgress 39s linear 1s forwards;
}
.trado-progress-label {
  width:min(390px,82vw); display:flex; justify-content:space-between;
  color:#7996a6; font:9px/1.5 monospace; letter-spacing:2px; margin-top:9px;
}
.trado-intro-footer {
  position:absolute; bottom:6%; color:#567482;
  font:9px/1.5 monospace; letter-spacing:3px; text-align:center;
}
.trado-spark {
  position:absolute; width:4px; height:4px; border-radius:50%;
  background:#9affeb; box-shadow:0 0 12px #19d6a0;
  animation:tradoSpark 4s ease-out infinite;
}
.trado-spark.s1 { left:19%; top:58%; --dx:35px; animation-delay:.4s; }
.trado-spark.s2 { left:77%; top:54%; --dx:-28px; animation-delay:1.3s; }
.trado-spark.s3 { left:31%; top:35%; --dx:-18px; animation-delay:2.1s; }
.trado-spark.s4 { left:68%; top:32%; --dx:22px; animation-delay:2.8s; }
@media (prefers-reduced-motion: reduce) {
  .trado-intro-overlay,.trado-reactor,.trado-reactor-core,.trado-reactor-ring,
  .trado-intro-title,.trado-intro-scan,.trado-progress,.trado-spark,
  .trado-console-line,.trado-intro-tagline,.trado-intro-topline { animation:none !important; }
  .trado-intro-overlay { display:none !important; }
}
@media (prefers-reduced-motion: reduce) { .trado-intro-overlay,.trado-intro-orb,.trado-intro-title,.trado-intro-scan { animation:none !important; } }
</style>
""", unsafe_allow_html=True)

# Show the cinematic welcome only once per browser session.
if not st.session_state.get("trado_intro_seen", False):
    st.session_state["trado_intro_seen"] = True
    st.markdown(
        """
        <div class="trado-intro-overlay">
          <div class="trado-intro-scan"></div>
          <div class="trado-intro-topline">TRADO SYSTEMS • SECURE SESSION • EDUCATION MODE</div>
          <span class="trado-spark s1"></span><span class="trado-spark s2"></span>
          <span class="trado-spark s3"></span><span class="trado-spark s4"></span>
          <div class="trado-reactor">
            <div class="trado-reactor-ring"></div>
            <div class="trado-reactor-ring r2"></div>
            <div class="trado-reactor-ring r3"></div>
            <div class="trado-reactor-core">T</div>
          </div>
          <div class="trado-intro-title">TRADO AI</div>
          <div class="trado-intro-sub">MARKET INTELLIGENCE • LEARNING SYSTEM</div>
          <div class="trado-intro-tagline">Clarity in data. Confidence in learning.</div>
          <div class="trado-console">
            <div class="trado-console-line"><span class="trado-check">[ OK ]</span> Initializing TRADO interface</div>
            <div class="trado-console-line"><span class="trado-check">[ OK ]</span> Loading visual intelligence layer</div>
            <div class="trado-console-line"><span class="trado-check">[ OK ]</span> Preparing market data workspace</div>
            <div class="trado-console-line"><span class="trado-check">[ OK ]</span> Checking educational AI connection</div>
            <div class="trado-console-line"><span class="trado-check">[ OK ]</span> Applying privacy and demo safeguards</div>
            <div class="trado-console-line"><span class="trado-check">[ READY ]</span> TRADO learning environment prepared</div>
          </div>
          <div class="trado-progress-wrap"><div class="trado-progress"></div></div>
          <div class="trado-progress-label"><span>INITIALIZING</span><span>WELCOME TO TRADO</span></div>
          <div class="trado-intro-footer">NO BROKER CONNECTION &nbsp; • &nbsp; NO ORDER EXECUTION</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- AUTHENTICATION GATE ----------------
# Email one-time passcode only. No password is collected or stored.
import secrets as _secrets
import smtplib
from email.message import EmailMessage

def send_login_code(destination, code):
    host = get_secret("SMTP_HOST")
    port = int(get_secret("SMTP_PORT", "587"))
    username = get_secret("SMTP_USERNAME")
    password = get_secret("SMTP_PASSWORD")
    sender = get_secret("SMTP_FROM", username)
    if not all([host, username, password, sender]):
        return False, "Email delivery is not configured. Add SMTP settings in Streamlit Secrets."
    message = EmailMessage()
    message["Subject"] = "Your TRADO AI verification code"
    message["From"] = sender
    message["To"] = destination
    message.set_content(
        f"Your TRADO AI verification code is {code}. "
        "It expires in 10 minutes. If you did not request this, ignore this email."
    )
    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(message)
        return True, "Verification code sent."
    except Exception:
        return False, "Email delivery failed. Check your SMTP settings."

if "trado_authenticated" not in st.session_state:
    st.session_state.trado_authenticated = False

if not st.session_state.trado_authenticated:
    st.markdown("""
    <style>
    .login-shell{max-width:560px;margin:5vh auto 2vh;padding:34px;
      background:linear-gradient(145deg,#101f32,#091321);
      border:1px solid #29445d;border-radius:22px;
      box-shadow:0 22px 80px #0008}
    .login-brand{font-size:34px;font-weight:900;letter-spacing:5px;color:#19d6a0}
    .login-sub{color:#9db2c5;letter-spacing:2px;font-size:11px}
    </style>
    <div class="login-shell">
      <div class="login-brand">TRADO AI</div>
      <div class="login-sub">SECURE EMAIL VERIFICATION • EDUCATION MODE</div>
      <h2>Welcome back</h2>
      <p style="color:#b5c6d5">Verify your email to open your market-learning workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    email = st.text_input("Email address", placeholder="you@example.com")
    human_check = st.checkbox("I'm not a bot")
    if st.button("Send verification code", type="primary", use_container_width=True):
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            st.error("Enter a valid email address.")
        elif not human_check:
            st.warning("Please complete the bot check.")
        else:
            code = f"{_secrets.randbelow(900000) + 100000}"
            ok, message = send_login_code(email.strip(), code)
            if ok:
                st.session_state.trado_pending_email = email.strip()
                st.session_state.trado_login_code = code
                st.session_state.trado_code_time = __import__("time").time()
                st.success(message)
            else:
                st.error(message)
                st.info("For privacy, TRADO does not display verification codes on screen.")
    if st.session_state.get("trado_login_code"):
        st.caption(f"Code sent to: {st.session_state.get('trado_pending_email', '')}")
        entered = st.text_input("6-digit verification code", max_chars=6)
        if st.button("Verify and enter TRADO", use_container_width=True):
            age = __import__("time").time() - st.session_state.get("trado_code_time", 0)
            if age > 600:
                st.error("That code has expired. Request a new one.")
            elif entered == st.session_state.get("trado_login_code"):
                st.session_state.trado_authenticated = True
                st.session_state.trado_user_email = st.session_state.trado_pending_email
                st.session_state.pop("trado_login_code", None)
                st.rerun()
            else:
                st.error("Incorrect verification code.")
    st.caption("TRADO uses email verification only. Never enter your MetaTrader 5 or Exness password here.")
    st.stop()

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
    page = st.radio("WORKSPACE", ["Dashboard", "Markets", "AI Analyst", "Learn", "Settings"])
    st.divider()
    st.success("EDUCATIONAL DEMO MODE")
    st.caption(f"Signed in: {st.session_state.get('trado_user_email', 'Verified email')}")
    if st.button("Sign out"):
        st.session_state.trado_authenticated = False
        st.session_state.pop("trado_user_email", None)
        st.rerun()
    st.caption("No broker connection • No order execution")

st.markdown("""
<div class="dashboard-top">
  <div><div class="dash-kicker">TRADO AI / MARKET INTELLIGENCE</div>
  <div class="dash-title">Welcome to your workspace</div>
  <div class="dash-sub">A clean view of market data, indicators and learning tools.</div></div>
  <div class="practice-pill">● DEMO ENVIRONMENT</div>
</div>
""", unsafe_allow_html=True)
st.info("Educational interface only. All balances and activity examples are illustrative practice data, not real funds or executed trades.")

if page == "Dashboard":
    col_balance, col_total, col_broker = st.columns([1.35, 1, 1])
    with col_balance:
        st.markdown("""
        <div class="practice-balance">
          <div class="practice-label">PRACTICE BALANCE</div>
          <div class="practice-value">$10,000.00</div>
          <span class="practice-pill">VIRTUAL FUNDS</span>
          <div class="practice-label" style="margin-top:14px">Illustrative learning balance · not withdrawable</div>
        </div>""", unsafe_allow_html=True)
        st.button("🔒  Deposit disabled in learning mode", disabled=True, use_container_width=True)
    with col_total:
        st.metric("Practice account value", "$10,000.00", "Demo only")
        st.markdown('<div class="panel-note">Sample figure for interface preview</div>', unsafe_allow_html=True)
    with col_broker:
        st.metric("Broker workspace", "Disconnected", "No credentials stored")
        st.markdown('<div class="panel-note">MT5 / Exness display-only selection</div>', unsafe_allow_html=True)

    st.markdown(" ")
    left, right = st.columns([1.02, 1.55], gap="large")
    with left:
        st.markdown('<div class="panel-title">Market watch</div>', unsafe_allow_html=True)
        watch = [
            ("EUR/USD", "FX · Major", "1.0842", "+0.18%"),
            ("GBP/USD", "FX · Major", "1.2718", "+0.11%"),
            ("USD/JPY", "FX · Major", "149.32", "−0.08%"),
            ("XAU/USD", "Metals", "2,035.40", "+0.32%"),
            ("BTC/USD", "Digital asset", "67,240", "+0.54%"),
            ("NASDAQ", "Index", "18,420", "+0.21%"),
        ]
        for sym, desc, price, change in watch:
            color = "#24d8a2" if not change.startswith("−") else "#f07b78"
            st.markdown(
                f'<div class="activity-row"><div><div class="activity-symbol">{sym}</div>'
                f'<div class="activity-meta">{desc}</div></div>'
                f'<div style="text-align:right"><div style="color:#e8eef3;font-weight:700">{price}</div>'
                f'<div style="color:{color};font-size:10px">{change}</div></div></div>',
                unsafe_allow_html=True
            )
        st.caption("Illustrative snapshot values for layout preview; not a live quote feed.")
    with right:
        st.markdown('<div class="panel-title">Practice balance history</div>', unsafe_allow_html=True)
        hist = pd.DataFrame({
            "Day": pd.date_range(end=pd.Timestamp.today().normalize(), periods=14),
            "Practice value": [10000,10030,10018,10055,10042,10070,10061,10088,10073,10102,10094,10115,10108,10125]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Day"], y=hist["Practice value"], mode="lines",
            line=dict(color="#20d6a3", width=2.5),
            fill="tozeroy", fillcolor="rgba(25,214,160,0.08)",
            hovertemplate="%{x|%d %b}<br>$%{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(
            height=245, margin=dict(l=8,r=8,t=12,b=8),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9aa8b5",size=10),
            xaxis=dict(showgrid=False,zeroline=False),
            yaxis=dict(showgrid=True,gridcolor="#202833",zeroline=False,tickprefix="$"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.caption("Synthetic example curve, not an account statement or performance record.")

    st.markdown(" ")
    c1, c2 = st.columns([1,1], gap="large")
    with c1:
        st.markdown('<div class="panel-title">Learning activity</div>', unsafe_allow_html=True)
        examples = [
            ("EMA 20 / EMA 50", "Moving-average comparison", "Study"),
            ("RSI 14", "Momentum indicator basics", "Study"),
            ("Candlestick patterns", "How to read OHLC bars", "Study"),
            ("Risk concepts", "Volatility, spread and uncertainty", "Study"),
        ]
        for name, desc, tag in examples:
            st.markdown(
                f'<div class="activity-row"><div><div class="activity-symbol">{name}</div>'
                f'<div class="activity-meta">{desc}</div></div>'
                f'<div class="activity-tag">{tag}</div></div>',
                unsafe_allow_html=True
            )
    with c2:
        st.markdown('<div class="panel-title">Broker platform overview</div>', unsafe_allow_html=True)
        broker = st.selectbox("Choose a platform to view", ["MetaTrader 5", "Exness"])
        st.markdown(
            f'<div class="broker-chip"><div style="font-size:13px;font-weight:750;color:#edf4f8">{broker}</div>'
            '<div class="activity-meta" style="margin-top:5px">Status: Not connected · Demo learning panel</div>'
            '<div class="activity-meta">No username, password, investor password or OTP is requested.</div></div>',
            unsafe_allow_html=True
        )
        st.caption("This selector is informational only. TRADO does not connect to broker accounts or place orders.")
elif page == "Markets":
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
    st.code('OPENAI_API_KEY = "your-private-key"\nOPENAI_MODEL = "gpt-5.5"\nTWELVE_DATA_API_KEY = "optional-private-data-key"\nSMTP_HOST = "smtp.example.com"\nSMTP_PORT = "587"\nSMTP_USERNAME = "your-mailbox"\nSMTP_PASSWORD = "your-mail-app-password"\nSMTP_FROM = "your-mailbox@example.com"', language="toml")
    st.write(f"OpenAI key: {'Configured' if OPENAI_KEY else 'Missing'}")
    st.write(f"Market data key: {'Configured' if DATA_KEY else 'Missing (optional)'}")
    st.write(f"Model: {OPENAI_MODEL}")
    st.error("Never commit API keys or SMTP credentials to GitHub. TRADO does not collect broker passwords or connect to live accounts.")

st.divider()
st.caption("TRADO AI v7.0 • Educational demo • No broker login • No trade execution")

