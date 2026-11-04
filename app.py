
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
# CSS DESIGN
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #080F20;
    --sidebar: #0D172B;
    --card: #111E35;
    --gold: #E6BD65;
    --gold-light: #FFD58B;
    --gold-dark: #F2BD65;
    --text: #F5F2EA;
    --muted: #A9B2C3;
    --brown: #80603B;
}

.stApp {
    background: var(--navy);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =====================================================
   REMOVE DEPLOY BUTTON
===================================================== */

/* Streamlit Deploy button selectors */
.stDeployButton,
[data-testid="stDeployButton"],
[data-testid="stAppDeployButton"],
button[data-testid="stAppDeployButton"],
div[data-testid="stAppDeployButton"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Hide only the Deploy control, not the complete header */
header[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* Keep sidebar controls visible */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    color: #FFD58B !important;
    background: #111E35 !important;
    border: 1px solid rgba(230,189,101,0.45) !important;
    border-radius: 8px !important;
    z-index: 999999 !important;
}

button[data-testid="stSidebarCollapseButton"] svg,
button[data-testid="stSidebarCollapsedControl"] svg {
    color: #FFD58B !important;
    fill: #FFD58B !important;
}

/* Hide unnecessary elements */
footer {
    visibility: hidden !important;
}

#MainMenu {
    visibility: hidden !important;
}

/* =====================================================
   MAIN CONTENT
===================================================== */

.stApp [data-testid="stMain"] {
    background: #080F20 !important;
}

.stApp [data-testid="stMain"] .block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1500px !important;
}

/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background: #0D172B !important;
    border-right: 1px solid rgba(230,189,101,0.18);
}

section[data-testid="stSidebar"] > div {
    background: #0D172B !important;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: #F5F2EA;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] {
    width: 100% !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    width: 100% !important;
    min-height: 48px !important;
    border-radius: 9px !important;
    border: 1px solid rgba(230,189,101,0.18) !important;
    background: #111E35 !important;
    color: #E9EAF0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
    transition: 0.2s ease !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: rgba(230,189,101,0.15) !important;
    border-color: #E6BD65 !important;
    color: #FFD58B !important;
}

/* =====================================================
   HEADINGS
===================================================== */

.main-title {
    color: #FFD58B;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.section-title {
    color: #FFD58B;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 8px;
}

.subtitle {
    color: #A9B2C3;
    font-size: 14px;
    line-height: 1.7;
}

/* =====================================================
   HERO SECTION
===================================================== */

.hero {
    background: linear-gradient(120deg, #142440, #101B31);
    border: 1px solid rgba(230,189,101,0.35);
    border-radius: 18px;
    padding: 38px;
    margin-bottom: 25px;
}

.hero h1 {
    color: #FFD58B;
    font-size: 36px;
    font-weight: 800;
    margin: 0 0 12px 0;
}

.hero p {
    color: #C5CBD6;
    font-size: 15px;
    line-height: 1.7;
    margin: 0;
}

/* =====================================================
   OVERVIEW CARDS
===================================================== */

.overview-card {
    background: #111E35;
    border: 1px solid rgba(230,189,101,0.25);
    border-radius: 14px;
    padding: 22px;
    min-height: 125px;
}

.overview-card h3 {
    color: #FFD58B;
    font-size: 24px;
    margin: 0 0 8px 0;
    font-weight: 800;
}

.overview-card p {
    color: #A9B2C3;
    font-size: 12px;
    margin: 0;
}

/* =====================================================
   TOOL CARDS
===================================================== */

.tool-card {
    background: #111E35;
    border: 1px solid rgba(230,189,101,0.25);
    border-radius: 14px;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 12px;
}

.tool-card h3 {
    color: #FFD58B;
    font-size: 17px;
    font-weight: 700;
    margin: 0 0 10px 0;
}

.tool-card p {
    color: #A9B2C3;
    font-size: 12px;
    line-height: 1.6;
    margin: 0;
}

/* =====================================================
   RESULT AND INFORMATION CARDS
===================================================== */

.result-box {
    background: #111E35;
    border: 1px solid rgba(230,189,101,0.4);
    border-radius: 12px;
    padding: 18px;
    margin: 12px 0;
    color: #FFD58B;
    overflow-wrap: anywhere;
}

.info-card {
    background: #111E35;
    border: 1px solid rgba(230,189,101,0.25);
    border-radius: 12px;
    padding: 20px;
    min-height: 145px;
    margin-bottom: 12px;
}

.info-card h4 {
    color: #FFD58B;
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 10px 0;
}

.info-card p {
    color: #A9B2C3;
    font-size: 12px;
    line-height: 1.7;
    margin: 0;
}

/* =====================================================
   MAIN AREA GOLD BUTTONS
===================================================== */

.stApp [data-testid="stMain"] div[data-testid="stButton"] {
    width: 100% !important;
    max-width: 100% !important;
    display: block !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    height: 58px !important;
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
    font-weight: 700 !important;
}

.stApp [data-testid="stMain"] div[data-testid="stButton"] > button:hover {
    background: linear-gradient(90deg, #FFD58B, #FFE3AF) !important;
    border-color: #FFD58B !important;
    transform: translateY(-1px);
}

/* =====================================================
   DOWNLOAD BUTTONS
===================================================== */

.stApp [data-testid="stMain"] div[data-testid="stDownloadButton"] {
    width: 100% !important;
}

.stApp [data-testid="stMain"] div[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    min-height: 52px !important;
    background: linear-gradient(90deg, #F2BD65, #FFD58B) !important;
    color: #80603B !important;
    -webkit-text-fill-color: #80603B !important;
    border: 1px solid #E9B95F !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
}

.stApp [data-testid="stMain"] div[data-testid="stDownloadButton"] > button p,
.stApp [data-testid="stMain"] div[data-testid="stDownloadButton"] > button span {
    color: #80603B !important;
    -webkit-text-fill-color: #80603B !important;
}

/* =====================================================
   INPUT FIELDS
===================================================== */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background: #111E35 !important;
    color: #F5F2EA !important;
    border-color: rgba(230,189,101,0.35) !important;
    border-radius: 8px !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label,
.stSlider label,
.stCheckbox label {
    color: #D8DCE5 !important;
    font-weight: 600 !important;
}

.stCheckbox span {
    color: #D8DCE5 !important;
}

.stSlider [data-baseweb="slider"] {
    color: #FFD58B !important;
}

/* DIVIDER */
hr {
    border-color: rgba(230,189,101,0.2) !important;
}

/* FOOTER */
.custom-footer {
    text-align: center;
    color: #7F8A9D;
    font-size: 11px;
    padding: 25px 0 10px 0;
    border-top: 1px solid rgba(230,189,101,0.15);
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def go_to_page(page_name):
    st.session_state.page = page_name


def generate_password(length, use_upper, use_lower, use_numbers,
                      use_symbols, exclude_similar):

    characters = ""

    if use_upper:
        characters += string.ascii_uppercase

    if use_lower:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += "!@#$%^&*()-_=+[]{};:,.?/"

    if exclude_similar:
        for char in "Il1O0o":
            characters = characters.replace(char, "")

    if not characters:
        return None

    return "".join(
        secrets.choice(characters) for _ in range(length)
    )


def generate_passphrase(number_of_words, separator, add_number):

    words = [
        "amber", "anchor", "apple", "artist", "autumn",
        "beacon", "breeze", "candle", "castle", "cedar",
        "cloud", "coffee", "comet", "crystal", "daisy",
        "desert", "dream", "eagle", "earth", "ember",
        "forest", "galaxy", "garden", "golden", "harbor",
        "horizon", "island", "jungle", "lantern", "lemon",
        "marble", "meadow", "moon", "mountain", "ocean",
        "pearl", "planet", "river", "silver", "sunrise"
    ]

    selected_words = [
        secrets.choice(words) for _ in range(number_of_words)
    ]

    phrase = separator.join(selected_words)

    if add_number:
        phrase += separator + str(secrets.randbelow(900) + 100)

    return phrase


def calculate_entropy(password):

    pool_size = 0

    if re.search(r"[a-z]", password):
        pool_size += 26

    if re.search(r"[A-Z]", password):
        pool_size += 26

    if re.search(r"[0-9]", password):
        pool_size += 10

    if re.search(r"[^a-zA-Z0-9]", password):
        pool_size += 32

    if pool_size == 0:
        return 0

    return len(password) * math.log2(pool_size)


def analyze_password(password):

    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains uppercase letters": bool(re.search(r"[A-Z]", password)),
        "Contains lowercase letters": bool(re.search(r"[a-z]", password)),
        "Contains numbers": bool(re.search(r"[0-9]", password)),
        "Contains symbols": bool(re.search(r"[^a-zA-Z0-9]", password)),
        "No obvious common patterns": not bool(
            re.search(
                r"1234|password|qwerty|abcd|1111",
                password.lower()
            )
        )
    }

    entropy = calculate_entropy(password)

    if entropy < 28:
        strength = "Very Weak"
    elif entropy < 36:
        strength = "Weak"
    elif entropy < 60:
        strength = "Moderate"
    elif entropy < 80:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return checks, entropy, strength


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 5px 25px 5px;">
        <div style="font-size: 30px;">🔐</div>
        <div style="color:#FFD58B;font-size:20px;font-weight:800;letter-spacing:1px;">
            SECUREPASS
        </div>
        <div style="color:#A9B2C3;font-size:10px;letter-spacing:3px;">
            ELITE SECURITY SUITE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#7F8A9D;font-size:10px;font-weight:700;letter-spacing:2px;'>MAIN MENU</p>",
        unsafe_allow_html=True
    )

    navigation = [
        ("🏠", "Dashboard"),
        ("🔑", "Password Generator"),
        ("💬", "Passphrase Studio"),
        ("🛡️", "Password Analyzer"),
        ("⚙️", "Security Center")
    ]

    for icon, page_name in navigation:

        if st.button(
            f"{icon}   {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True
        ):
            go_to_page(page_name)
            st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="background:#111E35;border:1px solid rgba(230,189,101,0.2);
                border-radius:12px;padding:15px;">
        <div style="color:#FFD58B;font-size:12px;font-weight:700;">
            SYSTEM OPERATIONAL
        </div>
        <div style="color:#A9B2C3;font-size:11px;margin-top:6px;">
            Your security workspace is ready.
        </div>
        <div style="color:#5ED6A0;font-size:11px;margin-top:12px;">
            ● All systems active
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# DASHBOARD
# =====================================================

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Your Security. Your Control.</h1>
        <p>
            Welcome to SECUREPASS ELITE — your personal password
            security workspace. Create stronger passwords, build
            memorable passphrases and understand password security
            with simple tools.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Everything you need to manage password security.</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="overview-card">
            <h3>Strong Passwords</h3>
            <p>Create passwords that help keep your accounts safe.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="overview-card">
            <h3>5 Tools</h3>
            <p>Dedicated password security features</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="overview-card">
            <h3>100%</h3>
            <p>Designed for simple and accessible use</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">EXPLORE YOUR TOOLS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Choose a tool to get started.</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown("""
        <div class="tool-card">
            <h3>🔑 Password Generator</h3>
            <p>
                Generate strong, random passwords with custom
                length and character options.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "OPEN PASSWORD GENERATOR",
            key="dashboard_generator",
            use_container_width=True
        ):
            go_to_page("Password Generator")
            st.rerun()

        st.markdown("""
        <div class="tool-card">
            <h3>🛡️ Password Analyzer</h3>
            <p>
                Review password characteristics and understand
                estimated strength.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "OPEN PASSWORD ANALYZER",
            key="dashboard_analyzer",
            use_container_width=True
        ):
            go_to_page("Password Analyzer")
            st.rerun()

    with col2:

        st.markdown("""
        <div class="tool-card">
            <h3>💬 Passphrase Studio</h3>
            <p>
                Create memorable passphrases using randomly
                selected words.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "OPEN PASSPHRASE STUDIO",
            key="dashboard_passphrase",
            use_container_width=True
        ):
            go_to_page("Passphrase Studio")
            st.rerun()

        st.markdown("""
        <div class="tool-card">
            <h3>⚙️ Security Center</h3>
            <p>
                Learn practical ways to protect your accounts
                and improve online safety.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "OPEN SECURITY CENTER",
            key="dashboard_security",
            use_container_width=True
        ):
            go_to_page("Security Center")
            st.rerun()


# =====================================================
# PASSWORD GENERATOR
# =====================================================

elif st.session_state.page == "Password Generator":

    st.markdown(
        '<div class="section-title">PASSWORD GENERATOR</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Create strong and unpredictable passwords.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

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

    with col2:

        st.markdown("**Character Options**")

        use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True)
        use_lower = st.checkbox("Lowercase Letters (a-z)", value=True)
        use_numbers = st.checkbox("Numbers (0-9)", value=True)
        use_symbols = st.checkbox("Symbols (!@#$...)", value=True)
        exclude_similar = st.checkbox("Exclude Similar Characters", value=False)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "GENERATE SECURE PASSWORDS",
        key="generate_passwords",
        use_container_width=True
    ):

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

        if not passwords:
            st.error("Please select at least one character type.")

        else:
            st.session_state.generated_passwords = passwords

    if st.session_state.generated_passwords:

        st.markdown("---")

        st.markdown(
            '<div class="section-title">GENERATED PASSWORDS</div>',
            unsafe_allow_html=True
        )

        for index, password in enumerate(
            st.session_state.generated_passwords,
            start=1
        ):

            st.markdown(
                f"""
                <div class="result-box">
                    <div style="color:#A9B2C3;font-size:11px;margin-bottom:8px;">
                        PASSWORD {index}
                    </div>
                    <div style="font-size:18px;font-weight:700;">
                        {html.escape(password)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        password_text = "\n".join(
            st.session_state.generated_passwords
        )

        st.download_button(
            "⬇ DOWNLOAD PASSWORDS",
            data=password_text,
            file_name="securepass_passwords.txt",
            mime="text/plain",
            use_container_width=True
        )


# =====================================================
# PASSPHRASE STUDIO
# =====================================================

elif st.session_state.page == "Passphrase Studio":

    st.markdown(
        '<div class="section-title">PASSPHRASE STUDIO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Create memorable combinations of random words.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        number_of_words = st.slider(
            "Number of Words",
            min_value=3,
            max_value=8,
            value=4
        )

        separator = st.selectbox(
            "Word Separator",
            ["-", "_", ".", "@", " "]
        )

    with col2:

        add_number = st.checkbox(
            "Add a random three-digit number",
            value=True
        )

        st.markdown("""
        <div class="info-card">
            <h4>Why use a passphrase?</h4>
            <p>
                A passphrase combines several words to create
                something easier to remember while allowing
                longer password combinations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    if st.button(
        "GENERATE PASSPHRASE",
        key="generate_passphrase",
        use_container_width=True
    ):

        st.session_state.generated_passphrase = generate_passphrase(
            number_of_words,
            separator,
            add_number
        )

    if st.session_state.generated_passphrase:

        st.markdown("---")

        st.markdown(
            '<div class="section-title">YOUR PASSPHRASE</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-box">
                <div style="font-size:22px;font-weight:700;">
                    {html.escape(st.session_state.generated_passphrase)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            "⬇ DOWNLOAD PASSPHRASE",
            data=st.session_state.generated_passphrase,
            file_name="securepass_passphrase.txt",
            mime="text/plain",
            use_container_width=True
        )


# =====================================================
# PASSWORD ANALYZER
# =====================================================

elif st.session_state.page == "Password Analyzer":

    st.markdown(
        '<div class="section-title">PASSWORD ANALYZER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Understand the characteristics of a password.</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h4>🔒 Privacy Reminder</h4>
        <p>
            For safety, do not enter a real password that you currently
            use. Test with a sample password instead.
        </p>
    </div>
    """, unsafe_allow_html=True)

    password_input = st.text_input(
        "Enter a sample password",
        type="password",
        placeholder="Enter a sample password..."
    )

    if st.button(
        "ANALYZE PASSWORD",
        key="analyze_password",
        use_container_width=True
    ):

        if not password_input:
            st.warning("Please enter a sample password.")

        else:
            checks, entropy, strength = analyze_password(password_input)

            st.session_state.analysis_result = {
                "checks": checks,
                "entropy": entropy,
                "strength": strength
            }

    if st.session_state.analysis_result:

        result = st.session_state.analysis_result

        st.markdown("---")

        st.markdown(
            '<div class="section-title">ANALYSIS RESULTS</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(f"""
            <div class="overview-card">
                <h3>{result["strength"]}</h3>
                <p>Estimated Password Strength</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="overview-card">
                <h3>{result["entropy"]:.1f} bits</h3>
                <p>Estimated Entropy</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">SECURITY CHECKLIST</div>',
            unsafe_allow_html=True
        )

        for check, passed in result["checks"].items():

            if passed:
                st.success(f"✓ {check}")

            else:
                st.warning(f"✗ {check}")

        st.caption(
            "Note: This is an educational estimate, not a complete "
            "security audit. It does not check breached-password databases."
        )


# =====================================================
# SECURITY CENTER
# =====================================================

elif st.session_state.page == "Security Center":

    st.markdown(
        '<div class="section-title">SECURITY CENTER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Simple habits that help protect your digital life.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    security_tips = [
        (
            "🔐 Use Unique Passwords",
            "Avoid reusing the same password across multiple websites. "
            "If one account is compromised, unique passwords help protect your other accounts."
        ),
        (
            "🛡️ Enable Two-Factor Authentication",
            "Add another layer of protection to important accounts using "
            "an authenticator app or another supported verification method."
        ),
        (
            "🔄 Update Your Passwords When Needed",
            "Change passwords immediately if you suspect an account has "
            "been compromised or exposed."
        ),
        (
            "🚫 Avoid Sharing Passwords",
            "Never share passwords through public messages, emails or "
            "untrusted websites."
        ),
        (
            "🔎 Watch Out for Phishing",
            "Check website addresses and sender details before clicking "
            "links or entering account information."
        ),
        (
            "🔑 Consider a Password Manager",
            "A reputable password manager can help create and store "
            "unique passwords for different accounts."
        )
    ]

    col1, col2 = st.columns(2, gap="large")

    for index, (title, description) in enumerate(security_tips):

        target_col = col1 if index % 2 == 0 else col2

        with target_col:

            st.markdown(
                f"""
                <div class="info-card">
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="custom-footer">
    SECUREPASS ELITE · YOUR SECURITY. YOUR CONTROL.
    <br><br>
    Designed to make password security simple.
</div>
""", unsafe_allow_html=True)
