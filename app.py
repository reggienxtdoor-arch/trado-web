
import streamlit as st

st.set_page_config(
    page_title="TRADO AI Trader",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 TRADO AI TRADER")
st.subheader("The Next Era of Smart Trading")

st.success("TRADO AI Trader is running!")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    ["Dashboard", "Market Analysis", "Risk Management", "Settings"]
)

if page == "Dashboard":
    st.header("Trading Dashboard")
    st.info("Welcome to TRADO AI Trader.")
    st.metric("Trading Mode", "DEMO ONLY")
    st.warning("No live trades are being executed.")

elif page == "Market Analysis":
    st.header("Market Analysis")
    st.write("Market analysis features coming soon.")

elif page == "Risk Management":
    st.header("Risk Management")
    st.write("Risk controls and demo testing settings.")

elif page == "Settings":
    st.header("Settings")
    st.write("TRADO configuration.")

st.caption("TRADO AI Trader v1.0.0 | Developed by ReggieNextDoor")
