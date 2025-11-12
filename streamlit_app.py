import streamlit as st
import random, string, base64
from pathlib import Path

st.set_page_config(page_title="Wer hat die Bombe", page_icon="💣", layout="centered")

st.title("💣 Wer hat die Bombe 💣")
st.write("Drücke **Start**, ein Buchstabe erscheint, das Ticken beginnt... und irgendwann 💥")

# Pfad zur Sounddatei (die du erzeugt hast)
audio_path = Path("tic_tic_bumm_realistisch.wav")

if not audio_path.exists():
    st.error("⚠️ Die Datei 'tic_tic_bumm_realistisch.wav' fehlt! Lege sie in denselben Ordner wie dieses Skript.")
else:
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()

if "playing" not in st.session_state:
    st.session_state.playing = False

start = st.button("💥 Start")

if start:
    st.session_state.playing = True
    # Zufälliger Buchstabe
    letter = random.choice(string.ascii_uppercase)
    st.markdown(f"<h1 style='font-size:150px; text-align:center'>{letter}</h1>", unsafe_allow_html=True)

if st.session_state.playing and audio_path.exists():
    # Ton automatisch abspielen
    st.markdown(f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)
    st.session_state.playing = False

st.markdown("---")
st.caption("Zeigt einen zufälligen Buchstaben und spielt den 30-Sekunden-Ton (tic...tic...💥).")
