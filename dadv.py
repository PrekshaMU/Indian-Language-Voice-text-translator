import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Indian Language Translator", layout="centered")

st.title("🇮🇳 Indian Language Voice + Text Translator (With Voice Output)")

# ---------------------------------------
# SUPPORTED INDIAN LANGUAGES
# ---------------------------------------
indian_languages = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Odia": "or",
    "Urdu": "ur"
}

# ---------------------------------------
# LANGUAGE DROPDOWN
# ---------------------------------------
src_lang = st.selectbox("Select Input Language:", list(indian_languages.keys()))
tgt_lang = st.selectbox("Select Output Language:", list(indian_languages.keys()))

src_code = indian_languages[src_lang]
tgt_code = indian_languages[tgt_lang]

# ---------------------------------------
# TRANSLATION
# ---------------------------------------
def translate_text(text):
    return GoogleTranslator(source=src_code, target=tgt_code).translate(text)

# ---------------------------------------
# TEXT TO SPEECH
# ---------------------------------------
def speak_text(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    return temp.name

# ---------------------------------------
# TEXT INPUT SECTION
# ---------------------------------------
st.subheader("📝 Text Input")

text_in = st.text_input("Enter text:")

if text_in:
    translated = translate_text(text_in)
    st.success("Translated Text:")
    st.write(translated)

    # Voice output
    audio_file = speak_text(translated, tgt_code)
    st.audio(audio_file, format="audio/mp3")

# ---------------------------------------
# SPEECH TO TEXT
# ---------------------------------------
def record_voice(lang_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)  # adjust for 1 second
        st.info("🎤 Speak now...")
        r.pause_threshold = 0.8  # wait for a pause in speech before ending
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)  # max 10 sec
        except sr.WaitTimeoutError:
            return None

    try:
        return r.recognize_google(audio, language=lang_code)
    except:
        return None

# ---------------------------------------
# VOICE INPUT SECTION
# ---------------------------------------
st.subheader("🎙 Voice Input")

if st.button("Start Recording"):
    spoken = record_voice(src_code)

    if spoken:
        st.success("You said:")
        st.write(spoken)

        translated = translate_text(spoken)
        st.success("Translated Output:")
        st.write(translated)

        # Voice output for translated sentence
        audio_file = speak_text(translated, tgt_code)
        st.audio(audio_file, format="audio/mp3")
    else:
        st.error("Could not recognize your voice. Try again!")
