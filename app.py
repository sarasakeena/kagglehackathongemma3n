import re
import gradio as gr
import requests
from PIL import Image
import pytesseract
from gtts import gTTS
from deep_translator import GoogleTranslator
import uuid
import time
import speech_recognition as sr
import json

# ✅ Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
# ✅ Ollama Endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# ✅ OCR using Tesseract
def simulate_ocr(image):
    try:
        raw_text = pytesseract.image_to_string(image, lang='tam+eng').strip()

        cleaned_lines = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # ✅ Remove markdown-style leading decorations
            line = re.sub(r'^[\*\:\-\_>#\s]+', '', line)

            # ✅ Remove stray asterisks or markdown marks anywhere in line
            line = re.sub(r'[\*\_]+', '', line)  # single or multiple * or _
            line = re.sub(r'[•●■▪︎◆★☆※§]', '', line)  # Remove common bullet marks too

            # ✅ Remove any space-surrounded asterisks (like `* word *`)
            line = re.sub(r'\s*\*\s*', ' ', line)

            # ✅ Remove non-ASCII Unicode asterisk variants
            line = re.sub(r'[﹡＊✱✳︎⁎]', '', line)

            # ✅ Filter out typical OCR system noise
            if not any(bad in line.lower() for bad in [
                "tesseract", "ocr failed", "readme", "error", "path not", "not installed"
            ]):
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    except Exception as e:
        return f"OCR failed: {str(e)}"
def clean_special_chars(text):
    # Remove markdown-style **bold**, ***triple asterisks***, etc.
    text = re.sub(r'\*{1,3}', '', text)
    # Remove other common markdown bullets or leftover formatting
    text = re.sub(r'[•●■▪︎◆★☆※§]', '', text)
    return text.strip()


# ✅ User profile context
def get_profile_context(profile):
    return {
        "Woman": "Explain in very simple language for a rural woman.",
        "Farmer": "Explain for a rural woman who is a farmer.",
        "Elderly": "Explain slowly and clearly for an elderly rural woman.",
        "Other": "Explain simply for someone unfamiliar with formal documents."
    }.get(profile, "Explain in simple language.")

# ✅ Translate output
def translate_text(text, lang):
    lang_code = {'Hindi': 'hi', 'Tamil': 'ta'}.get(lang)
    if not lang_code:
        return text
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# ✅ Text-to-Speech
def speak(text, lang):
    lang_code = {'Hindi': 'hi', 'Tamil': 'ta', 'English': 'en'}.get(lang, 'en')
    filename = f"audio_{uuid.uuid4().hex[:6]}.mp3"
    try:
        gTTS(text=text, lang=lang_code).save(filename)
        return filename
    except:
        return None

# ✅ Call Ollama Model with Streaming
def call_ollama_stream(prompt):
    print("📨 Prompt sent to Ollama:\n", prompt)
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "gemma3n:latest",
                "prompt": prompt,
                "system_prompt": "You are a helpful assistant.",
                "stream": True
            },
            stream=True,
            timeout=200
        )
        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = line.decode("utf-8").replace("data: ", "")
                    data = json.loads(chunk)
                    full_reply += data.get("response", "")
                except Exception as e:
                    print("🔴 JSON Parse Error:", e)
                    continue
        return full_reply.strip() or "❌ No response from model."
    except Exception as e:
        return f"❌ Ollama server error: {str(e)}"

# ✅ Handle uploaded image
def process_image(image, language, profile):
    start = time.time()
    extracted_text = simulate_ocr(image)
    if not extracted_text:
        return "⚠️ Could not extract any text from the uploaded image. Please try a clearer image.", None

    instruction = get_profile_context(profile)

    lower_text = extracted_text.lower()
    if any(term in lower_text for term in ["medicine", "pesticide", "tablet", "spray", "dosage", "chemical", "mg", "ml"]):
        suffix = (
            "Please explain what the medicine, pesticide, or chemical is for, how to use it, and warn of any safety risks."
        )
    else:
        suffix = (
            "Please explain what this document is about, and help the user understand the key information clearly."
        )

    prompt = (
        f"{instruction}\n\n"
        f"The following text was extracted from a document:\n\n"
        f"{extracted_text}\n\n"
        f"{suffix}"
    )

    result = call_ollama_stream(prompt)
    cleaned = clean_special_chars(result)
    translated = translate_text(cleaned, language)

    audio = speak(translated, language)
    return f"⏱️ Took {time.time() - start:.2f} sec\n\n{translated}", audio

# ✅ Transcribe voice
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio) # type: ignore
    except:
        return ""

# ✅ Handle user doubt
def handle_doubt(doubt_text_input, doubt_audio_input, language, profile, image):
    if doubt_audio_input:
        doubt_text_input = transcribe_audio(doubt_audio_input)
    if not doubt_text_input:
        return "⚠️ Please enter or record a question.", None

    context = simulate_ocr(image)
    prompt = (
        f"Earlier, you explained this document:\n\n{context}\n\n"
        f"The user has a follow-up question:\n\n{doubt_text_input}\n\n"
        f"Answer clearly in simple English suitable for a rural audience."
    )
    answer = call_ollama_stream(prompt)
    cleaned = clean_special_chars(answer)
    translated = translate_text(cleaned, language)

    audio = speak(translated, language)
    return translated, audio

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🌸 Sahaayika — AI Visual Assistant for Rural Women")

    with gr.Row():
        image_input = gr.Image(
            type="pil",
            label="📸 Upload an Image",
            sources=["upload"]  # Only allow file upload, no webcam/clipboard
        )

        language_input = gr.Radio(
            ["Hindi", "Tamil", "English"],
            label="🌍 Output Language",
            value="English"
        )

        profile_input = gr.Dropdown(
            ["Woman", "Farmer", "Elderly", "Other"],
            label="👤 Profile Type",
            value="Woman"
        )

    output_text = gr.Textbox(label="📝 Simplified Explanation", lines=10)
    output_audio = gr.Audio(type="filepath", label="🔊 Listen")

    gr.Button("🧠 Understand Image").click(
        fn=process_image,
        inputs=[image_input, language_input, profile_input],
        outputs=[output_text, output_audio]
    )

    gr.Markdown("## ❓ Ask a Doubt")

    with gr.Row():
        doubt_text = gr.Textbox(label="❓ Type Your Doubt")
        doubt_audio_input = gr.Audio(
            type="filepath",
            label="🎙️ Upload Your Voice Question",
            sources=["upload"]  # Only allow file upload, no microphone/clipboard
        )

    doubt_response_text = gr.Textbox(label="📖 Answer", lines=6)
    doubt_audio_output = gr.Audio(type="filepath", label="🔊 Spoken Answer")

    gr.Button("📩 Ask Doubt").click(
        fn=handle_doubt,
        inputs=[doubt_text, doubt_audio_input, language_input, profile_input, image_input],
        outputs=[doubt_response_text, doubt_audio_output]
    )

demo.launch()
