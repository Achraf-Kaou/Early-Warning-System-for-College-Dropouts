Interface Web – Alerte précoce du décrochage (Tâche 4.2)

Interface Streamlit connectée à l'API FastAPI.

Prérequis





L'API backend doit être démarrée :

cd backend
uvicorn app.main:app --reload --port 8000



Installer les dépendances de l'interface :

cd frontend
pip install -r requirements.txt

Lancement

cd frontend
streamlit run app.py

L'interface s'ouvre automatiquement dans le navigateur (généralement http://localhost:8501).

Utilisation





Vérifier la connexion API via le bouton dans la barre latérale



Remplir (ou modifier) les champs du formulaire



Cliquer sur Estimer le risque de décrochage



Consulter le niveau de risque (faible / modéré / élevé) et la probabilité

Structure

frontend/
├── app.py              # Application Streamlit
├── requirements.txt
└── README.md

