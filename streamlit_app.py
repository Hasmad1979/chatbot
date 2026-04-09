import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")

# Style CSS pour améliorer l'interface
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stForm { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Assistant Technique MFP")
st.caption("Maintenance, Codes Erreurs et Support Interactif")

# --- CONFIGURATION GOOGLE GEMINI ---
# Votre clé est maintenant intégrée ici
GOOGLE_API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialisation du modèle (Gemini 1.5 Flash est le plus rapide)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialisation de l'historique de discussion
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Affichage de l'historique
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Zone de saisie utilisateur
if prompt := st.chat_input("Ex: Comment résoudre l'erreur SC542 sur Ricoh ?"):
    # Affichage du message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Génération de la réponse technique
    with st.chat_message("assistant"):
        with st.spinner("Analyse technique en cours..."):
            try:
                # Consigne système envoyée à chaque message pour forcer l'expertise
                instruction = (
                    "Tu es un ingénieur support senior expert en photocopieurs (Ricoh, Konica, HP, Canon, Sharp). "
                    "Donne des réponses techniques très précises, étape par étape. "
                    "Utilise des listes à puces pour les procédures. "
                    "Si une manipulation est dangereuse (haute tension, chaleur), avertis l'utilisateur. "
                    "Question de l'utilisateur : "
