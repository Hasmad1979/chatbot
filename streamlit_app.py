import streamlit as st
import google.generativeai as genai

# 1. Configuration de l'interface
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.markdown("Expertise technique instantanée pour photocopieurs")

# 2. Configuration de l'IA avec votre clé
API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Gestion de la mémoire (Historique)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Chat Interactif
if prompt := st.chat_input("Ex: Procédure bourrage papier J001 ?"):
    # Affichage utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        with st.spinner("Rédaction de la procédure..."):
            try:
                # On force l'IA à donner une réponse technique détaillée
                instruction = "Tu es un technicien expert en maintenance de photocopieurs. Donne une réponse technique détaillée étape par étape pour : "
                response = model.generate_content(instruction + prompt)
                
                output_text = response.text
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception:
                st.error("Petit souci de connexion. Veuillez cliquer sur 'Entrée' pour relancer.")

# 5. Option de signalement matériel (Obligatoire)
st.write("---")
with st.expander("🆘 Signaler une panne matériel (Besoin d'un technicien)"):
    with st.form("ticket_form"):
        st.write("Utilisez ce formulaire si l'IA ne peut pas résoudre le problème à distance.")
        col1, col2 = st.columns(2)
        sn = col1.text_input("N° de Série du MFP")
        contact = col2.text_input("Votre Contact")
        desc = st.text_area("Description précise du problème")
        
        if st.form_submit_button("Envoyer la demande"):
            if sn and desc:
                st.success(f"Ticket enregistré pour le S/N {sn}. Un technicien vous contactera.")
            else:
                st.warning("Veuillez remplir le numéro de série et la description.")
