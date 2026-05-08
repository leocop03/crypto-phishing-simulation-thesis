import requests
import json

OLLAMA_MODEL = "llama3"

def build_prompt(agent_profile, message):
    return f"""
Sei un utente chiamato {agent_profile['id']}.

Profilo:
- Età: {agent_profile['age']}
- Esperienza con le criptovalute: {agent_profile['crypto_experience']}
- Formazione sulla sicurezza: {agent_profile['security_training']}
- Tratti: impulsività={agent_profile['traits']['impulsiveness']},
  fiducia nei brand={agent_profile['traits']['trust_in_brands']},
  competenza tecnologica={agent_profile['traits']['tech_savvy']}.

Ricevi il seguente messaggio ({message['channel']}):
\"\"\"{message['text']}\"\"\".

Devi scegliere UNA sola azione tra:
1) IGNORA
2) CLICCA_SUL_LINK
3) INSERISCI_CREDENZIALI
4) CHIEDI_AIUTO_AMICO
5) SEGNALA_COME_PHISHING

Rispondi in JSON esattamente nel formato:
{{
  "choice": "UNA_DELLE_AZIONI_SOPRA",
  "motivation": "spiega in 2-3 frasi il perché della scelta"
}}
"""

def query_llm(prompt: str) -> dict:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    text = data["response"]
    # qui puoi fare un try/except per json.loads, nel caso il modello sgarra
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {"choice": "IGNORA", "motivation": "errore parsing"}