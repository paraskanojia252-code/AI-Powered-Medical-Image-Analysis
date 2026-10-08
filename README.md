# 🩻 AI-Powered Medical Image Analysis Tool

A Streamlit web app that lets users upload a medical image (X-ray, MRI, CT, etc.) and receive a structured, AI-generated report with both technical findings and a plain-language explanation.

**Live app:** <PASTE YOUR STREAMLIT CLOUD LINK HERE>

> ⚠️ **Disclaimer:** This project is for educational purposes only. It does not provide medical diagnoses and is not a substitute for a qualified radiologist or doctor.

## Features

- Upload `.jpg`, `.jpeg`, `.png`, or `.bmp` images from the Streamlit sidebar
- Image preprocessing with Pillow (converted to RGB and resized for consistent handling)
- Google Gemini vision model acts as a radiology assistant
- Markdown report with five sections:
  1. Image Type & Region
  2. Key Findings
  3. Diagnostic Assessment
  4. Patient-Friendly Explanation
  5. Clinical Research Context
- Optional clinical context box and downloadable report

## Tech stack

| Component | Technology |
|---|---|
| Language | Python |
| UI framework | Streamlit |
| Image handling | Pillow (PIL) |
| AI integration | Google Gemini (`gemini-2.5-flash` by default) |
| Env configuration | python-dotenv |
| Deployment | Streamlit Cloud |

Built with plain Python and Streamlit only (no Flask, Django, or LangChain).

## How it works

1. The user uploads an image in the sidebar.
2. Pillow opens it, converts it to RGB, and resizes it to fit within 1024x1024.
3. The image is sent to the Gemini API with a structured prompt.
4. The model returns a Markdown report, which the app displays next to the image.

## API key required

A **Gemini API key** from https://aistudio.google.com/app/apikey

## Run locally

```bash
pip install -r requirements.txt
```

Create a file named `.env` in the project folder:

```
GEMINI_API_KEY=your-key-here
```

Then run:

```bash
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Upload `app.py`, `requirements.txt`, and `README.md` to a public GitHub repo (**do not upload your `.env` file**).
2. Go to https://share.streamlit.io, click **Create app**, and select your repo, branch `main`, and file `app.py`.
3. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
4. Click **Deploy**.

## Example

Upload a chest X-ray. The app returns a report that starts like this:

```
## 1. Image Type & Region
Frontal chest radiograph (PA view), adequate image quality...

## 4. Patient-Friendly Explanation
Your chest X-ray shows the lungs and heart. ...
```

> Replace this with a real output or screenshot from your own run.
