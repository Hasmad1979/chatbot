import streamlit as st
import google.generativeai as genai

# Configuration
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")

# Clé API
GOOGLE_API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Historique
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Affichage des messages
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Entrée utilisateur
if prompt := st.chat_input("Posez votre question technique ici..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Réflexion technique..."):
            # Consigne simplifiée pour éviter les erreurs de syntaxe
            sys_msg = "Tu es un technicien expert en imprimantes. Donne des étapes claires : "
            response = st.session_state.chat.send_message(sys_msg + prompt)
            st.markdown(response.text)

# Formulaire de ticket
st.write("---")
with st.expander("🚨 Signaler une panne matériel"):
    with st.form("ticket_form"):
        sn = st.text_input("N° de Série")
        desc = st.text_area("Description du problème")
        if st.form_submit_button("Envoyer"):
            st.success("Ticket enregistré !")
