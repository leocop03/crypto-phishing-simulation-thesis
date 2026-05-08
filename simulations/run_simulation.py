import json
import csv
import os
from datetime import datetime
import requests
import random


# ------- CONFIGURAZIONE -------

OLLAMA_MODEL = "llama3"  # cambia se usi un modello diverso
OLLAMA_URL = "http://localhost:11434/api/generate"

ARCHETYPES_PATH = os.path.join("agents", "profiles_archetypes.json")
MESSAGES_PATH = os.path.join("scenarios", "messages.json")

RESULTS_DIR = "results"
INSTANCES_PER_ARCHETYPE = 6  # 14 archetipi * 6 ≈ 84 agenti


# ------- FUNZIONI DI CARICAMENTO -------

def load_archetypes(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def expand_profiles(archetypes, instances_per_archetype=INSTANCES_PER_ARCHETYPE):
    """
    Clona ogni archetipo in più agenti:
    - id: aggiunge suffisso _1, _2, ...
    - età: piccola variazione random +/- 2 anni (clampata nella stessa fascia d'età)
    """
    profiles = []

    for arch in archetypes:
        base_age = arch.get("age", 30)
        for i in range(instances_per_archetype):
            profile = json.loads(json.dumps(arch))  # deep copy
            profile["id"] = f"{arch['id']}_{i+1}"

            # variazione età controllata
            jitter = random.randint(-2, 2)
            new_age = max(15, base_age + jitter)
            profile["age"] = new_age

            profiles.append(profile)

    return profiles


def load_messages(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------- PROMPT & CHIAMATA LLM -------

def build_prompt(agent_profile: dict, message: dict) -> str:
    """
    Costruisce il prompt per un singolo agente e un singolo messaggio.
    Il modello deve rispondere in JSON con 'choice' e 'motivation'.
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
- Tratti: impulsività={traits.get('impulsiveness')}, fiducia nei brand={traits.get('trust_in_brands')}, competenza tecnologica={traits.get('tech_savvy')}, livello di attenzione={traits.get('attention_level')}, avversione al rischio={traits.get('risk_aversion')}

Ricevi il seguente messaggio ({message.get('channel')}), relativo al mondo delle criptovalute:

\"\"\"{message.get('text')}\"\"\".

Devi scegliere UNA sola azione tra:
1) IGNORA
2) CLICCA_SUL_LINK
3) INSERISCI_CREDENZIALI
4) CHIEDI_AIUTO_AMICO
5) SEGNALA_COME_PHISHING

INTERPRETA il profilo in modo realistico: non essere perfetto per forza, ma agisci come faresti nella vita reale dato il tuo carattere.

Rispondi in JSON esattamente nel formato:
{{
  "choice": "UNA_DELLE_AZIONI_SOPRA",
  "motivation": "spiega in 2-3 frasi il perché della scelta"
}}
Non aggiungere testo fuori dal JSON.
"""


def query_llm(prompt: str) -> dict:
    """
    Invia il prompt a Ollama e tenta di parsare un JSON con 'choice' e 'motivation'.
    In caso di errore, ritorna una scelta di fallback 'IGNORA'.
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "")

        # Cerca un blocco JSON dentro la risposta
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("Nessun JSON trovato nella risposta del modello")

        json_str = text[start:end + 1]
        parsed = json.loads(json_str)

        # Normalizza chiavi
        choice = str(parsed.get("choice", "")).strip().upper()
        motivation = str(parsed.get("motivation", "")).strip()

        if choice == "":
            choice = "IGNORA"

        return {
            "choice": choice,
            "motivation": motivation
        }

    except Exception as e:
        # fallback molto conservativo
        return {
            "choice": "IGNORA",
            "motivation": f"Fallback per errore di parsing o chiamata modello: {e}"
        }


# ------- MAIN SIMULATION -------

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # 1) carica archetipi e li espande in profili
    archetypes = load_archetypes(ARCHETYPES_PATH)
    profiles = expand_profiles(archetypes, INSTANCES_PER_ARCHETYPE)

    # 2) carica messaggi
    messages = load_messages(MESSAGES_PATH)

    # 3) prepara file CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(RESULTS_DIR, f"sim_{timestamp}.csv")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "agent_id",
            "age",
            "age_group",
            "role",
            "crypto_experience",
            "security_training",
            "environment",
            "message_id",
            "message_type",
            "channel",
            "scenario_description",
            "urgency",
            "personalization",
            "reward",
            "choice",
            "motivation"
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

                writer.writerow([
                    profile.get("id"),
                    profile.get("age"),
                    profile.get("age_group"),
                    profile.get("role"),
                    profile.get("crypto_experience"),
                    profile.get("security_training"),
                    profile.get("environment"),
                    message.get("id"),
                    message.get("type"),
                    message.get("channel"),
                    message.get("description"),
                    feats.get("urgency"),
                    feats.get("personalization"),
                    feats.get("reward"),
                    resp.get("choice", ""),
                    resp.get("motivation", "").replace("\n", " ")
                ])

    print(f"Simulazione completata. File salvato in: {out_path}")


if __name__ == "__main__":
    main()