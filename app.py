import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="FC 26 PRO Tournament", page_icon="🎮", layout="wide")

# Design "Dark Stadium"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #00ff41; color: black; border-radius: 20px; font-weight: bold; }
    .css-1r6slb0 { background-color: #1a1c24; border-radius: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ FC 26 - Tournament Manager")

# Utilisation du cache pour garder les données même si on rafraîchit (persistance locale)
if 'players' not in st.session_state:
    st.session_state.players = []
if 'history' not in st.session_state:
    st.session_state.history = []

# --- BARRE LATÉRALE : GESTION DES JOUEURS ---
with st.sidebar:
    st.header("👥 Joueurs du jour")
    new_p = st.text_input("Ajouter un joueur")
    if st.button("➕ Ajouter"):
        if new_p and new_p not in st.session_state.players:
            st.session_state.players.append(new_p)
            st.rerun()
    
    st.write("---")
    if st.button("🗑️ Reset le Tournoi"):
        st.session_state.players = []
        st.session_state.history = []
        st.rerun()

# --- SECTION PRINCIPALE ---
if not st.session_state.players:
    st.info("👋 Bienvenue ! Ajoutez les noms des joueurs dans la barre à gauche pour commencer.")
else:
    tab1, tab2, tab3 = st.tabs(["📊 Classement", "⚽ Saisir Score", "📜 Historique"])

    with tab1:
        st.subheader("Classement en temps réel")
        # Calcul automatique
        stats = []
        for p in st.session_state.players:
            mj, pts, bp, bc = 0, 0, 0, 0
            for m in st.session_state.history:
                if m['J1'] == p or m['J2'] == p:
                    mj += 1
                    if m['J1'] == p:
                        bp += m['S1']; bc += m['S2']
                        if m['S1'] > m['S2']: pts += 3
                        elif m['S1'] == m['S2']: pts += 1
                    else:
                        bp += m['S2']; bc += m['S1']
                        if m['S2'] > m['S1']: pts += 3
                        elif m['S2'] == m['S1']: pts += 1
            stats.append({"Joueur": p, "Pts": pts, "MJ": mj, "Diff": bp-bc, "Buts +": bp})
        
        df = pd.DataFrame(stats).sort_values(by=["Pts", "Diff", "Buts +"], ascending=False)
        st.table(df)

        # Qualification Auto
        if len(st.session_state.players) >= 4:
            st.divider()
            st.subheader("🔥 Phases Finales (Top 4)")
            top4 = df["Joueur"].tolist()[:4]
            col1, col2 = st.columns(2)
            col1.success(f"Demi 1 : {top4[0]} vs {top4[3]}")
            col2.success(f"Demi 2 : {top4[1]} vs {top4[2]}")

    with tab2:
        st.subheader("Enregistrer un match")
        c1, c2, c3, c4 = st.columns(4)
        j1 = c1.selectbox("Joueur 1", st.session_state.players, key="sel1")
        s1 = c2.number_input("Score J1", min_value=0, step=1, key="num1")
        s2 = c3.number_input("Score J2", min_value=0, step=1, key="num2")
        j2 = c4.selectbox("Joueur 2", st.session_state.players, key="sel2")

        if st.button("Valider le score"):
            if j1 == j2:
                st.error("Un joueur ne peut pas jouer contre lui-même !")
            else:
                st.session_state.history.insert(0, {"J1": j1, "S1": s1, "S2": s2, "J2": j2})
                st.balloons()
                st.rerun()

    with tab3:
        st.subheader("Derniers matchs joués")
        if st.session_state.history:
            for m in st.session_state.history:
                st.write(f"🏟️ **{m['J1']}** {m['S1']} - {m['S2']} **{m['J2']}**")
        else:
            st.write("Aucun match enregistré pour le moment.")
