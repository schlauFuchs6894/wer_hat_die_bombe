import streamlit as st
import random, string, time
import base64
from pathlib import Path

st.set_page_config(page_title="Wer hat die Bombe", page_icon="💣", layout="centered")

st.title("💣 Wer hat die Bombe 💣")
st.write("Drücke **Start**, ein zufälliger Buchstabe erscheint... "
         "nach einiger Zeit passiert etwas 💥")

# Pfad zur Sounddatei
audio_path = Path("explosion.wav")

if not audio_path.exists():
    st.warning("⚠️ Die Datei 'explosion.wav' wurde nicht gefunden. "
               "Lege sie in denselben Ordner wie dieses Skript!")

if "running" not in st.session_state:
    st.session_state.running = False

# Start-Button
start = st.button("💥 Start")

# Platzhalter für Anzeige
placeholder = st.empty()

def random_letter():
    """Gibt einen zufälligen Buchstaben (A–Z) zurück."""
    return random.choice(string.ascii_uppercase)

if start and not st.session_state.running:
    st.session_state.running = True
    letter = random_letter()
    placeholder.markdown(f"<h1 style='font-size:150px; text-align:center'>{letter}</h1>", unsafe_allow_html=True)

    # Unsichtbarer Timer – einfach warten
    time.sleep(30)

    # Explosion abspielen automatisch (keine Play-Taste)
    if audio_path.exists():
        # Datei in base64 konvertieren, um sie automatisch im HTML-Audio-Tag abzuspielen
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    # Explosionstext anzeigen
    placeholder.markdown("<h1 style='color:red; text-align:center'>💥 BUMM! 💥</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center'>WER HAT DIE BOMBE?</h2>", unsafe_allow_html=True)

    st.session_state.running = False

st.markdown("---")
st.caption("Einfach. Zufällig. Laut. 💣 Keine Wörter, keine Listen – nur ein Buchstabe und das Schicksal.")
