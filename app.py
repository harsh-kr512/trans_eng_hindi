import streamlit as st
import openai
from dotenv import load_dotenv
import os
from auth import verify_user, register_user

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key = OPENAI_API_KEY)

# --- OpenAI Chat Function ---
def translate_to_hindi(english_text,model):
    try:
        response = client.chat.completions.create(
        # model="ft:gpt-4.1-nano-2025-04-14:personal:trans1:BxR1FpxF",
        #model = "gpt-4.1-nano",
        model = model,
        messages=[
            {"role": "system", "content": "You are an expert English to Hindi translator. Always provide a clear and accurate Hindi translation along with a simple real-life example sentence in both English and Hindi to help users understand the context easily."},
            {"role": "user", "content": f"Translate{english_text}"}
        ]
    )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI 
st.set_page_config("English to Hindi Translator", page_icon="🈯")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Authentication Pages
if not st.session_state.authenticated:
    menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

    if menu == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    elif menu == "Sign Up":
        st.title("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            success, msg = register_user(new_username, new_password)
            if success:
                st.success(msg)
                st.info("Go to Login to access the app.")
            else:
                st.warning(msg)

# Main App
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.experimental_rerun()

    st.title("English to Hindi Translator")
    st.markdown("Use AI to translate English text into Hindi with real-world examples.")

    # Select model
    model_choice = st.radio(
        "Select the model to use:",
        ["Fine-tuned Model", "Standard GPT Model"],
        index=0,
        help="Fine-tuned model may give more context-aware translations."
    )

    # Map model name
    model = (
        "ft:gpt-4.1-nano-2025-04-14:personal:trans1:BxR1FpxF"
        if model_choice == "Fine-tuned Model"
        else "gpt-4.1-nano"
    )

    english_input = st.text_area("Enter English sentence to translate", height=100)

    if st.button("Translate"):
        if english_input.strip() == "":
            st.warning("Please enter a sentence")
        else:
            hindi_output = translate_to_hindi(english_input,model)
            st.success("Hindi Translation:")
            st.write(hindi_output)
