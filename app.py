import streamlit as st
import secrets
import string
import math
import re

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SecurePassPro",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f8f9ff, #eef1ff);
    color: #172554;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7ff;
}

h1, h2, h3 {
    color: #172554;
}

.hero {
    background: linear-gradient(110deg, #dceaff, #f0e5ff, #ffeafa);
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 32px;
    font-weight: 700;
}

.hero p {
    font-size: 16px;
    color: #475569;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5eaff;
    box-shadow: 0 5px 20px rgba(90, 100, 180, 0.06);
    margin-bottom: 18px;
}

.feature-card {
    background: linear-gradient(135deg, #ffffff, #f3f0ff);
    padding: 20px;
    border-radius: 17px;
    border: 1px solid #e3ddff;
    min-height: 130px;
}

.result-card {
    background: linear-gradient(120deg, #eff6ff, #f5f0ff);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #dce4ff;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e5eaff;
    text-align: center;
}

.metric-card h2 {
    color: #6854e8;
}

.stButton > button {
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #8b5cf6, #5b8cff);
    color: white;
    font-weight: 600;
    min-height: 45px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #7045dc, #4779e8);
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #e5eaff;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

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


def password_strength(entropy):

    if entropy < 40:
        return "Weak", "🔴"

    elif entropy < 60:
        return "Medium", "🟠"

    elif entropy < 80:
        return "Strong", "🟢"

    return "Very Strong", "💜"


def generate_password(length, groups, custom=""):

    characters = "".join(groups) + custom

    if not characters:
        return None

    if length < len(groups):
        return None

    password = []

    for group in groups:

        password.append(secrets.choice(group))

    for _ in range(length - len(password)):

        password.append(secrets.choice(characters))

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def analyze_password(password):

    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains uppercase letters": any(c.isupper() for c in password),
        "Contains lowercase letters": any(c.islower() for c in password),
        "Contains numbers": any(c.isdigit() for c in password),
        "Contains special characters": any(
            c in string.punctuation for c in password
        )
    }

    return checks


# ==========================================
# SESSION STATE
# ==========================================

if "passwords" not in st.session_state:
    st.session_state.passwords = []

if "generated_passphrase" not in st.session_state:
    st.session_state.generated_passphrase = ""


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🔐 SecurePassPro")

    st.caption("Stronger Passwords. Safer You.")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "🔑 Password Generator",
            "🧠 Passphrase Generator",
            "🔍 Password Analyzer",
            "🛡️ Security Center"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### ✨ Your Security Matters")

    st.info(
        "Create stronger passwords and "
        "protect your digital world."
    )

    st.caption("SecurePassPro v1.0")


# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown("""
    <div class="hero">

    <h1>Welcome to SecurePassPro! 👋</h1>

    <p>
    Generate strong, unique passwords and keep
    your digital life secure — all in one place.
    </p>

    <h3>🔒 Small Steps. Big Security.</h3>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explore Your Security Tools")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
        <h2>🔑</h2>
        <h3>Password Generator</h3>
        <p>Create strong random passwords instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
        <h2>🧠</h2>
        <h3>Passphrase Generator</h3>
        <p>Create memorable secure passphrases.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
        <h2>🔍</h2>
        <h3>Password Analyzer</h3>
        <p>Check password characteristics and strength.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Actions")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🔑 Generate a Password", use_container_width=True):
            st.session_state.navigate = "🔑 Password Generator"
            st.rerun()

    with c2:
        if st.button("🔍 Analyze a Password", use_container_width=True):
            st.session_state.navigate = "🔍 Password Analyzer"
            st.rerun()

    st.markdown("### 💡 Security Tips")

    st.success("Use a unique password for every account.")

    st.info("Enable two-factor authentication wherever possible.")

    st.warning("Never share your passwords with anyone.")


# ==========================================
# PASSWORD GENERATOR
# ==========================================

elif page == "🔑 Password Generator":

    st.title("🔑 Password Generator")

    st.write("Create a strong password tailored to your needs.")

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("Password Configuration")

        length = st.slider(
            "Password Length",
            8, 128, 16
        )

        st.markdown("### Character Types")

        a, b = st.columns(2)

        with a:

            upper = st.checkbox("Uppercase (A-Z)", True)

            lower = st.checkbox("Lowercase (a-z)", True)

        with b:

            digits = st.checkbox("Numbers (0-9)", True)

            symbols = st.checkbox("Special Characters", True)

        exclude = st.checkbox(
            "Exclude confusing characters (O, 0, l, 1)"
        )

        custom = st.text_input(
            "Custom Characters (Optional)",
            placeholder="e.g. @#$%^&"
        )

        st.markdown("### Advanced Settings")

        number = st.selectbox(
            "Number of Passwords",
            [1, 3, 5, 10]
        )

        preset = st.selectbox(
            "Password Preset",
            ["Custom", "Strong", "Maximum Security"]
        )

        if preset == "Strong":

            length = max(length, 16)

            upper = lower = digits = symbols = True

        elif preset == "Maximum Security":

            length = max(length, 32)

            upper = lower = digits = symbols = True

    with col2:

        st.subheader("Password Strength Guide")

        st.success("🟢 Strong: 60–79 bits")

        st.info("💜 Very Strong: 80+ bits")

        st.warning("🟠 Medium: 40–59 bits")

        st.error("🔴 Weak: Below 40 bits")

        st.markdown("### 💡 Pro Tip")

        st.write(
            "Longer passwords with different character "
            "types generally provide better security."
        )

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
                "".join(c for c in group if c not in "O0l1")
                for group in groups
            ]

        if not groups and not custom:

            st.error("Select at least one character type.")

        elif length < len(groups) + (1 if custom else 0):

            st.error("Increase password length.")

        else:

            if exclude:
                custom = "".join(
                    c for c in custom if c not in "O0l1"
                )

            if not groups and custom:
                groups = [custom]

            st.session_state.passwords = []

            for _ in range(number):

                password = generate_password(
                    length,
                    groups,
                    custom
                )

                if password:
                    st.session_state.passwords.append(password)

    if st.session_state.passwords:

        st.markdown("## 🎉 Your Generated Passwords")

        for i, password in enumerate(
            st.session_state.passwords, 1
        ):

            entropy = calculate_entropy(password)

            strength, icon = password_strength(entropy)

            with st.container(border=True):

                c1, c2 = st.columns([3, 1])

                with c1:

                    st.text_input(
                        f"Password {i}",
                        value=password,
                        key=f"password_{i}"
                    )

                with c2:

                    st.markdown(f"### {icon} {strength}")

                st.caption(
                    f"Length: {len(password)} | "
                    f"Estimated entropy: {entropy:.1f} bits"
                )

        all_passwords = "\n".join(
            st.session_state.passwords
        )

        c1, c2 = st.columns(2)

        with c1:

            st.download_button(
                "⬇️ Download Passwords",
                all_passwords,
                file_name="SecurePassPro_passwords.txt",
                use_container_width=True
            )

        with c2:

            if st.button(
                "🔄 Generate Again",
                use_container_width=True
            ):

                st.session_state.passwords = []
                st.rerun()


# ==========================================
# PASSPHRASE GENERATOR
# ==========================================

elif page == "🧠 Passphrase Generator":

    st.title("🧠 Passphrase Generator")

    st.write(
        "Generate memorable combinations of random words."
    )

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

    count = st.slider(
        "Number of Words",
        3, 8, 4
    )

    separator = st.selectbox(
        "Word Separator",
        ["-", "_", ".", "@", " "]
    )

    add_number = st.checkbox(
        "Add random numbers",
        True
    )

    if st.button(
        "✨ Generate Passphrase",
        use_container_width=True
    ):

        selected = [
            secrets.choice(words)
            for _ in range(count)
        ]

        phrase = separator.join(selected)

        if add_number:
            phrase += str(secrets.randbelow(900) + 100)

        st.session_state.generated_passphrase = phrase

    if st.session_state.generated_passphrase:

        st.success("Your passphrase is ready!")

        st.code(
            st.session_state.generated_passphrase
        )

        st.download_button(
            "⬇️ Download Passphrase",
            st.session_state.generated_passphrase,
            file_name="passphrase.txt"
        )


# ==========================================
# PASSWORD ANALYZER
# ==========================================

elif page == "🔍 Password Analyzer":

    st.title("🔍 Password Analyzer")

    st.write(
        "Check password characteristics and identify "
        "potential weaknesses."
    )

    st.warning(
        "Privacy: Analysis happens locally in this app. "
        "Avoid entering passwords you currently use."
    )

    password = st.text_input(
        "Enter a sample password",
        type="password",
        placeholder="Enter password here"
    )

    if st.button(
        "Analyze Password",
        use_container_width=True
    ):

        if not password:

            st.error("Please enter a password.")

        else:

            entropy = calculate_entropy(password)

            strength, icon = password_strength(entropy)

            st.markdown("## Analysis Results")

            c1, c2, c3 = st.columns(3)

            c1.metric("Length", len(password))

            c2.metric("Entropy Estimate", f"{entropy:.1f} bits")

            c3.metric("Strength", strength)

            st.markdown("### Security Checklist")

            checks = analyze_password(password)

            for label, result in checks.items():

                if result:
                    st.success("✓ " + label)

                else:
                    st.error("✗ " + label)

            if re.search(r"(.)\1{3,}", password):

                st.warning(
                    "Repeated characters detected."
                )

            if password.isdigit():

                st.warning(
                    "Using only numbers is not recommended."
                )

            st.info(
                "Entropy is an estimate, not a guarantee "
                "of real-world password security."
            )


# ==========================================
# SECURITY CENTER
# ==========================================

elif page == "🛡️ Security Center":

    st.title("🛡️ Security Center")

    st.write(
        "Learn how to protect your digital identity."
    )

    tips = [
        (
            "🔐 Use Unique Passwords",
            "Never reuse the same password across multiple accounts."
        ),
        (
            "📏 Choose Longer Passwords",
            "Long, random passwords are generally harder to guess."
        ),
        (
            "🛡️ Enable Two-Factor Authentication",
            "Add an extra layer of protection to your accounts."
        ),
        (
            "🚫 Avoid Personal Information",
            "Don't use birthdays, names or phone numbers."
        ),
        (
            "🔄 Update Compromised Passwords",
            "Change passwords immediately if an account is compromised."
        ),
        (
            "🔒 Use a Password Manager",
            "A reputable password manager can help store unique passwords."
        )
    ]

    for title, description in tips:

        with st.expander(title):

            st.write(description)

    st.divider()

    st.subheader("Password Strength Guide")

    st.error("Weak — Below 40 bits")

    st.warning("Medium — 40 to 59 bits")

    st.success("Strong — 60 to 79 bits")

    st.info("Very Strong — 80 bits or above")

    st.caption(
        "These are approximate entropy categories, "
        "not guarantees of security."
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">

🔐 SecurePassPro

<br>

Stronger Passwords. Safer You.

<br><br>

Built with Python and Streamlit

</div>
""", unsafe_allow_html=True)