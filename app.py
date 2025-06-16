import os
import tempfile
import streamlit as st
import pandas as pd

from rag.langchain import answer_question, delete_file_from_store, store_pdf_file
from feedback_db import init_db, save_feedback  # ✅ Import des fonctions feedback

# Initialisation de la base de données
init_db()

# Configuration de la page
st.set_page_config(page_title="Analyse de documents", page_icon="👋")

# Initialisation des états de session
if 'stored_files' not in st.session_state:
    st.session_state['stored_files'] = []

if 'last_response' not in st.session_state:
    st.session_state['last_response'] = ""

if 'last_question' not in st.session_state:
    st.session_state['last_question'] = ""

if 'last_lang' not in st.session_state:
    st.session_state['last_lang'] = "fr"

if 'last_feedback' not in st.session_state:
    st.session_state['last_feedback'] = None

def get_framework_functions(framework):
    if framework == "LangChain":
        from rag.langchain import answer_question, delete_file_from_store, store_pdf_file
        return answer_question, delete_file_from_store, store_pdf_file
    elif framework == "LlamaIndex":
        from rag.llamaindex import answer_question, delete_file_from_store, store_pdf_file
        return answer_question, delete_file_from_store, store_pdf_file
    else:
        raise ValueError("Framework inconnu")

def main():
    st.title("Analyse de documents")
    st.subheader("Analysez vos documents avec une IA en les chargeant dans l'application. Puis posez toutes vos questions.")
    
    # Choix du framework d'indexation
    framework_choice = st.radio(
        "Choisissez le framework d'indexation :",
        ["LangChain", "LlamaIndex"],
        horizontal=True
    )

    if "current_framework" not in st.session_state:
        st.session_state["current_framework"] = framework_choice
    if framework_choice != st.session_state["current_framework"]:
        st.warning(f"Changement de framework détecté ({st.session_state['current_framework']} → {framework_choice}). Les documents devront être réindexés.")
        st.session_state['stored_files'] = []
        st.session_state["current_framework"] = framework_choice

    answer_question, delete_file_from_store, store_pdf_file = get_framework_functions(framework_choice)

    # Téléversement de fichiers
    uploaded_files = st.file_uploader(
        label="Déposez vos fichiers ici ou chargez-les",
        type=None,
        accept_multiple_files=True
    )

    # Affichage des fichiers
    file_info = []
    if uploaded_files:
        for f in uploaded_files:
            size_in_kb = len(f.getvalue()) / 1024
            file_info.append({
                "Nom du fichier": f.name,
                "Taille (KB)": f"{size_in_kb:.2f}"
            })

            if f.name.endswith('.pdf') and f.name not in st.session_state['stored_files']:
                temp_dir = tempfile.mkdtemp()
                path = os.path.join(temp_dir, "temp.pdf")
                with open(path, "wb") as outfile:
                    outfile.write(f.read())
                store_pdf_file(path, f.name)
                st.session_state['stored_files'].append(f.name)

        df = pd.DataFrame(file_info)
        st.table(df)

    # Suppression de fichiers non présents
    files_to_be_deleted = set(st.session_state['stored_files']) - {f['Nom du fichier'] for f in file_info}
    for name in files_to_be_deleted:
        st.session_state['stored_files'].remove(name)
        delete_file_from_store(name)

    # Choix de langue
    lang_choice = st.selectbox(
        "Langue de la réponse souhaitée :",
        ["Français", "Anglais", "Espagnol", "Arabe"]
    )
    lang_map = {
        "Français": "fr",
        "Anglais": "en",
        "Espagnol": "es",
        "Arabe": "ar"
    }
    lang_code = lang_map[lang_choice]

    # Slider pour le nombre de documents contextuels
    k = st.slider("Nombre de documents contextuels à utiliser", min_value=1, max_value=20, value=5)

    # Entrée de la question
    question = st.text_input("Votre question ici")

    # Traitement de la question
    if st.button("Analyser") and question:
        model_response = answer_question(question, lang=lang_code, k=k)
        st.session_state["last_response"] = model_response
        st.session_state["last_question"] = question
        st.session_state["last_lang"] = lang_code
        st.session_state["last_feedback"] = None

    # Affichage de la réponse
    st.text_area("Zone de texte, réponse du modèle", value=st.session_state["last_response"], height=200)

    # Feedback utilisateur
    if st.session_state["last_response"]:
        try:
            feedback = st.feedback("faces")
        except:
            feedback = st.radio(
                "Que pensez-vous de cette réponse ?",
                ["😠 Très insatisfait", "😕 Insatisfait", "😐 Moyen", "🙂 Satisfait", "😃 Très satisfait"],
                key="feedback_faces"
            )

        if feedback and feedback != st.session_state["last_feedback"]:
            st.session_state["last_feedback"] = feedback

            # Sauvegarde du feedback
            save_feedback(
                question=st.session_state["last_question"],
                response=st.session_state["last_response"],
                feedback=feedback,
                lang=st.session_state["last_lang"]
            )
            st.success("✅ Feedback enregistré, merci !")

if __name__ == "__main__":
    main()
