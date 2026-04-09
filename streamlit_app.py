import streamlit as st
import requests
import time

st.set_page_config(page_title="Support MFP Expert", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")

# --- CONFIGURATION ---
HF_TOKEN = "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"
# On change pour un modèle plus petit (TinyLlama) qui est presque toujours prêt
API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if prompt := st.chat_input("Posez votre question technique ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Réponse technique en cours..."):
            # Format spécifique pour TinyLlama
            formatted_prompt = f"<|system|>\nTechnicien expert MFP.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
            
            output = query({"inputs": formatted_prompt})
            
            # Gestion de l'attente si le modèle charge
            if isinstance(output, dict) and "estimated_time" in output:
                st.info(f"Le cerveau de l'IA se prépare... (environ {int(output['estimated_time'])} sec). Réessayez dans un instant.")
                full_response = "Modèle en cours de chargement. Merci de patienter 30 secondes et de renvoyer votre message."
            else:
                try:
                    full_response = output[0]['generated_text'].split("<|assistant|>\n")[-1]
                except:
                    full_response = "Je suis prêt ! Reposez-moi votre question."

            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
