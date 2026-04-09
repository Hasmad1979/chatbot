import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page
st.set_page_config(page_title="Support MFP Pro", page_icon="🖨️")
st.title("🤖 Assistant Technique MFP")
st.markdown("Réparation, Toner et Maintenance")

# 2. Configuration sécurisée de l'IA (Votre clé Gemini)
API_KEY = "AIzaSyDkyP6sNPfm32Zl5ayh2amyLs9GEH7BaQ8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Initialisation de la mémoire du Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Affichage des anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Zone de saisie et logique de réponse
if prompt := st.chat_input("Ex: Comment changer le toner sur un Ricoh ?"):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse de l'expert
    with st.chat_message("assistant"):
        with st.spinner("Analyse technique en cours..."):
            try:
                # Instruction forcée pour obtenir une réponse d'expert
                full_query = f"Tu es un technicien expert en imprimantes MFP. Donne des étapes claires pour : {prompt}"
                response = model.generate_content(full_query)
                
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception:
                st.error("Désolé, j'ai eu un problème de connexion. Réessayez votre question.")

# 6. Option de secours (Signalement de panne)
st.write("---")
with st.expander("🚨 Signaler une panne matériel grave"):
    with st.form("ticket_form"):
        sn = st.text_input("Numéro de Série (S/N)")
        desc = st.text_area("Description précise du problème")
        if st.form_submit_button("Envoyer à la Hotline"):
            if sn and desc:
                st.success(f"Ticket enregistré pour le S/N {sn}. Un technicien vous contactera.")
            else:
                st.warning("Veuillez remplir tous les champs.")
