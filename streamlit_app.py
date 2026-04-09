import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="Support Pro MFP", page_icon="🖨️")

st.title("🤖 Assistant Technique MFP")
st.markdown("Maintenance, Toner et Support Hardware")

# --- CONFIGURATION GROQ (GRATUIT & RAPIDE) ---
# Allez sur https://console.groq.com/ pour créer une clé gratuite si celle-ci expire
GROQ_API_KEY = "gsk_yH7M9v6VvX4X8v6VvX4X8v6VvX4X8v6VvX4X8v6VvX4X" # Exemple de format

# Initialisation du client Groq
# Note : Il est préférable de mettre votre clé dans les "Secrets" Streamlit plus tard
client = Groq(api_key="VOTRE_CLE_API_GROQ_ICI") 

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Ex: Code erreur SC542 sur Ricoh ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse technique en cours..."):
            try:
                # Prompt système pour forcer l'expertise technique
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Tu es un ingénieur support senior spécialisé en photocopieurs (MFP) marques Ricoh, Konica, HP, Canon. "
                                "Donne des instructions techniques précises : étapes de démontage, nettoyage de vitre, remplacement de toner. "
                                "Si le problème nécessite un tournevis ou une pièce complexe, demande à l'utilisateur d'ouvrir un ticket."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    model="llama3-8b-8192", # Modèle ultra performant
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Erreur de connexion. Veuillez vérifier votre clé API Groq.")

# --- FORMULAIRE DE TICKET (Toujours disponible en bas) ---
st.divider()
with st.expander("🆘 Ouvrir un ticket d'incident matériel"):
    with st.form("ticket"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Entreprise / Client")
            modele = st.text_input("Modèle de la machine")
        with col2:
            serie = st.text_input("Numéro de Série")
            contact = st.text_input("Téléphone / Email")
        
        description = st.text_area("Détails de la panne")
        if st.form_submit_button("Envoyer la demande d'intervention"):
            st.success("Ticket enregistré ! Notre hotline vous rappellera sous 2 heures.")
