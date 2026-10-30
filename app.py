import streamlit as st
import secrets
import string
import math

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SecurePass | Password Generator",
    page_icon="🔐",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1020, #151b32);
    color: white;
}

.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: #ffffff;
}

.subtitle {
    text-align: center;
    color: #aab4d4;
    font-size: 16px;
    margin-bottom: 30px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    background: linear-gradient(90deg, #635bff, #9b59ff);
    color: white;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    border: 1px solid white;
    color: white;
}

div[data-testid="stMetric"] {
    background: #202945;
    padding: 15px;
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #8994b5;
    font-size: 13px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    "<h1>🔐 SecurePass</h1>",
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Your personal password security assistant</p>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- PASSWORD SETTINGS ----------------

st.subheader("⚙️ Password Configuration")

length = st.slider(
    "Password Length",
    min_value=8,
    max_value=64,
    value=16
)

st.caption(f"Selected length: {length} characters")


# ---------------- CHARACTER OPTIONS ----------------

st.subheader("🔤 Character Preferences")

col1, col2 = st.columns(2)

with col1:

    use_upper = st.checkbox(
        "Uppercase letters (A-Z)",
        value=True
    )

    use_lower = st.checkbox(
        "Lowercase letters (a-z)",
        value=True
    )

with col2:

    use_digits = st.checkbox(
        "Numbers (0-9)",
        value=True
    )

    use_symbols = st.checkbox(
        "Special characters (!@#$)",
        value=True
    )


exclude_ambiguous = st.checkbox(
    "Exclude confusing characters (O, 0, l, 1)",
    value=False
)

st.divider()


# ---------------- GENERATE PASSWORD ----------------

st.subheader("🚀 Generate Your Password")


if st.button("🔐 Generate Secure Password"):

    characters = ""

    groups = []

    if use_upper:
        groups.append(string.ascii_uppercase)

    if use_lower:
        groups.append(string.ascii_lowercase)

    if use_digits:
        groups.append(string.digits)

    if use_symbols:
        groups.append(string.punctuation)

    if not groups:

        st.error("Please select at least one character type.")

        st.session_state.password = ""

    elif length < len(groups):

        st.error("Password length is too short for selected options.")

        st.session_state.password = ""

    else:

        if exclude_ambiguous:

            groups = [
                group.translate(
                    str.maketrans("", "", "O0l1")
                )
                for group in groups
            ]

        if any(not group for group in groups):

            st.error("Selected character options are invalid.")

            st.session_state.password = ""

        else:

            characters = "".join(groups)

            # Include at least one character from each group

            password_list = [
                secrets.choice(group)
                for group in groups
            ]

            # Fill remaining positions

            for _ in range(length - len(password_list)):

                password_list.append(
                    secrets.choice(characters)
                )

            # Shuffle password

            secrets.SystemRandom().shuffle(password_list)

            password = "".join(password_list)

            st.session_state.password = password


# ---------------- DISPLAY PASSWORD ----------------

if st.session_state.get("password"):

    password = st.session_state.password

    st.divider()

    st.subheader("✨ Your Generated Password")

    show_password = st.checkbox(
        "Show Password",
        value=True
    )

    st.text_input(
        "Generated Password",
        value=password,
        type="default" if show_password else "password"
    )

    st.caption(
        "Use the copy icon in the password field to copy it."
    )

    # ---------------- STRENGTH CALCULATION ----------------

    pool_size = len(characters) if characters else 0

    # Reconstruct the pool for the displayed password
    if pool_size == 0:
        pool_size = sum(
            len(group)
            for group in groups
        )

    entropy = length * math.log2(pool_size)

    if entropy < 40:
        strength = "Weak"

    elif entropy < 60:
        strength = "Medium"

    elif entropy < 80:
        strength = "Strong"

    else:
        strength = "Very Strong"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Password Length",
            length
        )

    with col2:
        st.metric(
            "Strength",
            strength
        )

    with col3:
        st.metric(
            "Estimated Entropy",
            f"{entropy:.1f} bits"
        )

    # ---------------- DOWNLOAD ----------------

    st.download_button(
        label="⬇️ Download Password",
        data=password,
        file_name="secure_password.txt",
        mime="text/plain"
    )


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div class="footer">

🔒 SecurePass | Random Password Generator

<br>

Built with Python, Streamlit and the Secrets Module

</div>
""", unsafe_allow_html=True)