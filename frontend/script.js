const API_BASE = "http://127.0.0.1:8000";

const form = document.getElementById("studentForm");
const btnPredict = document.getElementById("btnPredict");
const btnCheckApi = document.getElementById("btnCheckApi");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const resultCard = document.getElementById("resultCard");
const errorCard = document.getElementById("errorCard");
const resultBadge = document.getElementById("resultBadge");
const progressBar = document.getElementById("progressBar");
const resultMessage = document.getElementById("resultMessage");
const resultJson = document.getElementById("resultJson");
const errorText = document.getElementById("errorText");

// ------------------------------------------------------------
// Helpers
// ------------------------------------------------------------
function hide(el) {
  el.classList.add("hidden");
}

function show(el) {
  el.classList.remove("hidden");
}

function setStatus(ok, message) {
  statusDot.className = "dot " + (ok === null ? "unknown" : ok ? "ok" : "error");
  statusText.textContent = message;
}

function formToPayload(formElement) {
  const data = new FormData(formElement);
  const payload = {};

  for (const [key, value] of data.entries()) {
    // Conversion numérique
    if (value === "" || value === null) {
      payload[key] = 0;
    } else if (!Number.isNaN(Number(value)) && value.trim() !== "") {
      payload[key] = Number(value);
    } else {
      payload[key] = value;
    }
  }

  return payload;
}

function renderResult(result) {
  hide(errorCard);
  show(resultCard);

  const risk = result.risk_level || "high";
  const proba = typeof result.probability === "number" ? result.probability : 0;
  const pct = Math.round(proba * 1000) / 10;

  const labels = {
    low: "🟢 RISQUE FAIBLE",
    medium: "🟠 RISQUE MODÉRÉ",
    high: "🔴 RISQUE ÉLEVÉ",
  };

  resultBadge.className = "result-badge " + risk;
  resultBadge.textContent = `${labels[risk] || labels.high} — ${pct} %`;

  progressBar.className = "progress-bar " + risk;
  progressBar.style.width = Math.min(Math.max(proba, 0), 1) * 100 + "%";

  resultMessage.textContent = result.message || "";
  resultJson.textContent = JSON.stringify(result, null, 2);

  resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderError(message) {
  hide(resultCard);
  show(errorCard);
  errorText.textContent = message;
}

// ------------------------------------------------------------
// API calls
// ------------------------------------------------------------
async function checkApi() {
  setStatus(null, "Vérification de l'API…");
  try {
    const res = await fetch(`${API_BASE}/health`, { method: "GET" });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();
    if (data.model_loaded) {
      setStatus(true, "API connectée – modèle chargé ✓");
    } else {
      setStatus(false, `API joignable mais modèle non chargé : ${data.error || "erreur inconnue"}`);
    }
  } catch (err) {
    setStatus(
      false,
      "Impossible de joindre l'API. Lancez : uvicorn app.main:app --reload --port 8000"
    );
  }
}

async function predict(payload) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    let detail = `Erreur HTTP ${res.status}`;
    try {
      const errBody = await res.json();
      detail = errBody.detail || JSON.stringify(errBody);
    } catch (_) {}
    throw new Error(detail);
  }

  return res.json();
}

// ------------------------------------------------------------
// Events
// ------------------------------------------------------------
btnCheckApi.addEventListener("click", checkApi);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hide(errorCard);
  hide(resultCard);

  btnPredict.disabled = true;
  btnPredict.textContent = "Analyse en cours…";

  try {
    const payload = formToPayload(form);
    const result = await predict(payload);
    renderResult(result);
  } catch (err) {
    renderError(
      err.message ||
        "Erreur lors de la prédiction. Vérifiez que l'API est démarrée et que le modèle est chargé."
    );
  } finally {
    btnPredict.disabled = false;
    btnPredict.textContent = "Estimer le risque de décrochage";
  }
});

// Vérification au chargement de la page
checkApi();
