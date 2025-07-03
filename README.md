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
```
## 1. Clone the repo
git clone https://github.com/your-username/sahaayika.git
cd sahaayika

## 2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate          # On Windows

## 3. Install dependencies
pip install -r requirements.txt

## Run the App
python app.py
This will launch the Gradio interface in your browser.

## Docker Setup (Optional)
If you want to run Sahaayika inside a Docker container:

1. Build the Docker image:
docker build -t sahaayika-app .
3. Run the container
docker run -p 7860:7860 sahaayika-app

Then open http://localhost:7860 in your browser.


## Sample Use Case
Upload a photo of a form or handwritten note.

Select your profile and preferred language.

Listen to the translated text in your language.

Optionally speak a question — Sahaayika will respond.

## Limitations & Future Work
OCR depends on image quality

TTS may take 2–3 seconds for output

Currently online TTS (gTTS) is used – to be replaced with offline option in future

Future: tone customization based on profile (e.g. formal/informal voices)

## Acknowledgements
Built as part of the Kaggle Hackathon / Gemma 3n Challenge

Special thanks to open-source tools: Tesseract, Gradio, gTTS, and Deep Translator

## License
This project is open-sourced under the MIT License.

## Contributing
Pull requests are welcome! Feel free to fork the repo and contribute.

## Let's Connect
If you liked this project, feel free to give it a star ⭐ and share it with your network!



