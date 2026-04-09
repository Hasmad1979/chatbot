import streamlit as st
import requests
import time

# Configuration de la page
st.set_page_config(page_title="Support Assistant MFP", page_icon="🖨️")

st.title("🤖 Assistant Technique MFP")
st.markdown("Réparation, Toner et Maintenance")

# --- CONFIGURATION ---
HF_TOKEN = "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"
# Utilisation d'un modèle plus léger et plus rapide pour éviter les surcharges
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fonction de requête avec gestion de l'attente (Retry)
def query(payload):
    for i in range(5):  # On essaie 5 fois
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        # Si le modèle charge, il donne un temps estimé
        if isinstance(output, dict) and "estimated_time" in output:
            wait_time = output["estimated_time"]
            with st.status(f"L'IA se réveille (attente : {int(wait_time)}s)..."):
                time.sleep(min(wait_time, 10)) # On attend max 10s avant de réessayer
            continue
        return output
    return output

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Ex: Comment changer le toner ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Analyse technique en cours..."):
            system_prompt = f"<|system|>\nTu es un expert MFP. Guide l'utilisateur pour le toner ou les pannes. Si le problème est complexe, dis-lui d'ouvrir un ticket technique.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
            
            output = query({"inputs": system_prompt, "parameters": {"max_new_tokens": 500}})
            
            if isinstance(output, list) and len(output) > 0:
                full_response = output[0].get('generated_text', "Une erreur est survenue.")
            else:
                full_response = "Le serveur met trop de temps à répondre. Veuillez réessayer une dernière fois ou remplir un ticket ci-dessous."
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- SECTION TICKET HOTLINE ---
st.divider()
st.subheader("🆘 Besoin d'un technicien ?")
with st.expander("Cliquez ici pour ouvrir un ticket incident"):
    with st.form("ticket_form"):
        nom = st.text_input("Nom / Entreprise")
        serie = st.text_input("Numéro de série du MFP")
        panne = st.text_area("Description du problème")
        submit = st.form_submit_button("Envoyer à la Hotline")
        if submit:
            st.success(f"Ticket envoyé ! Un technicien vous contactera pour le MFP n°{serie}.")
