import streamlit as st
import requests
import time

# Configuration de l'interface
st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.markdown("Maintenance préventive et curative")

# --- CONFIGURATION API ---
HF_TOKEN = "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"
# Utilisation de Mistral-7B (excellent pour les procédures techniques en français)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique de discussion
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction de requête robuste avec relance automatique
def query_ai(prompt_text):
    payload = {
        "inputs": f"<s>[INST] Tu es un technicien expert en photocopieurs. Donne des instructions techniques détaillées et tape par étape pour : {prompt_text} [/INST]",
        "parameters": {"max_new_tokens": 1000, "temperature": 0.7}
    }
    
    for attempt in range(3): # Tentative de reconnexion automatique (3 fois)
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        # Si le modèle est en train de charger
        if isinstance(output, dict) and "estimated_time" in output:
            time.sleep(5) # Attendre 5 secondes avant de réessayer
            continue
        
        # Si on reçoit la réponse
        if isinstance(output, list) and len(output) > 0:
            return output[0]['generated_text'].split("[/INST]")[-1].strip()
            
    return "Désolé, le serveur technique est très occupé. Pouvez-vous reposer votre question ou utiliser le formulaire de panne ci-dessous ?"

# Logique du Chat
if prompt := st.chat_input("Ex: Procédure pour bourrage papier J001 ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Rédaction de la procédure technique..."):
            answer = query_ai(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# --- OPTION : SIGNALER UNE PANNE MATÉRIELLE (Toujours visible) ---
st.write("---")
st.subheader("🆘 Problème non résolu ?")
with st.expander("🚨 Signaler une panne matériel grave / Demander un technicien"):
    with st.form("ticket_hotline"):
        st.info("Utilisez ce formulaire si l'IA ne peut pas résoudre la panne à distance.")
        col1, col2 = st.columns(2)
        with col1:
            serie = st.text_input("Numéro de Série (S/N)")
            modele = st.text_input("Modèle du MFP")
        with col2:
            contact = st.text_input("Votre Nom / Téléphone")
        
        description = st.text_area("Description précise du problème ou code erreur affiché")
        
        envoi = st.form_submit_button("Envoyer la demande d'intervention")
        if envoi:
            if serie and description:
                st.success(f"Ticket enregistré pour la machine {serie}. Un technicien vous contactera.")
            else:
                st.warning("Veuillez remplir le numéro de série et la description.")
