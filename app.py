import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()  # loads GEMINI_API_KEY from a local .env file (for local runs)

st.set_page_config(page_title="AI Medical Image Analysis", page_icon="🩻", layout="wide")

MAX_SIZE = (1024, 1024)  # images are resized to fit within this box

SYSTEM_PROMPT = """You are an AI radiology assistant used for education and \
research. You analyze medical images (X-ray, MRI, CT, ultrasound, etc.) and \
write structured reports. Be precise, cautious, and honest about uncertainty. \
Never claim a definitive diagnosis. If the image is not a medical image or is \
too poor in quality to interpret, say so clearly."""

USER_PROMPT = """Analyze this medical image and respond in Markdown using \
exactly these five sections:

## 1. Image Type & Region
(Modality, body region, view/orientation if identifiable, image quality)

## 2. Key Findings
(Bullet points of visible observations, using proper radiological terminology)

## 3. Diagnostic Assessment
(Possible conditions or differential diagnoses, ranked by likelihood, with \
the reasoning and your level of confidence)

## 4. Patient-Friendly Explanation
(A plain-language summary a non-medical person can understand, avoiding jargon, \
calm in tone)

## 5. Clinical Research Context
(Relevant background on the suspected conditions, typical next steps such as \
further imaging or tests, and general references to guidelines)
{extra}"""


def get_api_key() -> str:
    """Streamlit secrets (cloud) -> environment / .env (local) -> sidebar input."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")


def preprocess(file) -> Image.Image:
    """Open, normalize to RGB, and resize while keeping the aspect ratio."""
    img = Image.open(file)
    img = img.convert("RGB")
    img.thumbnail(MAX_SIZE)
    return img


def analyze(api_key: str, model_name: str, image: Image.Image, extra: str) -> str:
    client = genai.Client(api_key=api_key.strip())
    extra_text = f"\nAdditional context from the user: {extra}" if extra.strip() else ""
    response = client.models.generate_content(
        model=model_name.strip(),
        contents=[USER_PROMPT.format(extra=extra_text), image],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=2048,
        ),
    )
    return response.text.strip()


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("📤 Upload")
    uploaded = st.file_uploader(
        "Medical image", type=["jpg", "jpeg", "png", "bmp"]
    )
    context = st.text_area(
        "Optional clinical context",
        placeholder="e.g. 45-year-old, persistent cough for 3 weeks",
    )

    st.header("⚙️ Settings")
    api_key = get_api_key() or st.text_input("Gemini API key", type="password")
    model_name = st.text_input(
        "Gemini model",
        value="gemini-3.8-flash",
        help="If you get a 'model not found' error, try another current Gemini Flash model name (e.g. gemini-3.7-flash).",
    )
    analyze_btn = st.button("Analyze image", type="primary", use_container_width=True)

# ---------------- Main page ----------------
st.title("🩻 AI-Powered Medical Image Analysis")
st.warning(
    "**Educational use only.** This tool does not provide a medical diagnosis and "
    "must not replace a qualified radiologist or doctor. Do not upload images "
    "that contain personal identifying information."
)

if uploaded is None:
    st.info("Upload an X-ray, MRI, CT scan, or other medical image from the sidebar to begin.")
    st.stop()

try:
    image = preprocess(uploaded)
except Exception as e:
    st.error(f"Could not read this image: {e}")
    st.stop()

col_img, col_report = st.columns([1, 1.4], gap="large")

with col_img:
    st.subheader("Uploaded image")
    st.image(image, caption=f"{uploaded.name} (resized to {image.width}x{image.height})")

with col_report:
    st.subheader("Diagnostic report")
    if analyze_btn:
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                with st.spinner("Analyzing image..."):
                    report = analyze(api_key, model_name, image, context)
                st.session_state["report"] = report
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    if "report" in st.session_state:
        st.markdown(st.session_state["report"])
        st.download_button(
            "Download report (.md)",
            st.session_state["report"],
            file_name="medical_report.md",
            mime="text/markdown",
        )
        st.caption("AI-generated content. Always consult a qualified healthcare professional.")
    else:
        st.write("Click **Analyze image** in the sidebar to generate the report.")