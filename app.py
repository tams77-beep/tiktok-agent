import os
import requests
import uuid

# Ta clé API ElevenLabs ici (remplace par la tienne)
api_key = "sk_f053d1f1b76bc9987e47399c4a3355bd78936af2fd18fc0e"
os.environ["ELEVENLABS_API_KEY"] = api_key

# Ajoute ce code juste après la transcription (ex: `text = result['text']`)

if not text.strip():
    st.error("❌ Le texte est vide, la transcription a échoué.")
    st.stop()

with st.spinner("🔊 Génération de la voix (ElevenLabs)..."):
    VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (voix par défaut)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text[:500],  # max 500 caractères
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
        st.error(f"❌ Erreur API ElevenLabs : {response.status_code}\n{response.text}")
