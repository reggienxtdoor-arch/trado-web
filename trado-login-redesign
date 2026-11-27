
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="TRADO AI | Login",
    page_icon="📈",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
      radial-gradient(circle at 10% 10%, #123b3b 0%, transparent 35%),
      radial-gradient(circle at 90% 20%, #102b43 0%, transparent 35%),
      #070b11;
    font-family: Inter, sans-serif;
}
.block-container {
    max-width: 650px;
    padding-top: 3rem;
}
.brand {
    text-align:center;
    font-size:38px;
    font-weight:800;
    letter-spacing:9px;
    color:#b9fff1;
    text-shadow:0 0 25px #19d6b4;
}
.tag {
    text-align:center;
    color:#19d6b4;
    letter-spacing:4px;
    font-size:11px;
    font-weight:800;
    margin-bottom:35px;
}
.login-card {
    background:linear-gradient(145deg,#121e2a,#0b131d);
    border:1px solid #293b4b;
    border-radius:22px;
    padding:28px;
    box-shadow:0 20px 65px #0008;
}
h2 { color:#f3f8fc; }
p { color:#9eafbd; }
div[data-testid="stTextInput"] input {
    background:#09121b;
    color:white;
    border:1px solid #354b5e;
    border-radius:11px;
    min-height:48px;
}
div[data-testid="stTextInput"] input:focus {
    border:1px solid #19d6b4;
    box-shadow:0 0 0 2px #19d6b422;
}
div.stButton > button,
div.stFormSubmitButton > button {
    background:linear-gradient(100deg,#19d6b4,#56aeea);
    color:#04110f;
    font-weight:800;
    border:0;
    border-radius:11px;
    min-height:47px;
}
div[data-testid="stTabs"] button {
    color:#aebdca;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color:#19d6b4;
}
</style>
""", unsafe_allow_html=True)

# Supabase configuration
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets.get(
        "SUPABASE_ANON_KEY",
        st.secrets.get("SUPABASE_PUBLISHABLE_KEY", "")
    )
    if not key:
        raise ValueError("Missing Supabase public key")
    supabase = create_client(url, key)
    configured = True
except Exception:
    supabase = None
    configured = False

# Handle email/OAuth callback
if configured:
    try:
        code = st.query_params.get("code")
        if code:
            result = supabase.auth.exchange_code_for_session(
                {"auth_code": code}
            )
            st.session_state["trado_user"] = result.user.email
            st.query_params.clear()
            st.rerun()
    except Exception:
        st.error("Sign-in confirmation failed. Please try again.")

# Session
if "trado_user" not in st.session_state:
    st.session_state["trado_user"] = None

st.markdown('<div class="brand">TRADO AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tag">SECURE ACCOUNT ACCESS</div>',
    unsafe_allow_html=True
)

if st.session_state["trado_user"]:
    st.success("You are signed in.")
    st.write("Account:", st.session_state["trado_user"])
    st.info("Welcome to your TRADO AI learning workspace.")
    if st.button("Sign out", use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state["trado_user"] = None
        st.rerun()
    st.stop()

st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.subheader("Welcome back")
st.write("Sign in to your TRADO AI account.")

login, signup, reset = st.tabs([
    "Sign in", "Create account", "Reset password"
])

with login:
    with st.form("login_form"):
        email = st.text_input(
            "Email address",
            placeholder="you@example.com"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your TRADO AI password"
        )
        submit = st.form_submit_button(
            "SIGN IN SECURELY",
            use_container_width=True
        )

    if submit:
        if not email.strip() or not password:
            st.warning("Enter your email and password.")
        elif not configured:
            st.error("Supabase is not configured. Add the secrets shown below.")
        else:
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password
                })
                st.session_state["trado_user"] = result.user.email
                st.rerun()
            except Exception:
                st.error(
                    "Login failed. Check your details and confirm your email."
                )

    st.divider()
    st.write("Or sign in using a connected provider:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Google", use_container_width=True):
            if configured:
                try:
                    result = supabase.auth.sign_in_with_oauth({
                        "provider": "google",
                        "options": {
                            "redirect_to": st.secrets.get("APP_URL", "")
                        }
                    })
                    st.link_button(
                        "Continue to Google",
                        result.url,
                        use_container_width=True
                    )
                except Exception:
                    st.error("Configure Google sign-in in Supabase first.")
            else:
                st.error("Configure Supabase first.")

    with col2:
        if st.button("Apple", use_container_width=True):
            if configured:
                try:
                    result = supabase.auth.sign_in_with_oauth({
                        "provider": "apple",
                        "options": {
                            "redirect_to": st.secrets.get("APP_URL", "")
                        }
                    })
                    st.link_button(
                        "Continue to Apple",
                        result.url,
                        use_container_width=True
                    )
                except Exception:
                    st.error("Configure Apple sign-in in Supabase first.")
            else:
                st.error("Configure Supabase first.")

with signup:
    with st.form("signup_form"):
        new_email = st.text_input("Email address")
        new_password = st.text_input(
            "Create password", type="password"
        )
        confirm = st.text_input(
            "Confirm password", type="password"
        )
        create = st.form_submit_button(
            "CREATE ACCOUNT",
            use_container_width=True
        )

    if create:
        if not configured:
            st.error("Connect Supabase before creating an account.")
        elif not new_email.strip() or not new_password:
            st.warning("Complete all fields.")
        elif len(new_password) < 8:
            st.warning("Use at least 8 characters.")
        elif new_password != confirm:
            st.error("Your passwords do not match.")
        else:
            try:
                supabase.auth.sign_up({
                    "email": new_email.strip(),
                    "password": new_password
                })
                st.success(
                    "Account created. Check your email for verification."
                )
            except Exception:
                st.error("Account creation failed. Check your details.")

with reset:
    with st.form("reset_form"):
        reset_email = st.text_input("Your account email")
        send = st.form_submit_button(
            "SEND RESET EMAIL",
            use_container_width=True
        )

    if send:
        if configured and reset_email.strip():
            try:
                supabase.auth.reset_password_for_email(
                    reset_email.strip()
                )
                st.success("Check your email for password-reset instructions.")
            except Exception:
                st.error("Could not send the reset email.")
        else:
            st.warning("Enter your email and configure Supabase.")

st.markdown('</div>', unsafe_allow_html=True)

if not configured:
    st.warning(
        "Authentication needs configuration. Add your Supabase URL "
        "and public key in Streamlit Secrets."
    )

st.caption("TRADO AI • Secure account access")
