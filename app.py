from dotenv import load_dotenv
import streamlit as st
import os
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Smart Assistant",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Light Gradient CSS Styling
# -----------------------------
st.markdown("""
<style>

/* Soft Light Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}

/* Padding */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
    color: #2c3e50 !important;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 10px !important;
    border: 2px solid #4CAF50 !important;
    background-color: white !important;
    color: black !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(45deg, #4CAF50, #2ecc71);
    color: white;
    font-size: 16px;
    border-radius: 12px;
    padding: 10px 25px;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px #2ecc71;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Functions
# -----------------------------

def translate_text(text, source_language, target_language):
    prompt = f"""
    You are a professional translator.
    Translate the following text from {source_language} to {target_language}.
    Provide only the translated text.

    Text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_itinerary(destination, days, budget, interests):
    prompt = f"""
    Create a {days}-day travel itinerary for {destination}.
    Budget: {budget}
    Interests: {interests}
    Provide a clear day-wise plan including:
    - Places to visit
    - Food suggestions
    - Travel tips
    Format it nicely.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2 = st.tabs(["🌐 Translator", "✈️ Travel Planner"])


# -----------------------------
# Translator Tab
# -----------------------------
with tab1:

    st.title("🌐 AI Language Translator")
    st.write("Translate text between different languages using Gemini AI.")

    text = st.text_area("📝 Enter text to translate:")

    languages = [
        "English", "Spanish", "French",
        "German", "Chinese", "Hindi",
        "Telugu", "Tamil", "Japanese"
    ]

    col1, col2 = st.columns(2)

    with col1:
        source_language = st.selectbox("🌍 Source Language:", languages)

    with col2:
        target_language = st.selectbox("🌍 Target Language:", languages)

    if st.button("🔄 Translate"):

        if text.strip() == "":
            st.warning("⚠️ Please enter some text.")
        elif source_language == target_language:
            st.warning("⚠️ Source and target languages cannot be same.")
        else:
            with st.spinner("Translating..."):
                translated = translate_text(text, source_language, target_language)
            st.success("✅ Translation Completed!")
            st.subheader("🗣️ Translated Text:")
            st.text_area(
             "📄 Output:",
             value=translated,
             height=200
            )

# -----------------------------
# Travel Planner Tab
# -----------------------------
with tab2:

    st.title("✈️ AI Travel Itinerary Generator")
    st.write("Generate smart travel plans using Gemini AI.")

    destination = st.text_input("📍 Enter Destination:")

    days = st.number_input("🗓️ Number of Days:", min_value=1, max_value=14, value=3)

    budget = st.selectbox("💰 Budget Type:", ["Low", "Medium", "Luxury"])

    interests = st.multiselect(
        "🎯 Select Interests:",
        ["Adventure", "Food", "History", "Nature", "Shopping", "Relaxation"]
    )

    if st.button("🚀 Generate Travel Plan"):

        if destination.strip() == "":
            st.warning("⚠️ Please enter a destination.")
        else:
            interest_text = ", ".join(interests)

            with st.spinner("Generating itinerary..."):
                itinerary = generate_itinerary(
                    destination,
                    days,
                    budget,
                    interest_text
                )

            st.success("✅ Travel Plan Generated!")
            st.write(itinerary)
