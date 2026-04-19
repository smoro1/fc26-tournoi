import streamlit as st
import pandas as pd

# Configuration mobile
st.set_page_config(page_title="FC 26 Tournoi", page_icon="⚽")

# Design sombre et stylé
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #00ff41; color: black; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 FC 26 : Championnat")

# Mémoire de l'app
if 'players' not in st.session_state: st.session_state.players = []
if 'matches' not in st.session_state: st.session_state.matches = []

# --- 1. INSCRIPTION ---
with st.expander("➕ Ajouter des joueurs", expanded=True):
    name = st.text_input("Nom du pote")
    if st.button("Ajouter à la liste"):
        if name and name not in st.session_state.players:
            st.session_state.players.append(name)
            st.rerun()
    st.write(f"Inscrits : {', '.join(st.session_state.players)}")
    if st.button("Tout effacer / Nouveau tournoi"):
        st.session_state.players = []
        st.session_state.matches = []
        st.rerun()

# --- 2. MATCHS & CLASSEMENT ---
if len(st.session_state.players) >= 2:
    st.divider()
    st.subheader("📝 Enregistrer un match")
    c1, c2 = st.columns(2)
    j1 = c1.selectbox("Joueur 1", st.session_state.players)
    s1 = c1.number_input("Score J1", min_value=0, step=1)
    j2 = c2.selectbox("Joueur 2", st.session_state.players, index=1 if len(st.session_state.players)>1 else 0)
    s2 = c2.number_input("Score J2", min_value=0, step=1)
    
    if st.button("Enregistrer le score"):
        st.session_state.matches.append({"j1": j1, "s1": s1, "j2": j2, "s2": s2})
        st.success("Score enregistré !")

    # Calcul du classement
    results = []
    for p in st.session_state.players:
        mj, pts, bp, bc = 0, 0, 0, 0
        for m in st.session_state.matches:
            if m['j1'] == p or m['j2'] == p:
                mj += 1
                if m['j1'] == p:
                    bp += m['s1']; bc += m['s2']
                    if m['s1'] > m['s2']: pts += 3
                    elif m['s1'] == m['s2']: pts += 1
                else:
                    bp += m['s2']; bc += m['s1']
                    if m['s2'] > m['s1']: pts += 3
                    elif m['s2'] == m['s1']: pts += 1
        results.append({"Joueur": p, "Pts": pts, "MJ": mj, "Diff": bp-bc})
    
    df = pd.DataFrame(results).sort_values(by=["Pts", "Diff"], ascending=False)
    st.subheader("📊 Classement")
    st.table(df)

# --- 3. PHASES FINALES ---
if len(st.session_state.players) >= 4:
    st.divider()
    st.subheader("🔥 Carré Final")
    top4 = df["Joueur"].tolist()[:4]
    st.info(f"Semi 1 : {top4[0]} vs {top4[3]}")
    st.info(f"Semi 2 : {top4[1]} vs {top4[2]}")
    st.success("🏆 FINALE : Vainqueurs des semis")
