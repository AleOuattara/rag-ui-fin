# 🧠 RAG-UI – Chatbot avec récupération augmentée et feedback utilisateur

Ce projet est un prototype de chatbot intelligent, capable de répondre à des questions en se basant sur des documents PDF chargés par l’utilisateur. Il est développé avec LangChain, llamaIndex, OpenAI, Streamlit et SQLite.

L’utilisateur peut interagir avec les documents, poser des questions, et fournir un feedback sur la qualité des réponses, qui est enregistré dans une base SQLite.




## 📂 Structure du projet

```text
rag-ui/
├── .git/                     # Dossier Git (créé après git init)
├── .gitignore               # Fichier pour ignorer certains fichiers dans Git
├── .streamlit/              # Configuration de l'application Streamlit
│   └── config.toml
├── app.py                   # Point d'entrée de l'application Streamlit
├── requirements.txt         # Dépendances Python
├── README.md                # Description du projet

├── rag/                     # Dossier principal pour la logique RAG
│   ├── __init__.py
│   ├── langchain.py         # Script principal avec logique utilisant LangChain
│   └── llamainindex.py      # Script alternatif utilisant LlamaIndex

├── secrets/                 # Clés et paramètres API Azure/OpenAI
│   └── config.yaml

├── notebooks/               # Notebooks Jupyter
│   ├── rag_langchain.ipynb
│   └── rag_llamaindex.ipynb

├── pages/                   # Pages supplémentaires Streamlit
│   └── exemple_page.py      # (optionnel)

├── samples/                 # Fichiers PDF d'exemple
│   └── demo.pdf

└── __pycache__/             # Cache Python (à ignorer)
```




## 🚀 Fonctionnalités

* 📥 Téléversement de documents PDF

* 🔍 Récupération augmentée via llamaiIndex ou LangChain + OpenAI 

* 💬 Interface interactive via Streamlit

* 📊 Historique et stockage des feedbacks utilisateurs dans une base SQLite

* 🧠 Métadonnées synthétiques générées pour les documents

* 🗃 Inspection de la base vectorielle interne (InMemory)




## 📌 Configuration

### 1. Cloner le projet

```bash
git clone https://github.com/ton_compte/rag-ui.git
cd rag-ui
```
### 2. Créer un environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate    # sur Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les clés API

```yaml
openai:
  api_key: ""

embedding:
  provider: "azure"
  azure_endpoint: "https://xxx.openai.azure.com"
  azure_deployment: "embedding-ada002"
  azure_api_version: "2023-05-15"
  azure_api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

chat:
  provider: "azure"
  azure_endpoint: "https://xxx.openai.azure.com"
  azure_deployment: "gpt35-chat"
  azure_api_version: "2023-05-15"
  azure_api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```




## ▶️ Lancer l'application

```bash
streamlit run app.py
```

Tu pourras :

* Charger un ou plusieurs fichiers PDF

* Poser des questions au chatbot 

* Visualiser la base vectorielle

* Donner une note à chaque réponse (stockée dans feedbacks.db)

## 🗃 Vérification de la base SQLite

Tu peux visualiser les feedbacks dans le fichier feedbacks.db :

Via Python 

```python
import sqlite3
conn = sqlite3.connect("feedbacks.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM feedbacks LIMIT 5;")
for row in cursor.fetchall():
    print(row)
conn.close()
```



## 📚 Technologies utilisées

- [LangChain](https://www.langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://platform.openai.com/) / [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [SQLite](https://www.sqlite.org/index.html)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)





## 📌 Auteur

Projet réalisé dans le cadre du module de la formation – Magistère Ingénieur Economiste - 3ème année
Aix-Marseille School of Economics — Promotion 2024–2025
Étudiant : 
- Alè OUATTARA
- Jean-Eude GBADA
- Bendounan ABDERREZZAK
