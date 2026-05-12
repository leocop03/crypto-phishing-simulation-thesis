import argparse
import csv
import hashlib
import json
import os
import random
from collections import Counter
from datetime import datetime

import requests


TRAIT_SCALE = [
    "molto_bassa",
    "bassa",
    "media",
    "alta",
    "molto_alta",
]

SECURITY_TRAINING_SCALE = [
    "no",
    "minima",
    "basilare",
    "autodidatta",
    "si",
]

BACKGROUND_VARIANTS = [
    "ha poco tempo e legge i messaggi rapidamente",
    "ha ricevuto da poco un avviso di sicurezza reale",
    "si affida spesso a notifiche e messaggi ricevuti sul telefono",
    "prima di agire tende a cercare conferme online",
    "usa spesso servizi crypto ma non controlla sempre i dettagli",
    "ha gia visto tentativi di phishing simili in passato",
    "sta gestendo molte attivita contemporaneamente",
    "ha bisogno di risolvere velocemente problemi legati agli account",
    "preferisce chiedere conferma a una persona piu esperta",
    "si fida molto dei messaggi che sembrano provenire da brand noti",
]

VARIANT_PROFILES = [
    {
        "impulsiveness": 1,
        "trust_in_brands": 1,
        "attention_level": -1,
        "risk_aversion": -1,
        "security_training": 0,
    },
    {
        "impulsiveness": -1,
        "trust_in_brands": -1,
        "attention_level": 1,
        "risk_aversion": 1,
        "security_training": 1,
    },
    {
        "impulsiveness": 0,
        "trust_in_brands": 1,
        "attention_level": 0,
        "risk_aversion": 0,
        "security_training": 0,
    },
    {
        "impulsiveness": 1,
        "trust_in_brands": 0,
        "attention_level": -1,
        "risk_aversion": 0,
        "security_training": -1,
    },
    {
        "impulsiveness": -1,
        "trust_in_brands": 0,
        "attention_level": 1,
        "risk_aversion": 0,
        "security_training": 0,
    },
    {
        "impulsiveness": 0,
        "trust_in_brands": -1,
        "attention_level": 0,
        "risk_aversion": 1,
        "security_training": 0,
    },
]

ALLOWED_DECISIONS = [
    "IGNORA",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA_COME_PHISHING",
    "PROCEDE_CON_LA_RICHIESTA",
    "RIMANDA_O_NON_DECIDE",
]

ALLOWED_SPECIFIC_ACTIONS = [
    "NESSUNA_AZIONE",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA_COME_PHISHING",
    "CLICCA_LINK_SENZA_INSERIRE_DATI",
    "INSERISCE_CREDENZIALI",
    "INSERISCE_DATI_KYC",
    "INSERISCE_SEED_PHRASE",
    "COLLEGA_WALLET",
    "APPROVA_TRANSAZIONE",
    "CONCEDE_ACCESSO_REMOTO",
    "INVIA_FONDI",
    "INSTALLA_APP_O_SOFTWARE",
    "COMPLETA_RESET_PASSWORD_LEGITTIMO",
    "LEGGE_GUIDA_SICUREZZA",
]

AUTO_ACTION_BY_DECISION = {
    "IGNORA": "NESSUNA_AZIONE",
    "RIMANDA_O_NON_DECIDE": "NESSUNA_AZIONE",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA_COME_PHISHING": "SEGNALA_COME_PHISHING",
}

DECISION_MAPPING = {
    "NESSUNA": "IGNORA",
    "NESSUNA_AZIONE": "IGNORA",
    "NESSUNA_AZIONE_ULTERIORE": "IGNORA",
    "NON_FA_NULLA": "IGNORA",
    "IGNORA_IL_MESSAGGIO": "IGNORA",
    "VERIFICA": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "VERIFICA_SUBITO": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "CONTROLLA_TRAMITE_CANALE_UFFICIALE": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA": "SEGNALA_COME_PHISHING",
    "SEGNALA_SUBITO": "SEGNALA_COME_PHISHING",
    "MARCA_COME_PHISHING": "SEGNALA_COME_PHISHING",
    "PROCEDE": "PROCEDE_CON_LA_RICHIESTA",
    "SEGUE_LA_RICHIESTA": "PROCEDE_CON_LA_RICHIESTA",
    "ESEGUE_LA_RICHIESTA": "PROCEDE_CON_LA_RICHIESTA",
    "RIMANDA": "RIMANDA_O_NON_DECIDE",
    "NON_DECIDE": "RIMANDA_O_NON_DECIDE",
    "RIMANDA_LA_DECISIONE": "RIMANDA_O_NON_DECIDE",
    "CI_PENSA": "RIMANDA_O_NON_DECIDE",
}

SPECIFIC_ACTION_MAPPING = {
    "NESSUNA": "NESSUNA_AZIONE",
    "NESSUNA_AZIONE_ULTERIORE": "NESSUNA_AZIONE",
    "NON_FA_NULLA": "NESSUNA_AZIONE",
    "VERIFICA": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "VERIFICA_SUBITO": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA": "SEGNALA_COME_PHISHING",
    "SEGNALA_SUBITO": "SEGNALA_COME_PHISHING",
    "CLICCA_LINK": "CLICCA_LINK_SENZA_INSERIRE_DATI",
    "CLICCA_SUL_LINK": "CLICCA_LINK_SENZA_INSERIRE_DATI",
    "CLICK_SUL_LINK": "CLICCA_LINK_SENZA_INSERIRE_DATI",
    "CLICKA_SUL_LINK": "CLICCA_LINK_SENZA_INSERIRE_DATI",
    "INSERISCE_CREDENZIALI_O_SEED": "INSERISCE_CREDENZIALI",
    "INSERISCI_CREDENZIALI": "INSERISCE_CREDENZIALI",
    "FORNISCE_CREDENZIALI": "INSERISCE_CREDENZIALI",
    "INSERISCE_KYC": "INSERISCE_DATI_KYC",
    "FORNISCE_DATI_KYC": "INSERISCE_DATI_KYC",
    "INSERISCE_SEED": "INSERISCE_SEED_PHRASE",
    "FORNISCE_SEED": "INSERISCE_SEED_PHRASE",
    "FORNISCE_SEED_PHRASE": "INSERISCE_SEED_PHRASE",
    "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE": "COLLEGA_WALLET",
    "CONNETTE_WALLET": "COLLEGA_WALLET",
    "APPROVA": "APPROVA_TRANSAZIONE",
    "APPROVA_RICHIESTA": "APPROVA_TRANSAZIONE",
    "CONCEDE_CONTROLLO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "CONDIVIDE_SCHERMO": "CONCEDE_ACCESSO_REMOTO",
    "INSTALLA_SOFTWARE_ACCESSO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "SCARICA_APP": "INSTALLA_APP_O_SOFTWARE",
    "INSTALLA_APP": "INSTALLA_APP_O_SOFTWARE",
    "INSTALLA_SOFTWARE": "INSTALLA_APP_O_SOFTWARE",
    "RESET_PASSWORD": "COMPLETA_RESET_PASSWORD_LEGITTIMO",
    "COMPLETA_RESET_PASSWORD": "COMPLETA_RESET_PASSWORD_LEGITTIMO",
    "LEGGE_GUIDA": "LEGGE_GUIDA_SICUREZZA",
}

JSON_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ALLOWED_DECISIONS,
        },
        "specific_action": {
            "type": "string",
            "enum": ALLOWED_SPECIFIC_ACTIONS,
        },
        "motivation": {
            "type": "string",
        },
    },
    "required": ["decision", "specific_action", "motivation"],
}


# ------- CONFIGURAZIONE -------

OLLAMA_MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"

ARCHETYPES_PATH = os.path.join("agents", "profiles_archetypes.json")
MESSAGES_PATH = os.path.join("scenarios", "messages.json")

RESULTS_DIR = "results"
INSTANCES_PER_ARCHETYPE = 6  # 16 archetipi * 6 = 96 agenti
RANDOM_SEED = 42
TEMPERATURE = 0.3
REQUEST_TIMEOUT_SECONDS = 60


# ------- FUNZIONI DI CARICAMENTO -------

def make_interaction_seed(agent_id: str, message_id: str) -> int:
    key = f"{RANDOM_SEED}|{agent_id}|{message_id}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:8], 16)


def load_archetypes(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_messages(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def shift_ordered_value(value: str, scale: list[str], shift: int) -> str:
    if value not in scale:
        return value

    shift = min(max(shift, -1), 1)
    idx = scale.index(value)
    shifted_idx = min(max(idx + shift, 0), len(scale) - 1)
    return scale[shifted_idx]


def expand_profiles(archetypes, instances_per_archetype=INSTANCES_PER_ARCHETYPE):
    """
    Clona ogni archetipo in piu agenti con variazioni controllate.
    Python varia i profili, ma non decide le azioni comportamentali.
    """
    profiles = []

    for arch in archetypes:
        base_age = arch.get("age", 30)
        base_traits = arch.get("traits", {})
        if instances_per_archetype <= len(BACKGROUND_VARIANTS):
            background_variants = random.sample(BACKGROUND_VARIANTS, instances_per_archetype)
        else:
            background_variants = random.choices(BACKGROUND_VARIANTS, k=instances_per_archetype)

        for i in range(instances_per_archetype):
            profile = json.loads(json.dumps(arch))  # deep copy
            profile["id"] = f"{arch['id']}_{i + 1}"

            jitter = random.randint(-2, 2)
            profile["age"] = max(15, base_age + jitter)

            variant = VARIANT_PROFILES[i % len(VARIANT_PROFILES)]
            random_noise = {
                "impulsiveness": random.choice([-1, 0, 0, 1]),
                "trust_in_brands": random.choice([-1, 0, 0, 1]),
                "tech_savvy": random.choice([-1, 0, 0, 1]),
                "attention_level": random.choice([-1, 0, 0, 1]),
                "risk_aversion": random.choice([-1, 0, 0, 1]),
                "security_training": random.choice([-1, 0, 0, 0, 1]),
            }

            traits = profile.setdefault("traits", {})
            for trait_name in [
                "impulsiveness",
                "trust_in_brands",
                "tech_savvy",
                "attention_level",
                "risk_aversion",
            ]:
                shift = variant.get(trait_name, 0) + random_noise.get(trait_name, 0)
                traits[trait_name] = shift_ordered_value(
                    base_traits.get(trait_name, traits.get(trait_name)),
                    TRAIT_SCALE,
                    shift,
                )

            training_shift = variant.get("security_training", 0) + random_noise.get("security_training", 0)
            profile["security_training"] = shift_ordered_value(
                arch.get("security_training"),
                SECURITY_TRAINING_SCALE,
                training_shift,
            )

            profile["background"] = background_variants[i]
            profiles.append(profile)

    return profiles


# ------- PROMPT & CHIAMATA LLM -------

def normalize_model_label(value) -> str:
    normalized = str(value).strip().upper()
    for old, new in [
        (" ", "_"),
        ("-", "_"),
        ("/", "_"),
        (".", ""),
        (",", ""),
        (":", ""),
        (";", ""),
        ("(", ""),
        (")", ""),
        ("'", ""),
        ('"', ""),
    ]:
        normalized = normalized.replace(old, new)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized.strip("_")


def format_label_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def build_prompt(agent_profile: dict, message: dict) -> str:
    """
    Costruisce il prompt per un singolo agente e messaggio.
    Il messaggio e gia stato letto: la decisione simulata inizia dopo la lettura.
    """
    traits = agent_profile.get("traits", {})
    feats = message.get("features", {})
    allowed_proceed_actions = message.get("allowed_proceed_actions", [])

    return f"""
Sei un utente reale chiamato {agent_profile.get('id')}. Devi simulare il comportamento spontaneo di questa persona, non dare consigli di sicurezza.

L'utente ha gia ricevuto e letto il messaggio. La lettura del messaggio non e una scelta simulata.
Devi decidere cosa fa dopo averlo letto.

Profilo:
- Eta: {agent_profile.get('age')}
- Fascia d'eta: {agent_profile.get('age_group')}
- Ruolo: {agent_profile.get('role')}
- Esperienza con le criptovalute: {agent_profile.get('crypto_experience')}
- Formazione sulla sicurezza: {agent_profile.get('security_training')}
- Contesto d'uso: {agent_profile.get('environment')}
- Situazione personale del momento: {agent_profile.get('background')}
- Tratti: impulsivita={traits.get('impulsiveness')}, fiducia nei brand={traits.get('trust_in_brands')}, competenza tecnologica={traits.get('tech_savvy')}, livello di attenzione={traits.get('attention_level')}, avversione al rischio={traits.get('risk_aversion')}

Caratteristiche percepibili del messaggio:
- Urgenza: {feats.get('urgency')}
- Personalizzazione: {feats.get('personalization')}
- Ricompensa o danno evitato: {feats.get('reward')}

Messaggio ricevuto tramite {message.get('channel')}:
\"\"\"{message.get('text')}\"\"\"

L'utente NON conosce l'etichetta interna del messaggio e NON sa se sia legittimo o fraudolento.
Non comportarti sempre come un esperto di cybersecurity.
Non scegliere automaticamente la risposta piu sicura.
Devi impersonare il profilo: includi esitazioni, scorciatoie, fiducia, distrazione, fretta o prudenza quando sono coerenti con questa persona.

Decisioni possibili:
{format_label_list(ALLOWED_DECISIONS)}

Se decide di procedere, puo scegliere solo una di queste azioni specifiche compatibili con il messaggio:
{format_label_list(allowed_proceed_actions)}

Azioni automatiche:
- Se decision = IGNORA: specific_action = NESSUNA_AZIONE
- Se decision = RIMANDA_O_NON_DECIDE: specific_action = NESSUNA_AZIONE
- Se decision = VERIFICA_TRAMITE_CANALE_UFFICIALE: specific_action = VERIFICA_TRAMITE_CANALE_UFFICIALE
- Se decision = SEGNALA_COME_PHISHING: specific_action = SEGNALA_COME_PHISHING

Criteri comportamentali:
- Alta esperienza crypto non significa automaticamente prudenza.
- Bassa formazione di sicurezza non significa automaticamente ingenuita.
- Una persona impulsiva, sotto pressione o attratta da una ricompensa puo procedere.
- Una persona attenta, avversa al rischio o formata puo verificare o segnalare.
- Una persona occupata puo ignorare o rimandare.
- Non scegliere sempre verifica.
- Non scegliere sempre procedi.
- Non scegliere sempre ignora.
- Valuta profilo, contesto, canale, urgenza, personalizzazione e ricompensa.
- Non scegliere azioni incompatibili con questo scenario.

Rispondi solo in JSON valido con questo schema:
{{
  "decision": "UNA_DECISIONE_AMMESSA",
  "specific_action": "UNA_AZIONE_SPECIFICA_AMMESSA",
  "motivation": "frase breve"
}}
"""


def build_retry_prompt(original_prompt: str, message: dict, validation_error: str) -> str:
    allowed_proceed_actions = message.get("allowed_proceed_actions", [])
    return f"""
{original_prompt}

La risposta precedente non rispettava lo schema o conteneva un'azione incompatibile.
Errore di validazione: {validation_error}

Rispondi di nuovo solo con JSON valido.
Decisioni ammesse:
{format_label_list(ALLOWED_DECISIONS)}

Azioni globali ammesse:
{format_label_list(ALLOWED_SPECIFIC_ACTIONS)}

Se decision = PROCEDE_CON_LA_RICHIESTA, le sole azioni ammesse per questo scenario sono:
{format_label_list(allowed_proceed_actions)}

Non aggiungere testo fuori dal JSON.
"""


def build_ollama_payload(prompt: str, interaction_seed: int, response_format, include_think: bool) -> dict:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": response_format,
        "options": {
            "temperature": TEMPERATURE,
            "seed": interaction_seed,
        },
    }
    if include_think:
        payload["think"] = False
    return payload


def post_ollama(prompt: str, interaction_seed: int) -> str:
    """
    Prova JSON schema + think=False, poi degrada in modo pulito per versioni
    di Ollama che non supportano uno dei due parametri.
    """
    attempts = [
        (JSON_RESPONSE_SCHEMA, True),
        (JSON_RESPONSE_SCHEMA, False),
        ("json", False),
    ]
    last_error = None

    for response_format, include_think in attempts:
        try:
            response = requests.post(
                OLLAMA_URL,
                json=build_ollama_payload(prompt, interaction_seed, response_format, include_think),
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.HTTPError as exc:
            last_error = exc
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code in {400, 404, 415, 422}:
                continue
            raise

    raise RuntimeError(f"Chiamata Ollama non riuscita anche con fallback: {last_error}")


def extract_json_response(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("Nessun JSON trovato nella risposta del modello")
    return json.loads(text[start:end + 1])


def build_parse_error_response(raw_response: str, validation_error: str, motivation: str = "") -> dict:
    return {
        "raw_decision": "",
        "decision": "PARSE_ERROR",
        "raw_specific_action": "",
        "specific_action": "PARSE_ERROR",
        "raw_initial_reaction": "",
        "initial_reaction": "PARSE_ERROR",
        "raw_final_action": "",
        "final_action": "PARSE_ERROR",
        "proceeded": False,
        "engaged": False,
        "compromised": False,
        "reported": False,
        "verified": False,
        "false_positive_report": False,
        "legitimate_completion": False,
        "parse_error": True,
        "validation_error": validation_error,
        "motivation": motivation,
        "raw_response": raw_response,
    }


def validate_model_response(parsed: dict, message: dict, raw_response: str) -> dict:
    raw_decision = normalize_model_label(parsed.get("decision", parsed.get("initial_reaction", "")))
    raw_specific_action = normalize_model_label(parsed.get("specific_action", parsed.get("final_action", "")))
    motivation = str(parsed.get("motivation", "")).strip()

    decision = DECISION_MAPPING.get(raw_decision, raw_decision)
    specific_action = SPECIFIC_ACTION_MAPPING.get(raw_specific_action, raw_specific_action)

    if decision not in ALLOWED_DECISIONS:
        return build_parse_error_response(
            raw_response,
            f"Decisione non ammessa: {raw_decision}",
            motivation,
        )

    if specific_action not in ALLOWED_SPECIFIC_ACTIONS:
        return build_parse_error_response(
            raw_response,
            f"Azione specifica non ammessa: {raw_specific_action}",
            motivation,
        )

    if decision != "PROCEDE_CON_LA_RICHIESTA":
        specific_action = AUTO_ACTION_BY_DECISION[decision]
    else:
        allowed_proceed_actions = message.get("allowed_proceed_actions", [])
        if specific_action not in allowed_proceed_actions:
            return build_parse_error_response(
                raw_response,
                f"Azione non compatibile con lo scenario: {specific_action}",
                motivation,
            )

    message_type = message.get("type")
    proceeded = decision == "PROCEDE_CON_LA_RICHIESTA"
    reported = decision == "SEGNALA_COME_PHISHING" or specific_action == "SEGNALA_COME_PHISHING"
    verified = (
        decision == "VERIFICA_TRAMITE_CANALE_UFFICIALE"
        or specific_action == "VERIFICA_TRAMITE_CANALE_UFFICIALE"
    )
    compromised = (
        message_type == "phishing"
        and specific_action in message.get("compromising_actions", [])
    )
    false_positive_report = message_type == "legittimo" and reported
    legitimate_completion = (
        message_type == "legittimo"
        and specific_action in message.get("legitimate_actions", [])
    )

    return {
        "raw_decision": raw_decision,
        "decision": decision,
        "raw_specific_action": raw_specific_action,
        "specific_action": specific_action,
        "raw_initial_reaction": raw_decision,
        "initial_reaction": decision,
        "raw_final_action": raw_specific_action,
        "final_action": specific_action,
        "proceeded": proceeded,
        "engaged": proceeded,
        "compromised": compromised,
        "reported": reported,
        "verified": verified,
        "false_positive_report": false_positive_report,
        "legitimate_completion": legitimate_completion,
        "parse_error": False,
        "validation_error": "",
        "motivation": motivation,
        "raw_response": raw_response,
    }


def query_llm(prompt: str, interaction_seed: int, message: dict) -> dict:
    """
    Invia il prompt a Ollama, valida decision/specific_action e ritenta una sola
    volta se JSON, label o compatibilita di scenario non sono validi.
    """
    current_prompt = prompt
    last_response = ""
    last_error = ""

    for attempt in range(2):
        try:
            raw_response = post_ollama(current_prompt, interaction_seed)
            last_response = raw_response
            parsed = extract_json_response(raw_response)
            validated = validate_model_response(parsed, message, raw_response)
            if not validated["parse_error"]:
                return validated

            last_error = validated["validation_error"]
        except Exception as exc:
            last_error = str(exc)

        if attempt == 0:
            current_prompt = build_retry_prompt(prompt, message, last_error)

    return build_parse_error_response(
        last_response,
        last_error,
        f"Errore parsing/chiamata modello: {last_error}",
    )


# ------- CSV, CLI E RIEPILOGO -------

CSV_COLUMNS = [
    "run_id",
    "model",
    "temperature",
    "random_seed",
    "interaction_seed",
    "agent_id",
    "age",
    "age_group",
    "role",
    "crypto_experience",
    "security_training",
    "environment",
    "background",
    "impulsiveness",
    "trust_in_brands",
    "tech_savvy",
    "attention_level",
    "risk_aversion",
    "message_id",
    "message_type",
    "channel",
    "scenario_description",
    "urgency",
    "personalization",
    "reward",
    "raw_decision",
    "decision",
    "raw_specific_action",
    "specific_action",
    "proceeded",
    "raw_initial_reaction",
    "initial_reaction",
    "raw_final_action",
    "final_action",
    "engaged",
    "compromised",
    "reported",
    "verified",
    "false_positive_report",
    "legitimate_completion",
    "parse_error",
    "validation_error",
    "motivation",
    "raw_response",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Esegue la simulazione locale LLM per scenari di phishing crypto."
    )
    parser.add_argument("--model", default=OLLAMA_MODEL, help="Modello Ollama da usare.")
    parser.add_argument("--temperature", type=float, default=TEMPERATURE, help="Temperature Ollama.")
    parser.add_argument("--instances", type=int, default=INSTANCES_PER_ARCHETYPE, help="Istanze per archetipo.")
    parser.add_argument("--limit", type=int, default=None, help="Limita il numero di interazioni.")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED, help="Seed generale della simulazione.")
    parser.add_argument(
        "--balanced",
        action="store_true",
        help="Con --limit, distribuisce le interazioni tra scenari invece di prendere solo le prime.",
    )
    return parser.parse_args()


def build_interactions(profiles: list[dict], messages: list[dict], limit: int | None, balanced: bool):
    if limit is not None and limit < 0:
        raise ValueError("--limit deve essere maggiore o uguale a zero")

    if limit == 0:
        return []

    if limit is None or not balanced:
        interactions = [(profile, message) for profile in profiles for message in messages]
        return interactions if limit is None else interactions[:limit]

    rng = random.Random(RANDOM_SEED)
    grouped = []
    for message in messages:
        shuffled_profiles = profiles[:]
        rng.shuffle(shuffled_profiles)
        grouped.append([(profile, message) for profile in shuffled_profiles])

    interactions = []
    index = 0
    while len(interactions) < limit and any(index < len(group) for group in grouped):
        for group in grouped:
            if index < len(group):
                interactions.append(group[index])
                if len(interactions) >= limit:
                    break
        index += 1

    return interactions


def make_csv_row(run_id: str, profile: dict, message: dict, interaction_seed: int, resp: dict) -> dict:
    feats = message.get("features", {})
    traits = profile.get("traits", {})

    row = {
        "run_id": run_id,
        "model": OLLAMA_MODEL,
        "temperature": TEMPERATURE,
        "random_seed": RANDOM_SEED,
        "interaction_seed": interaction_seed,
        "agent_id": profile.get("id"),
        "age": profile.get("age"),
        "age_group": profile.get("age_group"),
        "role": profile.get("role"),
        "crypto_experience": profile.get("crypto_experience"),
        "security_training": profile.get("security_training"),
        "environment": profile.get("environment"),
        "background": profile.get("background"),
        "impulsiveness": traits.get("impulsiveness"),
        "trust_in_brands": traits.get("trust_in_brands"),
        "tech_savvy": traits.get("tech_savvy"),
        "attention_level": traits.get("attention_level"),
        "risk_aversion": traits.get("risk_aversion"),
        "message_id": message.get("id"),
        "message_type": message.get("type"),
        "channel": message.get("channel"),
        "scenario_description": message.get("description"),
        "urgency": feats.get("urgency"),
        "personalization": feats.get("personalization"),
        "reward": feats.get("reward"),
        "raw_decision": resp.get("raw_decision", ""),
        "decision": resp.get("decision", ""),
        "raw_specific_action": resp.get("raw_specific_action", ""),
        "specific_action": resp.get("specific_action", ""),
        "proceeded": resp.get("proceeded", False),
        "raw_initial_reaction": resp.get("raw_initial_reaction", ""),
        "initial_reaction": resp.get("initial_reaction", ""),
        "raw_final_action": resp.get("raw_final_action", ""),
        "final_action": resp.get("final_action", ""),
        "engaged": resp.get("engaged", False),
        "compromised": resp.get("compromised", False),
        "reported": resp.get("reported", False),
        "verified": resp.get("verified", False),
        "false_positive_report": resp.get("false_positive_report", False),
        "legitimate_completion": resp.get("legitimate_completion", False),
        "parse_error": resp.get("parse_error", False),
        "validation_error": str(resp.get("validation_error", "")).replace("\n", " "),
        "motivation": str(resp.get("motivation", "")).replace("\n", " "),
        "raw_response": str(resp.get("raw_response", "")).replace("\n", " "),
    }
    return row


def update_summary(summary: dict, row: dict):
    summary["rows"] += 1
    summary["decision_counter"][row["decision"]] += 1
    summary["specific_action_counter"][row["specific_action"]] += 1

    if str(row["parse_error"]).lower() == "true":
        summary["parse_errors"] += 1
    if str(row["reported"]).lower() == "true":
        summary["reported"] += 1
    if str(row["verified"]).lower() == "true":
        summary["verified"] += 1

    message_type = row["message_type"]
    if message_type == "phishing":
        summary["phishing_rows"] += 1
        if str(row["compromised"]).lower() == "true":
            summary["compromised_phishing"] += 1
    elif message_type == "legittimo":
        summary["legitimate_rows"] += 1
        if str(row["compromised"]).lower() == "true":
            summary["compromised_legitimate"] += 1


def print_counter(title: str, counter: Counter):
    print(f"\n{title}:")
    if not counter:
        print("  nessun dato")
        return
    for key, value in counter.most_common():
        print(f"  {key}: {value}")


def print_summary(out_path: str, summary: dict):
    total = summary["rows"]
    parse_error_rate = (summary["parse_errors"] / total * 100) if total else 0
    reported_rate = (summary["reported"] / total * 100) if total else 0
    verified_rate = (summary["verified"] / total * 100) if total else 0

    print("\nSimulazione completata.")
    print(f"File generato: {out_path}")
    print(f"Modello: {OLLAMA_MODEL}")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Righe: {total}")
    print(f"Parse error rate: {summary['parse_errors']}/{total} ({parse_error_rate:.2f}%)")

    print_counter("Decision distribution", summary["decision_counter"])
    print_counter("Specific action distribution", summary["specific_action_counter"])

    print("\nCompromised:")
    print(f"  phishing: {summary['compromised_phishing']}/{summary['phishing_rows']}")
    print(f"  legittimo: {summary['compromised_legitimate']}/{summary['legitimate_rows']}")
    print(f"\nReported rate: {summary['reported']}/{total} ({reported_rate:.2f}%)")
    print(f"Verified rate: {summary['verified']}/{total} ({verified_rate:.2f}%)")

    if summary["compromised_legitimate"] > 0:
        print("WARNING: trovate compromissioni su messaggi legittimi, non dovrebbe succedere.")


def main():
    global INSTANCES_PER_ARCHETYPE, OLLAMA_MODEL, RANDOM_SEED, TEMPERATURE

    args = parse_args()
    OLLAMA_MODEL = args.model
    TEMPERATURE = args.temperature
    INSTANCES_PER_ARCHETYPE = args.instances
    RANDOM_SEED = args.seed

    random.seed(RANDOM_SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    archetypes = load_archetypes(ARCHETYPES_PATH)
    profiles = expand_profiles(archetypes, INSTANCES_PER_ARCHETYPE)
    messages = load_messages(MESSAGES_PATH)
    interactions = build_interactions(profiles, messages, args.limit, args.balanced)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = timestamp
    out_path = os.path.join(RESULTS_DIR, f"sim_{timestamp}.csv")

    summary = {
        "rows": 0,
        "parse_errors": 0,
        "reported": 0,
        "verified": 0,
        "phishing_rows": 0,
        "legitimate_rows": 0,
        "compromised_phishing": 0,
        "compromised_legitimate": 0,
        "decision_counter": Counter(),
        "specific_action_counter": Counter(),
    }

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        total = len(interactions)
        for cnt, (profile, message) in enumerate(interactions, start=1):
            print(f"[{cnt}/{total}] {profile['id']} <- {message['id']}")

            prompt = build_prompt(profile, message)
            interaction_seed = make_interaction_seed(
                profile.get("id"),
                message.get("id"),
            )
            resp = query_llm(prompt, interaction_seed, message)
            row = make_csv_row(run_id, profile, message, interaction_seed, resp)

            writer.writerow(row)
            update_summary(summary, row)

    print_summary(out_path, summary)


if __name__ == "__main__":
    main()
