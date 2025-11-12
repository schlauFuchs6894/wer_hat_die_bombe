import streamlit as st
import random
import time

st.set_page_config(page_title="Wer hat die Bombe?", page_icon="💣")

st.title("💣 Wer hat die Bombe? — Heiße-Kartoffel-Spiel")

# --- Session State Defaults ---
if "phase" not in st.session_state:
    st.session_state.phase = "setup"
if "players" not in st.session_state:
    st.session_state.players = []
if "current_holder" not in st.session_state:
    st.session_state.current_holder = None
if "bomb_active" not in st.session_state:
    st.session_state.bomb_active = False
if "bomb_start" not in st.session_state:
    st.session_state.bomb_start = None
if "bomb_duration" not in st.session_state:
    st.session_state.bomb_duration = 30  # Sekunden
if "start_letter" not in st.session_state:
    st.session_state.start_letter = ""
if "exploded" not in st.session_state:
    st.session_state.exploded = False
if "loser" not in st.session_state:
    st.session_state.loser = None

# --- Phase 1: Spieler ---
if st.session_state.phase == "setup":
    st.subheader("Schritt 1 — Spieler eingeben")
    anzahl = st.number_input("Anzahl der Spieler", min_value=2, max_value=12, value=4, step=1)
    names = []
    cols = st.columns(2)
    for i in range(anzahl):
        col = cols[i % 2]
        name = col.text_input(f"Name Spieler {i+1}", key=f"name_{i}")
        names.append(name)

    if st.button("Spieler speichern und weiter"):
        if all(names):
            st.session_state.players = names
            st.session_state.current_holder = random.choice(st.session_state.players)
            st.session_state.phase = "config"
            st.rerun()
        else:
            st.warning("Bitte alle Spielernamen ausfüllen.")

# --- Phase 2: Einstellungen ---
elif st.session_state.phase == "config":
    st.subheader("Schritt 2 — Spiel konfigurieren")
    st.write("Gib einen Startbuchstaben und optional ein Beispielwort ein (z. B. `e` und `Erdbeere`).")
    st.session_state.start_letter = st.text_input("Startbuchstabe", value=st.session_state.start_letter, max_chars=1)
    beispielwort = st.text_input("Beispielwort (optional)")
    st.session_state.bomb_duration = st.number_input("Bombe zündet nach (Sekunden)", min_value=5, max_value=120, value=30, step=1)

    st.markdown(f"**Aktueller Starthalter:** {st.session_state.current_holder}")
    if st.button("Bombe starten"):
        if st.session_state.start_letter.strip() == "":
            st.warning("Bitte einen Startbuchstaben angeben.")
        else:
            st.session_state.bomb_active = True
            st.session_state.bomb_start = time.time()
            st.session_state.exploded = False
            st.session_state.loser = None
            st.session_state.phase = "playing"
            st.rerun()

    if st.button("Zurück — Spieler bearbeiten"):
        st.session_state.phase = "setup"
        st.rerun()

# --- Phase 3: Spiel läuft ---
elif st.session_state.phase == "playing":
    st.subheader("🔁 Spiel läuft — Bombe ist aktiv")
    players = st.session_state.players
    holder = st.session_state.current_holder
    duration = st.session_state.bomb_duration
    start = st.session_state.bomb_start

    now = time.time()
    remaining = max(0, int(duration - (now - start))) if start else duration

    st.markdown(f"**Startbuchstabe:** `{st.session_state.start_letter}`")
    st.markdown(f"**Derzeit hat die Bombe:** **{holder}**")
    st.progress(1 - remaining / duration if duration > 0 else 0)
    st.metric("Verbleibende Sekunden", f"{remaining}s")

    st.write("Während die Bombe läuft, kannst du sie an einen anderen Spieler weitergeben.")
    cols = st.columns((2, 1))
    with cols[0]:
        target = st.selectbox("Wähle, an wen du weitergeben willst", options=[p for p in players if p != holder])
    with cols[1]:
        if st.button("Weitergeben"):
            st.session_state.current_holder = target
            st.rerun()

    st.write("---")
    st.write("Tipp: Drücke `Aktualisieren`, um die Countdown-Anzeige zu aktualisieren.")
    if st.button("Aktualisieren"):
        st.rerun()

    if remaining <= 0 and not st.session_state.exploded:
        st.session_state.exploded = True
        st.session_state.bomb_active = False
        st.session_state.loser = st.session_state.current_holder
        st.rerun()

    if st.session_state.exploded:
        st.session_state.phase = "explosion"
        st.rerun()

# --- Phase 4: Explosion ---
elif st.session_state.phase == "explosion":
    st.subheader("💥 BUMM — Die Bombe ist explodiert!")
    loser = st.session_state.loser
    if loser:
        st.error(f"💣 Die Bombe ist bei **{loser}** explodiert — das Handy war in der Hand von **{loser}**!")
    else:
        st.error("Die Bombe ist explodiert — niemand konnte zugeordnet werden 😅.")

    st.write("Was soll passieren? (z. B. kleine Strafe oder Punktabzug)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nochmal mit gleicher Gruppe"):
            st.session_state.bomb_active = False
            st.session_state.bomb_start = None
            st.session_state.exploded = False
            st.session_state.loser = None
            st.session_state.current_holder = random.choice(st.session_state.players)
            st.session_state.phase = "config"
            st.rerun()
    with col2:
        if st.button("Neues Spiel (alles zurücksetzen)"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.write("---")
    st.write("Spielübersicht:")
    st.write(f"- Spieler: {', '.join(st.session_state.players)}")
    st.write(f"- Verlierer: {loser if loser else '—'}")
