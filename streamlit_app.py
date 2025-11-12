import streamlit as st
import random, string, time
from pathlib import Path

st.set_page_config(page_title="Wer hat die Bombe", page_icon="💣", layout="centered")

st.title("💣 Wer hat die Bombe 💣")
st.write("Drücke **Start**, dann erscheint ein zufälliges Wort. "
         "Nach etwa 30 Sekunden gibt’s ein **BUMM!** 🔥")

# Pfad zur Sounddatei
audio_path = Path("explosion.wav")

if not audio_path.exists():
    st.warning("⚠️ Die Datei 'explosion.wav' wurde nicht gefunden. "
               "Lege sie in denselben Ordner wie dieses Skript!")

# Status speichern
if "running" not in st.session_state:
    st.session_state.running = False

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    start = st.button("▶️ Start")
with col2:
    stop = st.button("⏹️ Stop")

# Platzhalter für Text und Timer
placeholder = st.empty()

def make_random_word():
    """Erzeugt ein zufälliges Wort aus Buchstaben."""
    length = random.randint(4, 8)
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

if start and not st.session_state.running:
    st.session_state.running = True
    word = make_random_word()

    with placeholder.container():
        st.markdown("### Zufallswort:")
        word_slot = st.empty()
        timer_slot = st.empty()

        for remaining in range(30, 0, -1):
            word_slot.markdown(f"**{word}**")
            timer_slot.markdown(f"⏳ Noch {remaining} Sekunden ...")
            time.sleep(1)

            if not st.session_state.running:
                break
        else:
            # Nach 30 Sekunden -> Explosion
            if audio_path.exists():
                st.audio(str(audio_path))
            st.markdown("<h1 style='color:red;'>💥 BUMM! 💥</h1>", unsafe_allow_html=True)
            st.markdown("<h2>WER HAT DIE BOMBE?</h2>", unsafe_allow_html=True)

    st.session_state.running = False

if stop:
    st.session_state.running = False
    placeholder.empty()

st.markdown("---")
st.caption("Ein einfaches Streamlit-Minispiel — keine Eingaben, keine Namen, nur Zufall und Spannung 💣")
