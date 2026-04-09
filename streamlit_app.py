import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")

# --- CONFIGURATION API ---
# Votre clé API Google Gemini
API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"

try:
    genai.configure(api_key=API_KEY)
    # Utilisation du modèle Flash pour la rapidité
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Erreur de configuration. Vérifiez votre clé API.")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INTERACTIF ---
if prompt := st.chat_input("Ex: Comment changer le toner ?"):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Expertise technique en cours..."):
            try:
                # Prompt simplifié pour éviter les erreurs de syntaxe
                full_prompt = f"Tu es un technicien expert en imprimantes. Réponds de façon précise à : {prompt}"
                response = model.generate_content(full_prompt)
                
                if response.text:
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("L'IA n'a pas pu répondre. Réessayez.")
            except Exception as e:
                st.error("La connexion a échoué. Veuillez renvoyer votre message.")

# --- FORMULAIRE DE TICKET (Toujours présent) ---
st.write("---")
with st.expander("🚨 Signaler une panne matériel (Ouvrir un ticket)"):
    with st.form("form_ticket"):
        sn = st.text_input("N° de Série du MFP")
        desc = st.text_area("Détails de la panne")
        if st.form_submit_button("Envoyer au support"):
            if sn and desc:
                st.success(f"Ticket enregistré pour le S/N {sn}.")
            else:
                st.warning("Veuillez remplir les champs.")
