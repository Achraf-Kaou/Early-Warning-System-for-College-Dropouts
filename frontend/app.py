import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_URL = "http://127.0.0.1:8000"  # Adapter si l'API tourne ailleurs

st.set_page_config(
    page_title="Alerte Décrochage Universitaire",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Alerte précoce du décrochage universitaire")
st.markdown(
    "Saisissez les informations d'un étudiant pour estimer son **niveau de risque de décrochage**.  \n"
    "Les résultats sont **indicatifs** et ne constituent pas une décision automatique."
)

# ---------------------------------------------------------------------------
# Sidebar – paramètres API
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("URL de l'API", value=API_URL)
    st.caption("L'API FastAPI doit être démarrée (uvicorn).")

    if st.button("Vérifier la connexion API"):
        try:
            r = requests.get(f"{api_url}/health", timeout=5)
            data = r.json()
            if data.get("model_loaded"):
                st.success("API connectée – modèle chargé ✓")
            else:
                st.error(f"Modèle non chargé : {data.get('error')}")
        except Exception as e:
            st.error(f"Impossible de joindre l'API : {e}")

# ---------------------------------------------------------------------------
# Formulaire principal
# ---------------------------------------------------------------------------
st.header("📋 Données de l'étudiant")

with st.form("student_form"):
    col1, col2, col3 = st.columns(3)

    # --- Colonne 1 : Infos générales ---
    with col1:
        st.subheader("Infos générales")
        age_at_enrollment = st.number_input("Âge à l'inscription", min_value=15, max_value=80, value=20)
        gender = st.selectbox("Genre", options=[(0, "Femme"), (1, "Homme")], format_func=lambda x: x[1])[0]
        marital_status = st.number_input("Statut marital (code)", min_value=1, value=1)
        nationality_placeholder = st.caption("Nationalité non utilisée par le modèle")

        st.subheader("Admission")
        application_mode = st.number_input("Mode de candidature (code)", min_value=1, value=17)
        application_order = st.number_input("Ordre de candidature", min_value=0, max_value=9, value=1)
        course = st.number_input("Filière / Course (code)", min_value=1, value=9254)
        daytime_evening_attendance = st.selectbox(
            "Cours de jour / soir",
            options=[(1, "Jour"), (0, "Soir")],
            format_func=lambda x: x[1],
        )[0]
        previous_qualification = st.number_input("Qualification antérieure (code)", min_value=1, value=1)
        previous_qualification_grade = st.number_input("Note qualification antérieure", value=130.0, step=0.1)
        admission_grade = st.number_input("Note d'admission", value=125.0, step=0.1)

    # --- Colonne 2 : Situation & famille ---
    with col2:
        st.subheader("Situation")
        displaced = st.selectbox("Étudiant déplacé", options=[(0, "Non"), (1, "Oui")], format_func=lambda x: x[1])[0]
        debtor = st.selectbox("Débiteur", options=[(0, "Non"), (1, "Oui")], format_func=lambda x: x[1])[0]
        tuition_fees_up_to_date = st.selectbox(
            "Frais de scolarité à jour",
            options=[(1, "Oui"), (0, "Non")],
            format_func=lambda x: x[1],
        )[0]
        scholarship_holder = st.selectbox(
            "Bénéficiaire d'une bourse",
            options=[(0, "Non"), (1, "Oui")],
            format_func=lambda x: x[1],
        )[0]

        st.subheader("Parents")
        mother_qualification = st.number_input("Qualification mère (code)", min_value=1, value=19)
        father_qualification = st.number_input("Qualification père (code)", min_value=1, value=12)
        mother_occupation = st.number_input("Profession mère (code)", min_value=0, value=5)
        father_occupation = st.number_input("Profession père (code)", min_value=0, value=9)

    # --- Colonne 3 : Performance académique ---
    with col3:
        st.subheader("1er semestre")
        cu_1st_enrolled = st.number_input("Unités inscrites (1er)", min_value=0, value=6)
        cu_1st_approved = st.number_input("Unités validées (1er)", min_value=0, value=6)
        cu_1st_grade = st.number_input("Note moyenne (1er)", min_value=0.0, value=13.5, step=0.1)
        cu_1st_evaluations = st.number_input("Évaluations (1er)", min_value=0, value=6)
        cu_1st_credited = st.number_input("Unités créditées (1er)", min_value=0, value=0)
        cu_1st_without_evaluations = st.number_input("Sans évaluation (1er)", min_value=0, value=0)

        st.subheader("2e semestre")
        cu_2nd_enrolled = st.number_input("Unités inscrites (2e)", min_value=0, value=6)
        cu_2nd_approved = st.number_input("Unités validées (2e)", min_value=0, value=5)
        cu_2nd_grade = st.number_input("Note moyenne (2e)", min_value=0.0, value=12.8, step=0.1)
        cu_2nd_evaluations = st.number_input("Évaluations (2e)", min_value=0, value=6)
        cu_2nd_credited = st.number_input("Unités créditées (2e)", min_value=0, value=0)
        cu_2nd_without_evaluations = st.number_input("Sans évaluation (2e)", min_value=0, value=0)

    submitted = st.form_submit_button("🔍 Estimer le risque de décrochage", use_container_width=True)

# ---------------------------------------------------------------------------
# Appel API + affichage du résultat
# ---------------------------------------------------------------------------
if submitted:
    payload = {
        "marital_status": int(marital_status),
        "application_mode": int(application_mode),
        "application_order": int(application_order),
        "course": int(course),
        "daytime_evening_attendance": int(daytime_evening_attendance),
        "previous_qualification": int(previous_qualification),
        "mother_qualification": int(mother_qualification),
        "father_qualification": int(father_qualification),
        "mother_occupation": int(mother_occupation),
        "father_occupation": int(father_occupation),
        "displaced": int(displaced),
        "debtor": int(debtor),
        "tuition_fees_up_to_date": int(tuition_fees_up_to_date),
        "gender": int(gender),
        "scholarship_holder": int(scholarship_holder),
        "age_at_enrollment": int(age_at_enrollment),
        "admission_grade": float(admission_grade),
        "previous_qualification_grade": float(previous_qualification_grade),
        "cu_1st_credited": int(cu_1st_credited),
        "cu_1st_enrolled": int(cu_1st_enrolled),
        "cu_1st_evaluations": int(cu_1st_evaluations),
        "cu_1st_approved": int(cu_1st_approved),
        "cu_1st_grade": float(cu_1st_grade),
        "cu_1st_without_evaluations": int(cu_1st_without_evaluations),
        "cu_2nd_credited": int(cu_2nd_credited),
        "cu_2nd_enrolled": int(cu_2nd_enrolled),
        "cu_2nd_evaluations": int(cu_2nd_evaluations),
        "cu_2nd_approved": int(cu_2nd_approved),
        "cu_2nd_grade": float(cu_2nd_grade),
        "cu_2nd_without_evaluations": int(cu_2nd_without_evaluations),
    }

    with st.spinner("Analyse en cours..."):
        try:
            response = requests.post(f"{api_url}/predict", json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Impossible de contacter l'API. "
                "Vérifiez qu'elle est bien lancée : `uvicorn app.main:app --reload --port 8000`"
            )
            st.stop()
        except Exception as e:
            st.error(f"❌ Erreur lors de la prédiction : {e}")
            st.stop()

    # Affichage du résultat
    st.divider()
    st.header("📊 Résultat de l'analyse")

    risk = result.get("risk_level", "unknown")
    proba = result.get("probability", 0)
    message = result.get("message", "")
    prediction = result.get("prediction", 0)

    # Couleurs selon le niveau
    if risk == "low":
        color = "#2ecc71"
        emoji = "🟢"
        label = "RISQUE FAIBLE"
    elif risk == "medium":
        color = "#f39c12"
        emoji = "🟠"
        label = "RISQUE MODÉRÉ"
    else:
        color = "#e74c3c"
        emoji = "🔴"
        label = "RISQUE ÉLEVÉ"

    st.markdown(
        f"""
        <div style="
            background-color: {color}22;
            border-left: 6px solid {color};
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <h2 style="margin:0; color:{color};">{emoji} {label}</h2>
            <p style="font-size:1.3rem; margin:0.4rem 0 0 0;">
                Probabilité de décrochage : <strong>{proba*100:.1f} %</strong>
            </p>
            <p style="margin:0.5rem 0 0 0; color:#333;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Barre de progression
    st.progress(min(max(proba, 0.0), 1.0))

    # Détails techniques
    with st.expander("Détails techniques"):
        st.json(result)
        st.caption(
            "prediction = 1 signifie que le modèle classe l'étudiant comme à risque de décrochage."
        )

# ---------------------------------------------------------------------------
# Pied de page
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "Projet académique – Alerte précoce du décrochage universitaire. "
    "Les prédictions sont indicatives et ne remplacent pas le jugement pédagogique."
)
