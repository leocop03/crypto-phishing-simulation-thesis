import json
import csv
import os
from datetime import datetime
import requests
import random

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

ALLOWED_INITIAL_REACTIONS = {
    "IGNORA",
    "APRE_MESSAGGIO_O_LINK",
    "SEGNALA_SUBITO",
    "VERIFICA_SUBITO",
    "PARSE_ERROR",
}

ALLOWED_FINAL_ACTIONS = {
    "NESSUNA_AZIONE_ULTERIORE",
    "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "INSERISCE_CREDENZIALI_O_SEED",
    "CONCEDE_ACCESSO_REMOTO",
    "INVIA_FONDI",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA_COME_PHISHING",
    "PARSE_ERROR",
}

INITIAL_REACTION_MAPPING = {
    "1": "IGNORA",
    "1) IGNORA": "IGNORA",

    "2": "APRE_MESSAGGIO_O_LINK",
    "2) APRE_MESSAGGIO_O_LINK": "APRE_MESSAGGIO_O_LINK",
    "APRE_LINK": "APRE_MESSAGGIO_O_LINK",
    "APRE_MESSAGGIO": "APRE_MESSAGGIO_O_LINK",
    "CLICCA_SUL_LINK": "APRE_MESSAGGIO_O_LINK",
    "CLICK_SUL_LINK": "APRE_MESSAGGIO_O_LINK",
    "CLICKA_SUL_LINK": "APRE_MESSAGGIO_O_LINK",

    "3": "SEGNALA_SUBITO",
    "3) SEGNALA_SUBITO": "SEGNALA_SUBITO",
    "SEGNALA_COME_PHISHING": "SEGNALA_SUBITO",

    "4": "VERIFICA_SUBITO",
    "4) VERIFICA_SUBITO": "VERIFICA_SUBITO",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE": "VERIFICA_SUBITO",
}

FINAL_ACTION_MAPPING = {
    "0": "NESSUNA_AZIONE_ULTERIORE",
    "1": "NESSUNA_AZIONE_ULTERIORE",
    "1) NESSUNA_AZIONE_ULTERIORE": "NESSUNA_AZIONE_ULTERIORE",
    "NESSUNA": "NESSUNA_AZIONE_ULTERIORE",
    "NESSUNA_AZIONE": "NESSUNA_AZIONE_ULTERIORE",
    "APRE_LINK": "NESSUNA_AZIONE_ULTERIORE",

    "2": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "2) COLLEGA_WALLET_O_APPROVA_TRANSAZIONE": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "COLLEGA_WALLET": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "APPROVA_TRANSAZIONE": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",

    "3": "INSERISCE_CREDENZIALI_O_SEED",
    "3) INSERISCE_CREDENZIALI_O_SEED": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCI_CREDENZIALI": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCE_CREDENZIALI": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCE_SEED": "INSERISCE_CREDENZIALI_O_SEED",
    "FORNISCE_SEED": "INSERISCE_CREDENZIALI_O_SEED",

    "4": "CONCEDE_ACCESSO_REMOTO",
    "4) CONCEDE_ACCESSO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "INSTALLA_SOFTWARE_ACCESSO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "CONCEDE_CONTROLLO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "CONDIVIDE_SCHERMO": "CONCEDE_ACCESSO_REMOTO",

    "5": "INVIA_FONDI",
    "5) INVIA_FONDI": "INVIA_FONDI",

    "6": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "6) VERIFICA_TRAMITE_CANALE_UFFICIALE": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "VERIFICA_SUBITO": "VERIFICA_TRAMITE_CANALE_UFFICIALE",

    "7": "SEGNALA_COME_PHISHING",
    "7) SEGNALA_COME_PHISHING": "SEGNALA_COME_PHISHING",
    "SEGNALA_SUBITO": "SEGNALA_COME_PHISHING",
}

COMPROMISING_FINAL_ACTIONS = {
    "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "INSERISCE_CREDENZIALI_O_SEED",
    "CONCEDE_ACCESSO_REMOTO",
    "INVIA_FONDI",
}


def normalize_model_label(value) -> str:
    return str(value).strip().upper().replace(" ", "_").replace("-", "_")


# ------- CONFIGURAZIONE -------

OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

ARCHETYPES_PATH = os.path.join("agents", "profiles_archetypes.json")
MESSAGES_PATH = os.path.join("scenarios", "messages.json")

RESULTS_DIR = "results"
INSTANCES_PER_ARCHETYPE = 6  # 16 archetipi * 6 = 96 agenti
RANDOM_SEED = 42 # genera casualità nello stesso ordine


# ------- FUNZIONI DI CARICAMENTO -------

def load_archetypes(path: str):
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
    Clona ogni archetipo in più agenti:
    - id: aggiunge suffisso _1, _2, ...
    - età: piccola variazione random +/- 2 anni (clampata nella stessa fascia d'età)
    - tratti comportamentali: variazioni controllate su attenzione, impulsivita, fiducia e rischio
    - formazione/consapevolezza: possibile variazione di un livello
    - background: dettaglio situazionale casuale
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
            profile["id"] = f"{arch['id']}_{i+1}"

            # variazione età controllata
            jitter = random.randint(-2, 2)
            new_age = max(15, base_age + jitter)
            profile["age"] = new_age

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


def load_messages(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------- PROMPT & CHIAMATA LLM -------

def build_prompt(agent_profile: dict, message: dict) -> str:
    """
    Costruisce il prompt per un singolo agente e un singolo messaggio.
    Il modello deve rispondere in JSON con 'initial_reaction', 'final_action' e 'motivation'.
    """
    traits = agent_profile.get("traits", {})
    return f"""
Sei un utente chiamato {agent_profile.get('id')}.

Profilo:
- Età: {agent_profile.get('age')}
- Fascia d'età: {agent_profile.get('age_group')}
- Ruolo: {agent_profile.get('role')}
- Esperienza con le criptovalute: {agent_profile.get('crypto_experience')}
- Formazione sulla sicurezza: {agent_profile.get('security_training')}
- Contesto d'uso: {agent_profile.get('environment')}
- Background individuale: {agent_profile.get('background')}
- Tratti: impulsività={traits.get('impulsiveness')}, fiducia nei brand={traits.get('trust_in_brands')}, competenza tecnologica={traits.get('tech_savvy')}, livello di attenzione={traits.get('attention_level')}, avversione al rischio={traits.get('risk_aversion')}

Ricevi il seguente messaggio ({message.get('channel')}), relativo al mondo delle criptovalute:

\"\"\"{message.get('text')}\"\"\".

Devi modellare la risposta in due livelli distinti.

Livello 1 - reazione iniziale:
1) IGNORA
2) APRE_MESSAGGIO_O_LINK
3) SEGNALA_SUBITO
4) VERIFICA_SUBITO

Livello 2 - azione finale o successiva:
1) NESSUNA_AZIONE_ULTERIORE
2) COLLEGA_WALLET_O_APPROVA_TRANSAZIONE
3) INSERISCE_CREDENZIALI_O_SEED
4) CONCEDE_ACCESSO_REMOTO
5) INVIA_FONDI
6) VERIFICA_TRAMITE_CANALE_UFFICIALE
7) SEGNALA_COME_PHISHING

Regole:
- initial_reaction descrive cosa fa l'utente appena riceve il messaggio.
- final_action descrive cosa fa dopo, se va oltre la prima reazione.
- Se initial_reaction e IGNORA, final_action deve essere NESSUNA_AZIONE_ULTERIORE.
- Se initial_reaction e SEGNALA_SUBITO, final_action deve essere SEGNALA_COME_PHISHING.
- Se initial_reaction e VERIFICA_SUBITO, final_action deve essere VERIFICA_TRAMITE_CANALE_UFFICIALE.
- Se initial_reaction e APRE_MESSAGGIO_O_LINK, final_action puo essere NESSUNA_AZIONE_ULTERIORE, una delle azioni compromettenti, oppure una verifica/segnalazione successiva.

Significato delle azioni:
- APRE_MESSAGGIO_O_LINK indica che l'utente apre il messaggio o il collegamento, ma questo da solo non equivale a compromissione.
- COLLEGA_WALLET_O_APPROVA_TRANSAZIONE indica che l’utente collega il wallet o approva una richiesta on-chain potenzialmente rischiosa.
- INSERISCE_CREDENZIALI_O_SEED indica che l’utente inserisce password, codice OTP, seed phrase o altre informazioni sensibili.
- INVIA_FONDI indica che l’utente trasferisce criptovalute verso l’indirizzo indicato dal messaggio.
- VERIFICA_TRAMITE_CANALE_UFFICIALE indica che l’utente non procede subito, ma controlla tramite sito ufficiale, app ufficiale, supporto verificato o persona esperta.
- CONCEDE_ACCESSO_REMOTO indica che l’utente installa o avvia un software di accesso remoto, condivide lo schermo, concede controllo remoto o segue istruzioni operative che permettono all’interlocutore di accedere al dispositivo.

Agisci coerentemente con il profilo assegnato. Considera esperienza, attenzione, impulsività, fiducia, formazione e contesto d'uso.
Scegli l'azione finale che l'utente compirebbe realisticamente dopo aver letto e valutato il messaggio.
Non scegliere automaticamente l'azione più rischiosa. L'agente deve fermarsi al punto in cui, in base al proprio profilo, diventerebbe sospettoso, chiederebbe conferma, ignorerebbe il messaggio o procederebbe.
Nella vita reale alcune persone ignorano messaggi senza analizzarli a fondo, soprattutto quando sono occupate, disinteressate o percepiscono il messaggio come poco rilevante.
Tuttavia, messaggi molto urgenti, personalizzati o legati alla sicurezza di account e fondi tendono più facilmente a generare una reazione attiva, positiva o negativa.

Una reazione attiva non implica necessariamente compromissione: aprire il messaggio o il link puo fermarsi prima di inserire dati, collegare wallet, concedere accesso remoto o inviare fondi.

Rispondi in JSON esattamente nel formato:
{{
  "initial_reaction": "UNA_DELLE_REAZIONI_INIZIALI",
  "final_action": "UNA_DELLE_AZIONI_FINALI",
  "motivation": "spiega brevemente in una frase il perché della scelta"
}}
Non aggiungere testo fuori dal JSON.
"""


def query_llm(prompt: str) -> dict:
    """
    Invia il prompt a Ollama e tenta di parsare un JSON con 'initial_reaction',
    'final_action' e 'motivation'. Salva valori grezzi e normalizzati.
    In caso di errore ritorna PARSE_ERROR, non IGNORA, per non falsare i risultati.
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.4, # più è alta più è creativo ma incoerente
                    "seed": RANDOM_SEED
                }
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "")

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("Nessun JSON trovato nella risposta del modello")

        json_str = text[start:end + 1]
        parsed = json.loads(json_str)

        raw_initial_reaction = normalize_model_label(parsed.get("initial_reaction", parsed.get("choice", "")))
        raw_final_action = normalize_model_label(parsed.get("final_action", ""))
        motivation = str(parsed.get("motivation", "")).strip()

        initial_reaction = INITIAL_REACTION_MAPPING.get(raw_initial_reaction, raw_initial_reaction)
        final_action = FINAL_ACTION_MAPPING.get(raw_final_action, raw_final_action)

        if initial_reaction not in ALLOWED_INITIAL_REACTIONS:
            initial_reaction = "PARSE_ERROR"

        if final_action not in ALLOWED_FINAL_ACTIONS:
            final_action = "PARSE_ERROR"

        if initial_reaction == "IGNORA":
            final_action = "NESSUNA_AZIONE_ULTERIORE"
        elif initial_reaction == "SEGNALA_SUBITO":
            final_action = "SEGNALA_COME_PHISHING"
        elif initial_reaction == "VERIFICA_SUBITO":
            final_action = "VERIFICA_TRAMITE_CANALE_UFFICIALE"

        parse_error = initial_reaction == "PARSE_ERROR" or final_action == "PARSE_ERROR"
        engaged = initial_reaction not in {"IGNORA", "PARSE_ERROR"}
        compromised = final_action in COMPROMISING_FINAL_ACTIONS
        reported = initial_reaction == "SEGNALA_SUBITO" or final_action == "SEGNALA_COME_PHISHING"
        verified = initial_reaction == "VERIFICA_SUBITO" or final_action == "VERIFICA_TRAMITE_CANALE_UFFICIALE"

        return {
            "raw_initial_reaction": raw_initial_reaction,
            "initial_reaction": initial_reaction,
            "raw_final_action": raw_final_action,
            "final_action": final_action,
            "engaged": engaged,
            "compromised": compromised,
            "reported": reported,
            "verified": verified,
            "motivation": motivation,
            "raw_response": text,
            "parse_error": parse_error
        }

    except Exception as e:
        return {
            "raw_initial_reaction": "",
            "initial_reaction": "PARSE_ERROR",
            "raw_final_action": "",
            "final_action": "PARSE_ERROR",
            "engaged": False,
            "compromised": False,
            "reported": False,
            "verified": False,
            "motivation": f"Errore parsing/chiamata modello: {e}",
            "raw_response": "",
            "parse_error": True
        }


# ------- MAIN SIMULATION -------

def main():
    random.seed(RANDOM_SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # 1) carica archetipi e li espande in profili
    archetypes = load_archetypes(ARCHETYPES_PATH)
    profiles = expand_profiles(archetypes, INSTANCES_PER_ARCHETYPE)

    # 2) carica messaggi
    messages = load_messages(MESSAGES_PATH)

    # 3) prepara file CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = timestamp

    out_path = os.path.join(RESULTS_DIR, f"sim_{timestamp}.csv")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "run_id",
            "model",
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
            "raw_initial_reaction",
            "initial_reaction",
            "raw_final_action",
            "final_action",
            "engaged",
            "compromised",
            "reported",
            "verified",
            "parse_error",
            "motivation",
            "raw_response"
        ])

        # 4) per ogni agente x messaggio, genera prompt, chiama LLM, salva riga
        total = len(profiles) * len(messages)
        cnt = 0

        for profile in profiles:
            for message in messages:
                cnt += 1
                print(f"[{cnt}/{total}] {profile['id']} <- {message['id']}")

                prompt = build_prompt(profile, message)
                resp = query_llm(prompt)

                feats = message.get("features", {})
                traits = profile.get("traits", {})

                writer.writerow([
                    run_id,
                    OLLAMA_MODEL,
                    profile.get("id"),
                    profile.get("age"),
                    profile.get("age_group"),
                    profile.get("role"),
                    profile.get("crypto_experience"),
                    profile.get("security_training"),
                    profile.get("environment"),
                    profile.get("background"),
                    traits.get("impulsiveness"),
                    traits.get("trust_in_brands"),
                    traits.get("tech_savvy"),
                    traits.get("attention_level"),
                    traits.get("risk_aversion"),
                    message.get("id"),
                    message.get("type"),
                    message.get("channel"),
                    message.get("description"),
                    feats.get("urgency"),
                    feats.get("personalization"),
                    feats.get("reward"),
                    resp.get("raw_initial_reaction", ""),
                    resp.get("initial_reaction", ""),
                    resp.get("raw_final_action", ""),
                    resp.get("final_action", ""),
                    resp.get("engaged", ""),
                    resp.get("compromised", ""),
                    resp.get("reported", ""),
                    resp.get("verified", ""),
                    resp.get("parse_error", ""),
                    resp.get("motivation", "").replace("\n", " "),
                    resp.get("raw_response", "").replace("\n", " ")
                ])

    print(f"Simulazione completata. File salvato in: {out_path}")


if __name__ == "__main__":
    main()
