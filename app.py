import streamlit as st
from pytube import YouTube
import whisper
from gtts import gTTS
import uuid
import os
from pydub import AudioSegment
from pydub.playback import play

st.set_page_config(page_title="TikTok Agent IA", layout="centered")
st.title("🎬 Générateur TikTok IA à partir de YouTube")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

youtube_url = st.text_input("🎥 Colle un lien YouTube ici :")

if youtube_url:
    if st.button("Transcrire et générer audio"):
        try:
            with st.spinner("🔽 Téléchargement en cours..."):
                yt = YouTube(youtube_url)
                video = yt.streams.filter(only_audio=True).first()
                audio_file = f"audio_{uuid.uuid4()}.mp4"
                audio_path = video.download(filename=audio_file)

            with st.spinner("🧠 Transcription avec Whisper..."):
                result = model.transcribe(audio_path)
                text = result["text"]

            st.success("✅ Transcription terminée !")
            st.text_area("📝 Transcription complète :", text, height=200)

            with st.spinner("🔊 Génération de la voix..."):
                tts = gTTS(text[:500], lang="fr")  # max 500 caractères pour gTTS
                tts_path = f"tts_{uuid.uuid4()}.mp3"
                tts.save(tts_path)

            st.audio(tts_path, format='audio/mp3')

            # Nettoyage des fichiers
            os.remove(audio_path)
            os.remove(tts_path)

        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
