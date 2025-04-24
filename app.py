import streamlit as st
from pytube import YouTube
import whisper
import requests
import uuid
import os

# 🔑 Clé API ElevenLabs (remplace ici par ta vraie clé)
os.environ["ELEVENLABS_API_KEY"] = "sk_f053d1f1b76bc9987e47399c4a3355bd78936af2fd18fc0e"
api_key = os.getenv("ELEVENLABS_API_KEY")

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
            with st.spinner("🔽 Téléchargement de l'audio..."):
                yt = YouTube(youtube_url)
                video = yt.streams.filter(only_audio=True).first()
                audio_filename = f"audio_{uuid.uuid4()}.mp4"
                audio_path = video.download(filename=audio_filename)

            with st.spinner("🧠 Transcription en cours..."):
                result = model.transcribe(audio_path)
                text = result["text"]

            # Affichage de la transcription
            st.success("✅ Transcription terminée !")
            st.text_area("📝 Transcription complète :", text, height=200)

            # Envoi à ElevenLabs
            with st.spinner("🔊 Génération de la voix (ElevenLabs)..."):
                VOICE_ID = "TxGEqnHWrfWFTfGW9XjX"  # Voix par défaut : Rachel (FR dispo si changé)
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
                headers = {
                    "xi-api-key": api_key,
                    "Content-Type": "application/json"
                }
                payload = {
                    "text": text[:500],  # max recommandé
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    audio_output_path = f"voice_{uuid.uuid4()}.mp3"
                    with open(audio_output_path, "wb") as f:
                        f.write(response.content)
                    st.audio(audio_output_path, format="audio/mp3")
                else:
                    st.error(f"Erreur : {response.status_code} - {response.text}")

            # Nettoyage
            os.remove(audio_path)

        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
