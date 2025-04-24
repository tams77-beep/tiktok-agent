import streamlit as st
from pytube import YouTube
import whisper
import os
import uuid
from moviepy.editor import AudioFileClip, TextClip, ColorClip, CompositeVideoClip
from gtts import gTTS

st.set_page_config(page_title="TikTok Video Generator", layout="centered")
st.title("Agent IA - TikTok à partir d'un reportage YouTube")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

youtube_url = st.text_input("Colle ici ton lien YouTube :")

if youtube_url:
    try:
        yt = YouTube(youtube_url)
        st.video(youtube_url)

        if st.button("Télécharger et analyser"):
            with st.spinner("Téléchargement en cours..."):
                video = yt.streams.filter(only_audio=True).first()
                filename = f"audio_{uuid.uuid4()}.mp4"
                audio_path = video.download(filename=filename)

            with st.spinner("Transcription avec Whisper..."):
                result = model.transcribe(audio_path)
                segments = result['segments'][:5]
                st.success("Transcription terminée. Sélectionne les extraits à transformer.")

                selected_segments = []
                for i, seg in enumerate(segments):
                    if st.checkbox(f"{seg['start']:.2f}s - {seg['end']:.2f}s : {seg['text'][:60]}..."):
                        selected_segments.append(seg)

                if selected_segments and st.button("Générer vidéos TikTok"):
                    for seg in selected_segments:
                        tiktok_filename = f"tiktok_{uuid.uuid4()}.mp4"
                        tts_path = f"voice_{uuid.uuid4()}.mp3"

                        tts = gTTS(seg['text'], lang='fr')
                        tts.save(tts_path)

                        clip = AudioFileClip(tts_path)
                        text_clip = TextClip(seg['text'], fontsize=24, color='white', bg_color='black', size=(720, 100)).set_duration(clip.duration).set_position(('center', 'bottom'))

                        video = ColorClip(size=(720, 1280), color=(0, 0, 0), duration=clip.duration).set_audio(clip)
                        final = CompositeVideoClip([video, text_clip])
                        final.write_videofile(tiktok_filename, fps=24)

                        st.video(tiktok_filename)

                        os.remove(tts_path)
                    os.remove(audio_path)
                    st.success("Vidéos TikTok générées avec succès !")

    except Exception as e:
        st.error(f"Erreur : {str(e)}")
