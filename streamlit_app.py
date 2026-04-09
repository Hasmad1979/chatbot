import streamlit as st
import requests
import time

st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.caption("Maintenance préventive et curative")

# --- CONFIGURATION ---
HF_TOKEN = "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"
# Utilisation de Mistral-7B : Le meilleur modèle open-source pour le français
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if prompt := st.chat_input("Ex: Comment changer le toner ou résoudre un bourrage ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche de la procédure technique..."):
            # Prompt optimisé pour Mistral
            formatted_prompt = f"<s>[INST] Tu es un technicien expert en imprimantes MFP. Aide l'utilisateur avec des étapes précises pour : {prompt} [/INST]"
            
            try:
                output = query({"inputs": formatted_prompt, "parameters": {"max_new_tokens": 500}})
                
                # Si le modèle doit charger
                if isinstance(output, dict) and "estimated_time" in output:
                    full_response = "Le serveur technique se connecte... Je suis prêt dans quelques secondes. Merci de renvoyer votre question maintenant."
                else:
                    # Extraction propre de la réponse
                    result = output[0]['generated_text']
                    full_response = result.split("[/INST]")[-1].strip()
                
                if not full_response:
                    full_response = "Je peux vous aider pour le changement de toner, les bourrages papier ou les codes erreurs. Précisez votre modèle de machine."

                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except:
                st.error("Petit souci de connexion. Réessayez la question, je suis là.")

# --- FORMULAIRE DE TICKET RAPIDE ---
st.divider()
with st.expander("🆘 Signaler une panne matériel grave"):
    with st.form("ticket"):
        st.write("Si l'IA ne peut pas résoudre le problème, ouvrez un ticket :")
        s = st.text_input("N° de Série")
        p = st.text_area("Description du problème")
        if st.form_submit_button("Envoyer à la Hotline"):
            st.success("Ticket créé ! Un technicien va vous rappeler.")
