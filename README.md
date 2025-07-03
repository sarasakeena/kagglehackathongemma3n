# 🌸 Sahaayika – AI Visual Assistant for Rural Women

**Sahaayika** (meaning “female assistant” in Sanskrit) is an offline, multilingual AI-powered visual assistant that helps users—especially rural or underserved women—understand printed or handwritten text through a combination of **OCR**, **translation**, **speech-to-text**, and **text-to-speech**.

---

## 🔍 Features

- 📸 **Image-to-Text (OCR):** Extracts text from printed or handwritten documents
- 🌐 **Translation:** Converts extracted text into Tamil, Hindi, or English
- 🔊 **Text-to-Speech:** Speaks the translated text aloud
- 🎤 **Speech Recognition:** Converts spoken input to text
- 🧕 **Profile-based Experience:** Language and profile selection for personalized output
- 💻 **Offline Capability:** Works without internet (except during initial install)
- 🌈 **Clean Gradio UI:** Simple and accessible interface for all users

---

## 🛠️ Tech Stack

- `Python`
- `Gradio` for UI
- `PyTesseract` for OCR
- `gTTS` for text-to-speech
- `deep_translator` for translations
- `SpeechRecognition` for voice input
- `OpenCV` for image preprocessing

---

## 📦 Requirements

Make sure you have **Python 3.8+** installed.  
Install Tesseract-OCR manually for your OS:

### Windows:
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Then set the Tesseract path in your code:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 1. Clone the repo
git clone https://github.com/your-username/sahaayika.git
cd sahaayika

# 2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate          # On Windows

# 3. Install Python dependencies
pip install -r requirements.txt
