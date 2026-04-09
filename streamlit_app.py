import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Support Assistant MFP", page_icon="🖨️")

st.title("🤖 Assistant Technique MFP")
st.markdown("Réparation, Toner et Maintenance")

# --- CONFIGURATION ---
# Votre token et l'URL du modèle (Zephyr est excellent pour le français)
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction pour appeler l'API proprement
# Remplacez votre fonction query actuelle par celle-ci
def query(payload):
    import time
    for i in range(3): # Il va essayer 3 fois
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        # Si le modèle est en train de charger, on attend et on recommence
        if isinstance(output, dict) and "estimated_time" in output:
            time.sleep(output["estimated_time"])
            continue
        return output
    return output

# Zone de saisie
if prompt := st.chat_input("Ex: Comment changer le toner ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche de la solution technique..."):
            # Préparation de la question pour l'IA
            system_prompt = f"<|system|>\nTu es un expert technique MFP. Aide pour les pannes, toners et pièces. Si c'est grave, propose un ticket hotline.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
            
            try:
                output = query({
                    "inputs": system_prompt,
                    "parameters": {"max_new_tokens": 500, "return_full_text": False}
                })
                
                # Extraction de la réponse
                if isinstance(output, list) and len(output) > 0:
                    full_response = output[0].get('generated_text', "Désolé, je ne peux pas répondre pour le moment.")
                else:
                    full_response = "Le service est temporairement surchargé, réessayez dans quelques secondes."
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                st.error("Erreur de connexion au cerveau de l'IA.")
