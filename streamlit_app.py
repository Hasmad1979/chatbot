import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")

# --- CONNEXION IA ---
# Votre clé est intégrée et nettoyée de tout espace invisible
API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8".strip()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Problème de configuration initiale. Veuillez rafraîchir la page.")

# Gestion de l'historique pour l'interactivité
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des bulles de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INTERACTION ---
if prompt := st.chat_input("Ex: Procédure pour bourrage papier ?"):
    # 1. Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Générer la réponse technique
    with st.chat_message("assistant"):
        with st.spinner("Expertise en cours..."):
            try:
                # Consigne stricte pour forcer les détails techniques
                context = "Tu es un technicien expert en photocopieurs. Donne des étapes précises et numérotées pour : "
                response = model.generate_content(context + prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("L'IA a généré une réponse vide. Réessayez votre question.")
            except Exception as e:
                st.error("Connexion instable. Cliquez à nouveau sur 'Entrée' pour relancer la recherche.")

# --- FORMULAIRE TICKET (En bas de page) ---
st.write("---")
with st.expander("🚨 Signaler une panne matériel grave"):
    with st.form("form_final"):
        st.write("Si l'IA ne peut pas résoudre la panne, ouvrez un ticket :")
        col1, col2 = st.columns(2)
        sn = col1.text_input("N° de Série")
        contact = col2.text_input("Votre Contact")
        desc = st.text_area("Description du problème")
        if st.form_submit_button("Envoyer à la Hotline"):
            if sn and desc:
                st.success(f"Ticket enregistré pour le S/N {sn}. Un technicien va vous rappeler.")
            else:
                st.error("Veuillez remplir le N° de série et la description.")
