import streamlit as st
from huggingface_hub import InferenceClient

# Configuration de la page
st.set_page_config(page_title="Support Assistant MFP", page_icon="🖨️")

st.title("🤖 Assistant Technique MFP")
st.markdown("Réparation, Toner et Maintenance")

# --- CONNEXION GRATUITE ---
# Remplacez par votre token Hugging Face (ou mettez-le dans les Secrets Streamlit)
hf_token = "VOTRE_TOKEN_HUGGING_FACE" 
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token=hf_token)

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Ex: Comment changer le toner ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logique de réponse de l'IA
    with st.chat_message("assistant"):
        # Instruction système pour guider l'IA
        system_instructions = (
            "Tu es un expert en maintenance d'imprimantes MFP. "
            "Aide l'utilisateur pour les pannes, le toner et les pièces. "
            "Si la panne est trop grave, conseille d'ouvrir un ticket hotline."
        )
        
        # Appel du modèle gratuit
        response = client.chat_completion(
            messages=[{"role": "system", "content": system_instructions},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            stream=False
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
