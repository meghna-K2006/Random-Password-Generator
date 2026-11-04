import streamlit as st
import secrets
import string
import math
import re
import html

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SECUREPASS ELITE",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "generated_passwords" not in st.session_state:
    st.session_state.generated_passwords = []

if "generated_passphrase" not in st.session_state:
    st.session_state.generated_passphrase = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# =====================================================
# CUSTOM CSS
# Keep CSS inside this style block only.
# Do not put st.html() or HTML page content here.
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080F20;
    color: #F5F7FC;
}

header, footer, #MainMenu {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0D172B;
    border-right: 1px solid #24334D;
}

section[data-testid="stSidebar"] * {
    color: #E8EDF7;
}

.brand {
    text-align: center;
    padding: 15px 5px 25px 5px;
}

.brand-icon {
    font-size: 38px;
    margin-bottom: 8px;
}

.brand-title {
    font-size: 22px;
    font-weight: 800;
    color: #E7BD65 !important;
    letter-spacing: 1px;
}

.brand-subtitle {
    font-size: 10px;
    color: #8C9BB5 !important;
    letter-spacing: 3px;
    margin-top: 5px;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    width: 100%;
    background: transparent !important;
    color: #C4CDDD !important;
    border: 1px solid transparent !important;
    border-radius: 9px;
    text-align: left;
    padding: 12px 15px;
    font-size: 13px;
    font-weight: 600;
    transition: 0.2s;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: #192943 !important;
    border: 1px solid #D5AC54 !important;
    color: #F0C96E !important;
}

/* HERO */

.hero {
    background: linear-gradient(120deg, #142641, #0D192D);
    border: 1px solid #B88C3B;
    border-radius: 18px;
    padding: 38px;
    margin-bottom: 25px;
}

.hero-label {
    color: #E6BD65;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 12px;
    line-height: 1.2;
}

.hero-title span {
    color: #E6BD65;
}

.hero-description {
    color: #AAB8CE;
    font-size: 13px;
    line-height: 1.8;
    max-width: 650px;
}

/* SECTION HEADINGS */

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #F5C77B;
    margin-top: 22px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #AAB8CE;
    font-size: 12px;
    margin-top: 0;
    margin-bottom: 15px;
}

/* OVERVIEW CARDS */

.overview-card {
    background: #111E33;
    border: 1px solid #263955;
    border-radius: 13px;
    padding: 20px;
    min-height: 115px;
    margin-bottom: 10px;
    box-sizing: border-box;
}

.overview-label {
    font-size: 11px;
    color: #98A8C0;
    margin-bottom: 12px;
}

.overview-value {
    font-size: 24px;
    font-weight: 800;
    color: #E9C36F;
}

.overview-note {
    font-size: 10px;
    color: #7F91AC;
    margin-top: 6px;
}

/* DASHBOARD TOOL CARDS */

.tool-card {
    background: linear-gradient(135deg, #142943, #102039);
    border: 1px solid #344B69;
    border-radius: 14px;
    padding: 20px;
    height: 145px;
    margin-bottom: 8px;
    box-sizing: border-box;
}

.tool-icon {
    font-size: 24px;
    margin-bottom: 12px;
}

.tool-title {
    font-size: 15px;
    font-weight: 700;
    color: #F5C77B;
    margin-bottom: 8px;
}

.tool-description {
    font-size: 11px;
    color: #D0D9E8;
    line-height: 1.6;
}

/* MAIN AREA BUTTONS
   Full-width gold buttons that match each dashboard tool card.
   The sidebar navigation keeps its original dark styling.
*/

.stApp [data-testid="stMain"] div[data-testid="stButton"] {
    width: 100% !important;
    display: block !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    height: 45px !important;
    min-height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 8px 15px !important;
    background: linear-gradient(90deg, #F2BD65, #FFD58B) !important;
    background-color: #FFD58B !important;
    color: #80603B !important;
    -webkit-text-fill-color: #80603B !important;
    border: 1px solid #E9B95F !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button p,
.stApp [data-testid="stMain"] div[data-testid="stButton"] > button span {
    color: #80603B !important;
    -webkit-text-fill-color: #80603B !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:hover {
    background: linear-gradient(90deg, #FFD58B, #FFE2A8) !important;
    background-color: #FFE0A0 !important;
    color: #5D4528 !important;
    -webkit-text-fill-color: #5D4528 !important;
    border: 1px solid #E9B95F !important;
    box-shadow: 0 4px 14px rgba(242, 189, 101, 0.25) !important;
    transform: translateY(-2px);
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:hover p,
.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:hover span {
    color: #5D4528 !important;
    -webkit-text-fill-color: #5D4528 !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:focus,
.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:active {
    color: #80603B !important;
    -webkit-text-fill-color: #80603B !important;
    border-color: #E9B95F !important;
    box-shadow: 0 0 0 2px rgba(242, 189, 101, 0.18) !important;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stTextArea textarea {
    background: #111E33;
    color: white;
    border: 1px solid #354967;
    border-radius: 8px;
}

.stCheckbox label {
    color: #D8E0ED;
}

/* PAGE HEADINGS */

.page-heading {
    font-size: 28px;
    font-weight: 800;
    color: #E8C16B;
    margin-bottom: 8px;
}

.page-description {
    color: #98A9C1;
    font-size: 13px;
    margin-bottom: 28px;
}

/* RESULT BOX */

.result-box {
    background: #13243A;
    border: 1px solid #D0A64F;
    border-radius: 12px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.result-label {
    color: #D8B45F;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.result-value {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 700;
    word-break: break-word;
}

/* SECURITY CENTER CARDS */

.info-card {
    background: #111E33;
    border: 1px solid #293B58;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
}

.info-card h4 {
    color: #E8C16B;
    margin-bottom: 9px;
    font-size: 15px;
}

.info-card p {
    color: #A5B3C8;
    font-size: 12px;
    line-height: 1.7;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #8999B2;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 22px 0 10px 0;
    border-top: 1px solid #263650;
    margin-top: 28px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def navigate(page):
    st.session_state.page = page


def page_heading(title, description):
    st.markdown(
        f"""
        <div class="page-heading">{html.escape(title)}</div>
        <div class="page-description">{html.escape(description)}</div>
        """,
        unsafe_allow_html=True
    )


def generate_password(
    length,
    use_upper,
    use_lower,
    use_numbers,
    use_symbols,
    exclude_similar
):
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase

    if use_lower:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += "!@#$%^&*()-_=+[]{}?"

    if exclude_similar:
        for char in "Il1O0o":
            characters = characters.replace(char, "")

    if not characters:
        return None

    return "".join(secrets.choice(characters) for _ in range(length))


def calculate_entropy(password):
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26

    if re.search(r"[A-Z]", password):
        pool += 26

    if re.search(r"[0-9]", password):
        pool += 10

    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🔐</div>
        <div class="brand-title">SECUREPASS</div>
        <div class="brand-subtitle">ELITE SECURITY</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠  Dashboard", key="nav_dashboard"):
        navigate("Dashboard")
        st.rerun()

    if st.button("🔑  Password Generator", key="nav_generator"):
        navigate("Password Generator")
        st.rerun()

    if st.button("📝  Passphrase Studio", key="nav_passphrase"):
        navigate("Passphrase Studio")
        st.rerun()

    if st.button("🛡️  Password Analyzer", key="nav_analyzer"):
        navigate("Password Analyzer")
        st.rerun()

    if st.button("⚙️  Security Center", key="nav_security"):
        navigate("Security Center")
        st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; padding:15px 5px;">
        <div style="color:#D9B45E;font-size:12px;font-weight:700;">
            YOUR SECURITY MATTERS
        </div>
        <div style="color:#8292AA;font-size:10px;margin-top:8px;">
            Protect your digital identity.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# DASHBOARD
# =====================================================

if st.session_state.page == "Dashboard":

    # HERO SECTION
    # st.html() renders this as HTML. It is deliberately placed
    # here in the Dashboard section, NOT inside the CSS block.

    st.html("""
    <div class="hero">
        <div class="hero-label">WELCOME TO SECUREPASS ELITE</div>

        <div class="hero-title">
            Your Security.<br>
            <span>Your Control.</span>
        </div>

        <div class="hero-description">
            Take control of your digital security with powerful
            password generation, passphrase creation and
            password analysis tools.
        </div>
    </div>
    """)

    # SECURITY OVERVIEW

    st.markdown(
        '<div class="section-title">Security Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html("""
        <div class="overview-card">
            <div class="overview-label">PASSWORD TOOLS</div>
            <div class="overview-value">03</div>
            <div class="overview-note">Powerful security tools</div>
        </div>
        """)

    with col2:
        st.html("""
        <div class="overview-card">
            <div class="overview-label">SECURITY STATUS</div>
            <div class="overview-value">Active</div>
            <div class="overview-note">All tools are operational</div>
        </div>
        """)

    with col3:
        st.html("""
        <div class="overview-card">
            <div class="overview-label">PROTECTION LEVEL</div>
            <div class="overview-value">Enhanced</div>
            <div class="overview-note">Built for stronger passwords</div>
        </div>
        """)

    # EXPLORE TOOLS

    st.markdown(
        '<div class="section-title">Explore Your Tools</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Choose a tool to get started.</div>',
        unsafe_allow_html=True
    )

    # FIRST ROW

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.html("""
        <div class="tool-card">
            <div class="tool-icon">🔐</div>
            <div class="tool-title">Password Generator</div>
            <div class="tool-description">
                Create secure, random passwords with custom controls.
            </div>
        </div>
        """)

        if st.button("CREATE PASSWORD  →", key="dashboard_generator"):
            navigate("Password Generator")
            st.rerun()

    with col2:
        st.html("""
        <div class="tool-card">
            <div class="tool-icon">✦</div>
            <div class="tool-title">Passphrase Studio</div>
            <div class="tool-description">
                Build memorable passphrases using randomly selected words.
            </div>
        </div>
        """)

        if st.button("BUILD PASSPHRASE  →", key="dashboard_passphrase"):
            navigate("Passphrase Studio")
            st.rerun()

    # SECOND ROW

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.html("""
        <div class="tool-card">
            <div class="tool-icon">◆</div>
            <div class="tool-title">Password Analyzer</div>
            <div class="tool-description">
                Review password characteristics and identify weaknesses.
            </div>
        </div>
        """)

        if st.button("ANALYZE PASSWORD  →", key="dashboard_analyzer"):
            navigate("Password Analyzer")
            st.rerun()

    with col2:
        st.html("""
        <div class="tool-card">
            <div class="tool-icon">🛡️</div>
            <div class="tool-title">Security Center</div>
            <div class="tool-description">
                Explore practical steps to protect your accounts.
            </div>
        </div>
        """)

        if st.button("EXPLORE SECURITY  →", key="dashboard_security"):
            navigate("Security Center")
            st.rerun()

    st.html("""
    <div class="footer">
        SECUREPASS ELITE · BUILT FOR BETTER DIGITAL HABITS
    </div>
    """)


# =====================================================
# PASSWORD GENERATOR
# =====================================================

elif st.session_state.page == "Password Generator":

    page_heading(
        "🔑 Password Generator",
        "Create strong, random and secure passwords."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Password Configuration")

        length = st.slider(
            "Password Length",
            min_value=8,
            max_value=128,
            value=16
        )

        count = st.selectbox(
            "Number of Passwords",
            [1, 3, 5, 10]
        )

        st.markdown("### Character Options")

        use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True)
        use_lower = st.checkbox("Lowercase Letters (a-z)", value=True)
        use_numbers = st.checkbox("Numbers (0-9)", value=True)
        use_symbols = st.checkbox("Special Symbols (!@#$)", value=True)

        exclude_similar = st.checkbox(
            "Exclude Similar Characters (I, l, 1, O, 0)",
            value=False
        )

        if st.button("GENERATE PASSWORD", key="generate_password_button"):

            passwords = []

            for _ in range(count):
                password = generate_password(
                    length,
                    use_upper,
                    use_lower,
                    use_numbers,
                    use_symbols,
                    exclude_similar
                )

                if password:
                    passwords.append(password)

            if passwords:
                st.session_state.generated_passwords = passwords
            else:
                st.error("Please select at least one character option.")

    with col2:

        st.markdown("### Generated Results")

        if st.session_state.generated_passwords:

            for index, password in enumerate(
                st.session_state.generated_passwords,
                start=1
            ):
                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-label">PASSWORD {index}</div>
                        <div class="result-value">{html.escape(password)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            all_passwords = "\n".join(st.session_state.generated_passwords)

            st.download_button(
                "⬇️ DOWNLOAD PASSWORDS",
                data=all_passwords,
                file_name="securepass_passwords.txt",
                mime="text/plain"
            )

        else:
            st.info("Your generated passwords will appear here.")


# =====================================================
# PASSPHRASE STUDIO
# =====================================================

elif st.session_state.page == "Passphrase Studio":

    page_heading(
        "📝 Passphrase Studio",
        "Create memorable passphrases using random words."
    )

    word_list = [
        "Ocean", "Mountain", "Silver", "Garden", "Sunshine",
        "River", "Forest", "Crystal", "Thunder", "Rainbow",
        "Galaxy", "Breeze", "Golden", "Shadow", "Planet",
        "Diamond", "Sunset", "Meadow", "Winter", "Rocket",
        "Velvet", "Falcon", "Candle", "Maple", "Castle",
        "Willow", "Marble", "Comet", "Coral", "Lantern",
        "Harbor", "Whisper", "Jasmine", "Cloud", "Phoenix",
        "Aurora", "Copper", "Butterfly", "Island", "Cosmic"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Passphrase Settings")

        word_count = st.slider(
            "Number of Words",
            min_value=3,
            max_value=8,
            value=4
        )

        separator = st.selectbox(
            "Word Separator",
            ["-", "_", ".", "@", " "]
        )

        add_number = st.checkbox(
            "Add a random 3-digit number",
            value=True
        )

        if st.button("GENERATE PASSPHRASE", key="generate_passphrase_button"):

            selected_words = [
                secrets.choice(word_list)
                for _ in range(word_count)
            ]

            passphrase = separator.join(selected_words)

            if add_number:
                passphrase += separator + str(secrets.randbelow(900) + 100)

            st.session_state.generated_passphrase = passphrase

    with col2:

        st.markdown("### Generated Passphrase")

        if st.session_state.generated_passphrase:

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">YOUR PASSPHRASE</div>
                    <div class="result-value">
                        {html.escape(st.session_state.generated_passphrase)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                "⬇️ DOWNLOAD PASSPHRASE",
                data=st.session_state.generated_passphrase,
                file_name="securepass_passphrase.txt",
                mime="text/plain"
            )

        else:
            st.info("Your passphrase will appear here.")


# =====================================================
# PASSWORD ANALYZER
# =====================================================

elif st.session_state.page == "Password Analyzer":

    page_heading(
        "🛡️ Password Analyzer",
        "Evaluate password strength and identify weaknesses."
    )

    st.warning(
        "For safety, avoid entering passwords that you currently "
        "use for real accounts. This basic analyzer does not check "
        "whether a password has appeared in known data breaches."
    )

    password = st.text_input(
        "Enter a sample password to analyze",
        type="password",
        placeholder="Enter a sample password..."
    )

    if st.button("ANALYZE PASSWORD", key="run_password_analysis"):

        if not password:
            st.error("Please enter a password to analyze.")

        else:

            entropy = calculate_entropy(password)

            checks = {
                "At least 8 characters": len(password) >= 8,
                "At least 12 characters": len(password) >= 12,
                "Contains uppercase letters": bool(re.search(r"[A-Z]", password)),
                "Contains lowercase letters": bool(re.search(r"[a-z]", password)),
                "Contains numbers": bool(re.search(r"[0-9]", password)),
                "Contains special symbols": bool(re.search(r"[^a-zA-Z0-9]", password))
            }

            passed = sum(checks.values())

            if len(password) < 8:
                strength = "Very Weak"
            elif entropy < 40:
                strength = "Weak"
            elif entropy < 60:
                strength = "Moderate"
            elif entropy < 80:
                strength = "Strong"
            else:
                strength = "Very Strong"

            st.session_state.analysis_result = {
                "strength": strength,
                "entropy": entropy,
                "checks": checks,
                "passed": passed
            }

    if st.session_state.analysis_result:

        result = st.session_state.analysis_result

        st.markdown("### Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Password Strength", result["strength"])

        with col2:
            st.metric("Estimated Entropy", f"{result['entropy']:.1f} bits")

        with col3:
            st.metric("Security Checks", f"{result['passed']}/6")

        st.markdown("### Security Checklist")

        for check, passed in result["checks"].items():

            if passed:
                st.success(f"✓ {check}")
            else:
                st.error(f"✗ {check}")

        st.caption(
            "Entropy is a rough estimate based on character variety "
            "and password length. It does not guarantee real-world security."
        )


# =====================================================
# SECURITY CENTER
# =====================================================

elif st.session_state.page == "Security Center":

    page_heading(
        "⚙️ Security Center",
        "Learn essential practices to protect your digital identity."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="info-card">
            <h4>🔐 Use Strong Passwords</h4>
            <p>
                Create long passwords using a combination of
                uppercase letters, lowercase letters, numbers
                and special characters.
            </p>
        </div>

        <div class="info-card">
            <h4>🔄 Avoid Password Reuse</h4>
            <p>
                Use a different password for every important
                online account. Reusing passwords increases
                the risk of multiple accounts being compromised.
            </p>
        </div>

        <div class="info-card">
            <h4>🛡️ Enable Two-Factor Authentication</h4>
            <p>
                Add another layer of protection to your accounts
                using an authenticator app, security key or
                another supported verification method.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="info-card">
            <h4>🔑 Use a Password Manager</h4>
            <p>
                A reputable password manager can help you
                generate, store and manage unique passwords
                securely.
            </p>
        </div>

        <div class="info-card">
            <h4>⚠️ Watch Out for Phishing</h4>
            <p>
                Be careful with suspicious links, unexpected
                attachments and websites requesting your
                login information.
            </p>
        </div>

        <div class="info-card">
            <h4>🔍 Review Account Activity</h4>
            <p>
                Regularly check your account login activity
                and security notifications. Change your
                password if you suspect unauthorized access.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# FOOTER FOR OTHER PAGES
# =====================================================

if st.session_state.page != "Dashboard":

    st.markdown("""
    <div class="footer">
        SECUREPASS ELITE · YOUR SECURITY MATTERS
    </div>
    """, unsafe_allow_html=True)