import streamlit as st
import secrets
import string
import math
import re

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="SecurePassPro",
    page_icon="🔐",
    layout="wide"
)

# =====================================
# SESSION STATE
# =====================================

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "passwords" not in st.session_state:
    st.session_state.passwords = []

if "history" not in st.session_state:
    st.session_state.history = []

if "passphrase" not in st.session_state:
    st.session_state.passphrase = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# =====================================
# THEME
# =====================================

theme = st.session_state.theme

if theme == "Dark":
    background = "#101827"
    card = "#1c2940"
    text = "#f8fafc"
    muted = "#cbd5e1"
    accent = "#a78bfa"
else:
    background = "#f4f6ff"
    card = "#ffffff"
    text = "#172554"
    muted = "#64748b"
    accent = "#7055e8"

# =====================================
# CUSTOM DESIGN
# =====================================

st.markdown(f"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

/* Main app background */
.stApp {{
    background-color: {background} !important;
    color: {text} !important;
}}

/* Header background wrapper */
header[data-testid="stHeader"] {{
    background-color: transparent !important;
}}

.block-container {{
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    background-color: {background};
}}

/* Sidebar Theme Integration */
[data-testid="stSidebar"] {{
    background-color: {card};
}}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {{
    color: {text} !important;
}}

[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] .stCaption {{
    color: {muted} !important;
}}

h1, h2, h3 {{
    color: {text};
}}

p, label {{
    color: {muted};
}}

.hero {{
    background: linear-gradient(
        120deg, #4935b5, #7957f5, #3984ee
    );
    padding: 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
}}

.hero h1, .hero h2, .hero p {{
    color: white;
}}

.stButton button {{
    background: linear-gradient(
        100deg, #7957f5, #4285f4
    );
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    min-height: 43px;
}}

.stButton button:hover {{
    color: white;
    border: 1px solid #a78bfa;
}}

[data-testid="stMetric"] {{
    background: {card};
    border: 1px solid #8b8b8b33;
    border-radius: 15px;
    padding: 18px;
}}

.feature {{
    background: {card};
    border: 1px solid #8b8b8b33;
    border-radius: 18px;
    padding: 22px;
    min-height: 155px;
    margin-bottom: 15px;
}}

.feature h3 {{
    color: {accent};
}}

.footer {{
    text-align: center;
    padding: 30px;
    color: {muted};
}}

</style>
""", unsafe_allow_html=True)

# =====================================
# HELPER FUNCTIONS
# =====================================

def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32
    if pool == 0:
        return 0
    return len(password) * math.log2(pool)


def get_strength(entropy):
    if entropy < 40:
        return "Weak"
    elif entropy < 60:
        return "Medium"
    elif entropy < 80:
        return "Strong"
    return "Very Strong"


def generate_password(length, groups):
    if not groups or length < len(groups):
        return None
    characters = "".join(groups)
    password = [secrets.choice(group) for group in groups]
    for _ in range(length - len(password)):
        password.append(secrets.choice(characters))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def password_checks(password):
    return {
        "Minimum 12 characters": len(password) >= 12,
        "Uppercase letters": any(c.isupper() for c in password),
        "Lowercase letters": any(c.islower() for c in password),
        "Numbers": any(c.isdigit() for c in password),
        "Special characters": any(c in string.punctuation for c in password)
    }


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.title("🔐 SecurePassPro")
    st.caption("STRONGER PASSWORDS. SAFER YOU.")
    st.divider()

    st.subheader("Appearance")
    selected_theme = st.selectbox(
        "Select Theme",
        ["Light", "Dark", "System"],
        index=["Light", "Dark", "System"].index(theme)
    )

    if selected_theme != theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "🏠 Dashboard",
            "🔑 Password Generator",
            "🧠 Passphrase Generator",
            "🔍 Password Analyzer",
            "🛡️ Security Center"
        ]
    )

    st.divider()
    st.success("Security Tools Active")
    st.caption("Version 3.0")

# =====================================
# DASHBOARD
# =====================================

if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
    <h1>Welcome to SecurePassPro 👋</h1>
    <p>
    Your personal password security studio.
    Create, analyse and strengthen your digital security.
    </p>
    <h2>🔐 Protect What Matters.</h2>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Dashboard")

    a, b, c = st.columns(3)
    a.metric("Passwords Generated", len(st.session_state.history))
    b.metric("Security Tools", "04")
    c.metric("Application Version", "3.0")

    st.divider()
    st.subheader("Explore Your Security Tools")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature">
        <h2>🔑</h2>
        <h3>Password Generator</h3>
        <p>Create strong random passwords.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature">
        <h2>🧠</h2>
        <h3>Passphrase Generator</h3>
        <p>Create memorable passphrases.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature">
        <h2>🔍</h2>
        <h3>Password Analyzer</h3>
        <p>Check password characteristics.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Security Recommendations")
    st.info("Use unique passwords for every account.")
    st.success("Enable two-factor authentication.")
    st.warning("Never share your passwords.")

# =====================================
# PASSWORD GENERATOR
# =====================================

elif page == "🔑 Password Generator":
    st.title("🔑 Password Generator")
    st.write("Create strong and random passwords.")
    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Configuration")
        length = st.slider("Password Length", 8, 128, 16)
        upper = st.checkbox("Uppercase Letters", True)
        lower = st.checkbox("Lowercase Letters", True)
        digits = st.checkbox("Numbers", True)
        symbols = st.checkbox("Special Characters", True)
        exclude = st.checkbox("Exclude confusing characters (O, 0, l, 1)")
        number = st.selectbox("Number of Passwords", [1, 3, 5, 10])

    with col2:
        st.subheader("Security Guide")
        st.success("Strong: 60–79 bits")
        st.info("Very Strong: 80+ bits")
        st.warning("Medium: 40–59 bits")
        st.error("Weak: Below 40 bits")
        st.caption("Longer randomly generated passwords are generally harder to guess.")

    st.divider()

    if st.button("✨ Generate Passwords", use_container_width=True):
        groups = []
        if upper:
            groups.append(string.ascii_uppercase)
        if lower:
            groups.append(string.ascii_lowercase)
        if digits:
            groups.append(string.digits)
        if symbols:
            groups.append(string.punctuation)

        if exclude:
            groups = [
                "".join(char for char in group if char not in "O0l1")
                for group in groups
            ]

        if not groups:
            st.error("Select at least one character type.")
        elif length < len(groups):
            st.error("Increase the password length.")
        else:
            st.session_state.passwords = []
            for _ in range(number):
                password = generate_password(length, groups)
                st.session_state.passwords.append(password)
                st.session_state.history.append(password)
            st.session_state.history = st.session_state.history[-20:]

    if st.session_state.passwords:
        st.subheader("Your Generated Passwords")
        for index, password in enumerate(st.session_state.passwords):
            entropy = calculate_entropy(password)
            strength = get_strength(entropy)
            with st.expander(f"Password {index + 1} — {strength}"):
                st.code(password)
                st.caption(f"Length: {len(password)} | Estimated entropy: {entropy:.1f} bits")
                st.progress(min(entropy / 128, 1.0))

        st.download_button(
            "⬇️ Download All Passwords",
            "\n".join(st.session_state.passwords),
            file_name="SecurePassPro_passwords.txt",
            use_container_width=True
        )

# =====================================
# PASSPHRASE GENERATOR
# =====================================

elif page == "🧠 Passphrase Generator":
    st.title("🧠 Passphrase Generator")
    st.write("Generate memorable combinations of random words.")

    words = [
        "River", "Mountain", "Cloud", "Garden",
        "Ocean", "Forest", "Silver", "Crystal",
        "Sunshine", "Planet", "Thunder", "Meadow",
        "Galaxy", "Autumn", "Breeze", "Velvet",
        "Sunrise", "Lantern", "Marble", "Willow",
        "Comet", "Harbor", "Maple", "Cedar",
        "Aurora", "Coral", "Pebble", "Falcon",
        "Orchid", "Canyon", "Winter", "Sapphire"
    ]

    count = st.slider("Number of Words", 3, 8, 4)
    separator = st.selectbox("Separator", ["-", "_", ".", "@", " "])
    add_number = st.checkbox("Add Random Numbers", True)

    if st.button("✨ Generate Passphrase", use_container_width=True):
        selected = [secrets.choice(words) for _ in range(count)]
        phrase = separator.join(selected)
        if add_number:
            phrase += str(secrets.randbelow(900) + 100)
        st.session_state.passphrase = phrase

    if st.session_state.passphrase:
        st.success("Passphrase generated!")
        st.code(st.session_state.passphrase)
        st.download_button(
            "⬇️ Download Passphrase",
            st.session_state.passphrase,
            file_name="SecurePassPro_passphrase.txt"
        )

# =====================================
# PASSWORD ANALYZER
# =====================================

elif page == "🔍 Password Analyzer":
    st.title("🔍 Password Analyzer")
    st.write("Evaluate password characteristics and security.")
    st.warning("Use a sample password. Never enter a password that protects an important account.")

    password = st.text_input("Enter Sample Password", type="password")

    if st.button("🔍 Analyze Password", use_container_width=True):
        if not password:
            st.error("Enter a password first.")
        else:
            entropy = calculate_entropy(password)
            st.session_state.analysis = {
                "entropy": entropy,
                "strength": get_strength(entropy),
                "checks": password_checks(password),
                "length": len(password),
                "repeated": bool(re.search(r"(.)\\1{3,}", password))
            }

    if st.session_state.analysis:
        result = st.session_state.analysis
        st.divider()
        st.subheader("Analysis Results")

        a, b, c = st.columns(3)
        a.metric("Length", result["length"])
        b.metric("Entropy Estimate", f'{result["entropy"]:.1f} bits')
        c.metric("Strength", result["strength"])

        st.progress(min(result["entropy"] / 128, 1.0))
        st.subheader("Security Checklist")

        for label, status in result["checks"].items():
            if status:
                st.success("✓ " + label)
            else:
                st.error("✗ " + label)

        if result["repeated"]:
            st.warning("Repeated characters detected.")

        st.info("This is an approximate analysis, not a guarantee of real-world security.")

# =====================================
# SECURITY CENTER
# =====================================

elif page == "🛡️ Security Center":
    st.title("🛡️ Security Center")
    st.write("Learn how to protect your digital identity.")

    tips = {
        "🔐 Unique Passwords": "Never reuse the same password across multiple accounts.",
        "📏 Longer Passwords": "Long random passwords are generally harder to guess.",
        "🛡️ Two-Factor Authentication": "Add an extra layer of security to your accounts.",
        "🚫 Avoid Personal Information": "Avoid birthdays, names and phone numbers.",
        "🔄 Compromised Passwords": "Change passwords immediately if an account is compromised.",
        "🔒 Password Managers": "Use a reputable password manager to store unique passwords."
    }

    for title, description in tips.items():
        with st.expander(title):
            st.write(description)

    st.divider()
    st.subheader("Password Strength Guide")
    st.error("Weak — Below 40 bits")
    st.warning("Medium — 40–59 bits")
    st.success("Strong — 60–79 bits")
    st.info("Very Strong — 80+ bits")
    st.caption("Strength categories are approximate entropy estimates.")

# =====================================
# FOOTER
# =====================================

st.divider()
st.markdown("""
<div class="footer">
<h3>🔐 SecurePassPro</h3>
Stronger Passwords. Safer You.
<br><br>
Built with Python and Streamlit
<br>
Version 3.0 | 2026
</div>
""", unsafe_allow_html=True)