import streamlit as st
from huggingface_hub import InferenceClient

# Configuration de la page
st.set_page_config(page_title="Support Assistant MFP", page_icon="🖨️")

st.title("🤖 Assistant Technique MFP")
st.markdown("Réparation, Toner et Maintenance")

# --- CONNEXION AVEC VOTRE TOKEN ---
# Votre token est intégré ici pour l'authentification
HF_TOKEN = "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"

# Initialisation du client avec la nouvelle syntaxe recommandée
client = InferenceClient(api_key=HF_TOKEN)

# Initialisation de l'historique de discussion
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Ex: Comment changer le toner noir ?"):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse de l'IA
    with st.chat_message("assistant"):
        with st.spinner("L'assistant réfléchit..."):
            try:
                # Instructions pour définir le comportement du bot
                system_instructions = (
                    "Tu es un expert technique spécialisé dans les imprimantes multifonctions (MFP). "
                    "Ton but est d'aider les clients à résoudre des pannes techniques (bourrages, codes erreurs) "
                    "et de les guider pas à pas pour changer les toners ou consommables. "
                    "Sois poli, professionnel et clair. Si le problème semble être une panne matérielle grave "
                    "que l'utilisateur ne peut pas réparer seul, suggère-lui d'ouvrir un ticket à la hotline "
                    "pour demander l'intervention d'un technicien."
                )
                
                # Appel au modèle de langage (Zephyr est très performant et gratuit)
                stream = client.chat.completions.create(
