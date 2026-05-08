import json
import csv
import os
from datetime import datetime
import requests
import random

ALLOWED_CHOICES = {
    "IGNORA",
    "APRE_LINK",
    "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "INSERISCE_CREDENZIALI_O_SEED",
    "CONCEDE_ACCESSO_REMOTO",
    "INVIA_FONDI",
    "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "SEGNALA_COME_PHISHING",
    "PARSE_ERROR",
}

CHOICE_MAPPING = {
    "1": "IGNORA",
    "1) IGNORA": "IGNORA",

    "2": "APRE_LINK",
    "2) APRE_LINK": "APRE_LINK",
    "CLICCA_SUL_LINK": "APRE_LINK",
    "CLICK_SUL_LINK": "APRE_LINK",
    "CLICKA_SUL_LINK": "APRE_LINK",

    "3": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "3) COLLEGA_WALLET_O_APPROVA_TRANSAZIONE": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "COLLEGA_WALLET": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",
    "APPROVA_TRANSAZIONE": "COLLEGA_WALLET_O_APPROVA_TRANSAZIONE",

    "4": "INSERISCE_CREDENZIALI_O_SEED",
    "4) INSERISCE_CREDENZIALI_O_SEED": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCI_CREDENZIALI": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCE_CREDENZIALI": "INSERISCE_CREDENZIALI_O_SEED",
    "INSERISCE_SEED": "INSERISCE_CREDENZIALI_O_SEED",
    "FORNISCE_SEED": "INSERISCE_CREDENZIALI_O_SEED",

    "5": "CONCEDE_ACCESSO_REMOTO",
    "5) CONCEDE_ACCESSO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "INSTALLA_SOFTWARE_ACCESSO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "CONCEDE_CONTROLLO_REMOTO": "CONCEDE_ACCESSO_REMOTO",
    "CONDIVIDE_SCHERMO": "CONCEDE_ACCESSO_REMOTO",

    "6": "INVIA_FONDI",
    "6) INVIA_FONDI": "INVIA_FONDI",

    "7": "VERIFICA_TRAMITE_CANALE_UFFICIALE",
    "7) VERIFICA_TRAMITE_CANALE_UFFICIALE": "VERIFICA_TRAMITE_CANALE_UFFICIALE",

    "8": "SEGNALA_COME_PHISHING",
    "8) SEGNALA_COME_PHISHING": "SEGNALA_COME_PHISHING",
}


# ------- CONFIGURAZIONE -------

OLLAMA_MODEL = "llama3"  # cambia se usi un modello diverso
OLLAMA_URL = "http://localhost:11434/api/generate"

ARCHETYPES_PATH = os.path.join("agents", "profiles_archetypes.json")
MESSAGES_PATH = os.path.join("scenarios", "messages.json")

RESULTS_DIR = "results"
INSTANCES_PER_ARCHETYPE = 6  # 16 archetipi * 6 = 96 agenti
RANDOM_SEED = 42


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
2) APRE_LINK
3) COLLEGA_WALLET_O_APPROVA_TRANSAZIONE
4) INSERISCE_CREDENZIALI_O_SEED
5) CONCEDE_ACCESSO_REMOTO
6) INVIA_FONDI
7) VERIFICA_TRAMITE_CANALE_UFFICIALE
8) SEGNALA_COME_PHISHING

Nota:
- APRE_LINK indica che l’utente apre il collegamento ma non inserisce dati, non collega wallet e non autorizza transazioni.
- COLLEGA_WALLET_O_APPROVA_TRANSAZIONE indica che l’utente collega il wallet o approva una richiesta on-chain potenzialmente rischiosa.
- INSERISCE_CREDENZIALI_O_SEED indica che l’utente inserisce password, codice OTP, seed phrase o altre informazioni sensibili.
- INVIA_FONDI indica che l’utente trasferisce criptovalute verso l’indirizzo indicato dal messaggio.
- VERIFICA_TRAMITE_CANALE_UFFICIALE indica che l’utente non procede subito, ma controlla tramite sito ufficiale, app ufficiale, supporto verificato o persona esperta.
- CONCEDE_ACCESSO_REMOTO indica che l’utente installa o avvia un software di accesso remoto, condivide lo schermo, concede controllo remoto o segue istruzioni operative che permettono all’interlocutore di accedere al dispositivo.

Agisci coerentemente con il profilo assegnato. Considera esperienza, attenzione, impulsività, fiducia, formazione e contesto d'uso.
Scegli l'azione finale che l'utente compirebbe realisticamente dopo aver letto e valutato il messaggio.
Non scegliere automaticamente l'azione più rischiosa. L'agente deve fermarsi al punto in cui, in base al proprio profilo, diventerebbe sospettoso, chiederebbe conferma, ignorerebbe il messaggio o procederebbe.
Se il messaggio non è rilevante per il profilo, se l'utente non riconosce il servizio, se è occupato, disinteressato o non ha un motivo concreto per interagire, può scegliere IGNORA.
Se l'utente aprirebbe il link solo per controllare ma poi non inserirebbe dati, non collegherebbe wallet e non approverebbe transazioni, scegli APRE_LINK.
Se l'utente aprirebbe il link e poi collegherebbe il wallet o approverebbe una richiesta on-chain, scegli COLLEGA_WALLET_O_APPROVA_TRANSAZIONE.
Se l'utente inserirebbe credenziali, codici OTP o seed phrase, scegli INSERISCE_CREDENZIALI_O_SEED.
Se l'utente invierebbe criptovalute all'indirizzo indicato, scegli INVIA_FONDI.
Se l'utente non procede subito ma controlla tramite sito ufficiale, app ufficiale, supporto verificato o persona esperta, scegli VERIFICA_TRAMITE_CANALE_UFFICIALE.
Se l'utente riconosce chiaramente il tentativo di phishing e lo segnala o lo classifica come malevolo, scegli SEGNALA_COME_PHISHING.
In molti casi un utente reale può semplicemente ignorare un messaggio senza analizzarlo a fondo. Usa IGNORA quando questa è la reazione più plausibile per il profilo.

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
    Salva sia la scelta grezza sia quella normalizzata.
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
                    "temperature": 0.4,
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

        raw_choice = str(parsed.get("choice", "")).strip().upper()
        motivation = str(parsed.get("motivation", "")).strip()

        normalized_choice = CHOICE_MAPPING.get(raw_choice, raw_choice)

        if normalized_choice not in ALLOWED_CHOICES:
            normalized_choice = "PARSE_ERROR"

        return {
            "raw_choice": raw_choice,
            "choice": normalized_choice,
            "motivation": motivation,
            "raw_response": text,
            "parse_error": normalized_choice == "PARSE_ERROR"
        }

    except Exception as e:
        return {
            "raw_choice": "",
            "choice": "PARSE_ERROR",
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
            "message_id",
            "message_type",
            "channel",
            "scenario_description",
            "urgency",
            "personalization",
            "reward",
            "raw_choice",
            "choice",
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
                    message.get("id"),
                    message.get("type"),
                    message.get("channel"),
                    message.get("description"),
                    feats.get("urgency"),
                    feats.get("personalization"),
                    feats.get("reward"),
                    resp.get("raw_choice", ""),
                    resp.get("choice", ""),
                    resp.get("parse_error", ""),
                    resp.get("motivation", "").replace("\n", " "),
                    resp.get("raw_response", "").replace("\n", " ")
                ])

    print(f"Simulazione completata. File salvato in: {out_path}")


if __name__ == "__main__":
    main()