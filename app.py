
import streamlit as st
import secrets
import string

st.set_page_config(
    page_title="Random Password Generator",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Random Password Generator")
st.write("Generate a strong, random password in seconds.")

length = st.slider(
    "Select password length",
    min_value=8,
    max_value=64,
    value=16
)

use_letters = st.checkbox("Include letters (A-Z, a-z)", value=True)
use_digits = st.checkbox("Include numbers (0-9)", value=True)
use_symbols = st.checkbox("Include special characters", value=True)

if st.button("Generate Password", type="primary"):
    characters = ""

    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        st.error("Please select at least one character type.")
    else:
        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        st.success("Password generated successfully!")
        st.code(password, language=None)
        st.caption(f"Password length: {length} characters")

        st.download_button(
            label="Download Password",
            data=password,
            file_name="password.txt",
            mime="text/plain"
        )

st.divider()
st.caption("Built with Python, Streamlit, and the secrets module.")
