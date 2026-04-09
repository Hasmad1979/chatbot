import streamlit as st
import requests
import time

# Configuration de l'interface
st.set_page_config(page_title="Expert MFP Pro", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.markdown("Maintenance, Codes Erreurs et Consommables")

# --- CONFIGURATION SÉCURISÉE ---
HF_TOKEN = "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"
# Modèle Mistral : Le plus performant pour le support technique en français
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def query_ai(user_input):
    # Prompt ultra-précis pour forcer une réponse d'expert
    payload = {
        "inputs": f"<s>[INST] Tu es un ingénieur support technique expert en imprimantes. Réponds de manière très détaillée et technique à cette question : {user_input} [/INST]",
        "parameters": {"max_new_tokens": 800, "temperature": 0.3}
    }
    
    # Boucle d'interactivité : On essaie jusqu'à ce que l'IA soit réveillée
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            output = response.json()
            
            # Cas 1 : Le modèle est en train de charger
            if isinstance(output, dict) and "estimated_time" in output:
                wait_time = int(output["estimated_time"])
                with st.status(f"🚀 Initialisation du cerveau technique ({wait_time}s)..."):
                    time.sleep(5) # On attend par tranches de 5 secondes
                continue
            
            # Cas 2 : Succès, on a une réponse technique
            if isinstance(output, list) and len(output) > 0:
                return output[0]['generated_text'].split("[/INST]")[-1].strip()
            
            # Cas 3 : Autre erreur
            return "Désolé, j'ai une difficulté technique. Pouvez-vous reformuler ?"
            
        except Exception:
            time.sleep(2)
            continue
            
    return "Le serveur technique met trop de temps à démarrer. Réessayez dans 30 secondes."

# Zone de Chat
if prompt := st.chat_input("Posez votre question technique (ex: Code SC542 Ricoh)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse du manuel technique..."):
            answer = query_ai(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# --- GARDE-FOU : SIGNALER UNE PANNE ---
st.write("---")
with st.exp
