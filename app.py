from pathlib import Path

import joblib
import streamlit as st

# Paths relative to project root (where app.py lives)
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "model" / "model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "model" / "vectorizer.pkl"

st.set_page_config(page_title="LobbyWatch India MVP")

# Support BOTH setups: (1) only model.pkl = pipeline, or (2) vectorizer.pkl + model.pkl = separate
@st.cache_resource
def load_model_and_vectorizer():
    has_vectorizer = VECTORIZER_PATH.exists()
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH) if has_vectorizer else None
    return model, vectorizer

model, vectorizer = load_model_and_vectorizer()

def predict(text: str):
    if vectorizer is not None:
        X = vectorizer.transform([text])
        return model.predict(X)[0]
    return model.predict([text])[0]

st.title("LobbyWatch India – Relation Detector")
st.write("Enter a public sector sentence and the model will classify the type of interaction.")

user_input = st.text_area("Enter sentence:")

if st.button("Predict Relation"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        prediction = predict(user_input)
        st.success(f"Predicted Relation Type: **{prediction}**")
