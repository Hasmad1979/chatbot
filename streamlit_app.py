import streamlit as st
import requests
import time

# 1. Configuration de l'interface
st.set_page_config(page_title="Support MFP Pro", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.markdown("Guides de réparation et maintenance en temps réel")

# 2. Configuration API (Votre Token est intégré)
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. Gestion de la mémoire du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Fonction pour obtenir une réponse technique
def get_technical_help(user_query):
    # Prompt forçant l'IA à être un expert
    prompt = f"<s>[INST] Tu es un technicien expert en imprimantes. Donne des instructions techniques étape par étape pour : {user_query} [/INST]"
    
    # On essaie de contacter le serveur plusieurs fois s'il "dort"
    for _ in range(5):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            result = response.json()
            
            if isinstance(result, dict) and "estimated_time" in result:
                time.sleep(5) # Attente si le modèle charge
                continue
                
            if isinstance(result, list):
                return result[0]['generated_text'].split("[/INST]")[-1].strip()
        except:
            continue
    return "Le serveur technique est occupé. Réessayez la question dans 10 secondes."

# 5. Zone de saisie interactive
if user_input := st.chat_input("Ex: Comment nettoyer le rouleau de transfert ?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyse technique en cours..."):
            ai_response = get_technical_help(user_input)
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 6. Formulaire de ticket (Sécurisé)
st.write("---")
with st.expander("🚨 Signaler une panne matériel (Besoin d'un technicien)"):
    with st.form("panne_form"):
        st.write("Remplissez ce formulaire si l'IA ne peut pas résoudre le problème.")
        sn = st.text_input("N° de Série du MFP")
        pb = st.text_area("Description de la panne")
        if st.form_submit_button("Envoyer à la Hotline"):
            if sn and pb:
                st.success(f"Ticket enregistré pour le S/N {sn}. Un technicien vous contactera.")
            else:
                st.error("Veuillez remplir tous les champs.")
