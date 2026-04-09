import streamlit as st
import google.generativeai as genai

# Configuration de base
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")

# Clé API Google Gemini
API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Gestion du Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Interaction
if prompt := st.chat_input("Posez votre question technique..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans la base technique..."):
            try:
                # On demande explicitement des réponses techniques détaillées
                context = "Tu es un technicien expert en imprimantes. Réponds précisément à : "
                response = model.generate_content(context + prompt)
                full_res = response.text
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error("Erreur de connexion à l'IA. Vérifiez votre clé API.")

# --- FORMULAIRE DE PANNE ---
st.write("---")
with st.expander("🚨 Signaler une panne matériel grave"):
    with st.form("panne_form"):
        sn = st.text_input("Numéro de Série")
        details = st.text_area("Description du problème")
        if st.form_submit_button("Envoyer Ticket"):
            if sn and details:
                st.success(f"Ticket enregistré pour le S/N {sn}.")
            else:
                st.warning("Veuillez remplir les champs.")
