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
