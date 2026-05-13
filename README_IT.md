# Simulazione di phishing crypto per tesi

Questo repository contiene un framework locale basato su LLM per studiare come archetipi sintetici di utenti reagiscono a messaggi crypto fraudolenti e legittimi.

## Scopo del progetto

Il progetto ha finalita accademica e difensiva. Simula il comportamento di archetipi sintetici davanti a messaggi legati al mondo crypto, includendo scenari di phishing e messaggi legittimi di controllo.

Non misura tassi reali di phishing e non deve essere letto come una stima empirica del successo degli attacchi. Serve a esplorare comportamenti simulati, confrontare scenari e profili, e discutere i limiti metodologici dell'uso di agenti LLM in cybersecurity.

## Ambito etico e di sicurezza

- Gli scenari sono sintetici.
- I domini usano valori sicuri o di test, per esempio `.test`.
- Non viene creato nessun dominio reale operativo.
- Non viene contattato nessun utente reale.
- Non viene costruita nessuna infrastruttura di phishing.
- Non vengono raccolte credenziali, dati wallet o fondi.
- La finalita e accademica, educativa e difensiva.
- Gli output sono simulati e non vanno interpretati come percentuali reali di successo.

## Struttura del repository

```text
agents/
  profiles_archetypes.json      Archetipi sintetici degli utenti
scenarios/
  messages.json                 Messaggi sintetici di phishing e legittimi
simulations/
  run_simulation.py             Script principale della simulazione
  analyze_latest.py             Analisi terminale dell'ultimo CSV
results/
  sim_*.csv                     Output locali generati, ignorati da Git
analysis.ipynb                  Notebook opzionale di analisi
README.md                       Documentazione in inglese
requirements.txt                Dipendenze Python
```

## Disegno della simulazione

Gli agenti sono archetipi sintetici descritti da attributi demografici, tecnici, comportamentali e contestuali. I messaggi includono sia scenari fraudolenti sia scenari legittimi.

La simulazione assume che il messaggio sia gia stato ricevuto e letto. La lettura non e una scelta simulata. La prima scelta modellata e la reazione comportamentale dopo la lettura.

Se l'utente procede, entra nel flow proposto dal messaggio. Nel flow puo fermarsi prima della compromissione oppure completare l'azione finale richiesta.

La struttura e a due passaggi:

1. decisione iniziale dopo la lettura;
2. esito del flow se l'utente procede.

L'etichetta interna `message_type` viene usata da validazione e analisi, ma non viene mostrata al modello come informazione esplicita per decidere.

### `decision`

- `IGNORA`: l'utente ignora il messaggio.
- `RIMANDA_O_NON_DECIDE`: l'utente rimanda o lascia il messaggio in sospeso.
- `VERIFICA_TRAMITE_CANALE_UFFICIALE`: l'utente controlla tramite un canale ufficiale indipendente.
- `SEGNALA_COME_PHISHING`: l'utente segnala o marca il messaggio come sospetto.
- `PROCEDE_CON_LA_RICHIESTA`: l'utente entra nel flow proposto dal messaggio.

### `flow_outcome`

- `NON_ENTRA_NEL_FLOW`: l'utente non entra nel flow.
- `SI_FERMA_PRIMA_DELLA_COMPROMISSIONE`: l'utente entra nel flow ma si ferma prima dell'azione finale compromettente.
- `COMPROMISSIONE_COMPLETATA`: l'utente completa una compromissione compatibile con lo scenario.
- `AZIONE_LEGITTIMA_COMPLETATA`: l'utente completa una richiesta legittima.

### `compromise_action`

- `NESSUNA`
- `INSERISCE_CREDENZIALI`
- `INSERISCE_DATI_KYC`
- `INSERISCE_SEED_PHRASE`
- `COLLEGA_WALLET`
- `APPROVA_TRANSAZIONE`
- `CONCEDE_ACCESSO_REMOTO`
- `INVIA_FONDI`
- `INSTALLA_APP_O_SOFTWARE`

`compromise_action` e specifica dello scenario. In uno scenario phishing, la compromissione e valida solo se l'azione appartiene a `possible_compromise_actions` per quello scenario.

## Calcolo della compromissione

I messaggi legittimi non generano compromissione. Entrare nel flow non significa automaticamente essere compromessi. La compromissione richiede phishing, completamento del flow e azione compatibile con lo scenario.

```python
compromised = (
    message_type == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in possible_compromise_actions
)
```

Questo schema distingue:

- utenti che non entrano nel flow;
- utenti che entrano ma si fermano prima della compromissione;
- utenti che completano una compromissione scenario-specifica;
- utenti che completano un'azione legittima.

## Modello usato

- Modello consigliato: `qwen3:8b` tramite Ollama.
- Temperatura consigliata: `0.3`.
- Output JSON validato.
- Schema JSON / structured output usato quando disponibile.
- Fallback a JSON mode se la versione locale di Ollama non supporta lo schema.
- Retry massimo una volta in caso di risposta non valida.

## Come eseguire

Creare e attivare l'ambiente virtuale su Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Mini-run bilanciata:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Run completa:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analisi:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## Opzioni CLI

- `--model`: modello Ollama da usare.
- `--temperature`: temperatura del modello.
- `--instances`: numero di istanze generate per archetipo.
- `--limit`: numero massimo di interazioni.
- `--seed`: seed generale della simulazione.
- `--balanced`: con `--limit`, distribuisce le interazioni tra scenari.

## Output CSV

Ogni riga del CSV rappresenta una interazione tra un agente sintetico e un messaggio.

Colonne principali:

- `agent_id`
- `archetype_id`
- `message_id`
- `message_type`
- `decision`
- `flow_outcome`
- `compromise_action`
- `entered_flow`
- `stopped_before_compromise`
- `compromised`
- `verified`
- `reported`
- `ignored`
- `delayed`
- `legitimate_completion`
- `parse_error`
- `validation_error`
- `motivation`
- `raw_response`

Il CSV contiene anche metadati della run, tratti dell'agente, feature del messaggio e alias retrocompatibili per analisi precedenti.

## Analisi dei risultati

`simulations/analyze_latest.py`:

- carica l'ultimo CSV da `results/`, oppure un file scelto con `--file`;
- stampa file analizzato, numero di righe, modello e temperatura se presenti;
- calcola parse error e validation error;
- stampa la distribuzione di `decision`;
- stampa la distribuzione di `flow_outcome`;
- stampa la distribuzione di `compromise_action`;
- calcola entered flow, stop prima della compromissione, verifica, segnalazione, ignore, delay e completamento legittimo;
- calcola il tasso di compromissione sui soli phishing;
- controlla che i messaggi legittimi abbiano `compromised = False`;
- produce risultati per scenario e per archetipo;
- produce tabelle scenario x `flow_outcome` e scenario x `compromise_action`;
- segnala possibili problemi metodologici senza trasformarli in obiettivi da forzare.

## Limiti metodologici

- I risultati non sono percentuali reali.
- Gli agenti sintetici non sono utenti reali.
- Il modello puo avere bias prudenziali o comportamenti troppo regolari.
- La simulazione dipende da prompt, modello, temperatura, validazione e scenari.
- Poche segnalazioni possono indicare una sottorappresentazione del comportamento di reporting.
- Molti stop prima della compromissione possono indicare bias prudenziale.
- Il framework e esplorativo e va discusso come simulazione, non come misura del comportamento umano reale.

## Workflow consigliato

1. Eseguire una mini-run bilanciata.
2. Analizzare l'output.
3. Eseguire la run completa solo dopo aver controllato schema e prompt.
4. Confrontare versioni diverse di prompt o modello quando serve.
