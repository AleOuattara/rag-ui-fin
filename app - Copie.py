import os
import tempfile

import streamlit as st
import pandas as pd

from rag.langchain import answer_question, delete_file_from_store, store_pdf_file

st.set_page_config(page_title="Analyse de documents", page_icon="👋")

if 'stored_files' not in st.session_state:
    st.session_state['stored_files'] = []

def main():
    st.title("Analyse de documents")
    st.subheader("Analysez vos documents avec une IA en les chargeant dans l'application. Puis posez toutes vos questions.")

    uploaded_files = st.file_uploader(
        label="Déposez vos fichiers ici ou chargez-les",
        type=None,
        accept_multiple_files=True
    )

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

    files_to_be_deleted = set(st.session_state['stored_files']) - {f['Nom du fichier'] for f in file_info}
    for name in files_to_be_deleted:
        st.session_state['stored_files'].remove(name)
        delete_file_from_store(name)

    # Choix de la langue de réponse
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

    question = st.text_input("Votre question ici")

    if st.button("Analyser"):
        model_response = answer_question(question, lang=lang_code)
        st.text_area("Zone de texte, réponse du modèle", value=model_response, height=200)
    else:
        st.text_area("Zone de texte, réponse du modèle", value="", height=200)

if __name__ == "__main__":
    main()
