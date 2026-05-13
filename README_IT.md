# Simulazione di phishing crypto per tesi

Questo repository contiene la parte sperimentale di una tesi triennale in Cybersecurity dedicata al phishing nel mondo delle criptovalute, alla social engineering e alle decisioni degli utenti sotto pressione.

Il progetto simula il comportamento di profili utente sintetici davanti a messaggi di phishing e messaggi legittimi legati al contesto crypto. Ogni interazione viene valutata da un Large Language Model eseguito localmente tramite Ollama.

L'idea centrale è che sia l'LLM a prendere la decisione comportamentale dell'agente. Python prepara l'esperimento, costruisce i prompt, normalizza le risposte e salva i risultati, ma non decide statisticamente quale azione deve compiere l'utente.

La simulazione ha valore esplorativo. Non serve a stimare percentuali reali di successo del phishing e non sostituisce studi empirici condotti su persone reali.

---

## Avvertenza importante

Questo repository è pensato esclusivamente per:

- ricerca accademica;
- educazione alla cybersecurity;
- analisi del comportamento davanti a messaggi sospetti;
- simulazioni difensive e controllate.

Il progetto **non**:

- esegue phishing reale;
- contatta utenti reali;
- raccoglie credenziali;
- interagisce con wallet reali;
- usa infrastrutture malevole reali;
- automatizza attacchi;
- contiene kit di phishing o strumenti offensivi.

Tutti gli scenari sono sintetici. I link usano domini `.test`, quindi non rappresentano infrastrutture operative.

---

## Contesto della ricerca

Nel mondo crypto molti attacchi non colpiscono direttamente la blockchain, ma sfruttano il comportamento umano: urgenza, paura, fiducia nei brand, finti operatori di supporto, messaggi di sicurezza, richieste di verifica wallet, accesso remoto o promesse di guadagni facili.

Questo repository serve a esplorare in modo controllato come utenti sintetici diversi possano reagire a messaggi di questo tipo.

La tesi più ampia analizza il phishing e la social engineering nel contesto delle criptovalute, includendo anche uno scenario ispirato a un caso studio di furto crypto ad alto valore.

---

## Obiettivi del progetto

La simulazione serve a osservare:

- come profili utente diversi reagiscono a messaggi di phishing crypto;
- quanto incidono urgenza, personalizzazione e promessa di ricompensa;
- come cambiano le risposte in base a formazione sulla sicurezza ed esperienza crypto;
- la differenza tra ignorare, verificare, segnalare, rimandare o procedere con un'azione specifica dello scenario;
- come vengono trattati i messaggi legittimi di controllo;
- come si comportano gli agenti davanti a scenari mirati ispirati al caso studio;
- quali limiti emergono usando agenti LLM per simulare comportamenti umani in cybersecurity.

I risultati vanno letti come confronto tra profili e scenari, non come fotografia statistica del mondo reale.

---

## Struttura del repository

```text
crypto-phishing-simulation-thesis/
│
├── agents/
│   └── profiles_archetypes.json
│
├── scenarios/
│   └── messages.json
│
├── simulations/
│   ├── run_simulation.py
│   └── analyze_latest.py
│
├── results/
│   └── generata localmente e ignorata da Git
│
├── analysis.ipynb
├── requirements.txt
├── README.md
├── README_IT.md
└── .gitignore
```

---

## File principali

### `agents/profiles_archetypes.json`

Contiene gli archetipi di utenti sintetici. Ogni archetipo rappresenta una tipologia di utente con caratteristiche demografiche, tecniche e comportamentali.

### `scenarios/messages.json`

Contiene i messaggi usati nella simulazione. Ci sono scenari di phishing crypto, messaggi legittimi di controllo e scenari mirati ispirati al caso studio.

### `simulations/run_simulation.py`

È il motore della simulazione. Espande gli archetipi in agenti sintetici, manda ogni coppia agente-messaggio al modello locale, controlla la risposta JSON, normalizza le etichette e salva tutto in CSV.

### `simulations/analyze_latest.py`

Carica l'ultimo CSV generato e stampa metriche aggiornate su `decision`, `flow_outcome`, `compromise_action`, compromissione, controlli sui messaggi legittimi, parse error e warning.

### `analysis.ipynb`

È il notebook di analisi. Carica il CSV più recente dalla cartella `results/`, calcola le metriche, genera tabelle e grafici, e separa i messaggi di phishing dai messaggi legittimi.

---

## Modello degli agenti sintetici

La simulazione parte da una lista di archetipi. Ogni archetipo viene poi espanso in più istanze, così non si ottengono agenti troppo rigidi o identici tra loro.

Di default:

```python
INSTANCES_PER_ARCHETYPE = 6
```

Con 16 archetipi si ottengono:

```text
16 archetipi × 6 istanze = 96 agenti sintetici
```

Con 10 messaggi nello scenario file si arriva a:

```text
96 agenti × 10 messaggi = 960 interazioni
```

Ogni istanza può avere piccole variazioni di età, tratti comportamentali, formazione sulla sicurezza e contesto momentaneo.

---

## Variabili degli agenti

Ogni archetipo può contenere questi campi.

| Campo | Significato |
|---|---|
| `id` | Identificativo interno dell'archetipo |
| `label` | Descrizione leggibile del profilo |
| `age` | Età di base, prima della variazione sulle istanze |
| `age_group` | Fascia d'età |
| `role` | Ruolo o profilo sintetico dell'utente |
| `crypto_experience` | Familiarità con strumenti e servizi crypto |
| `security_training` | Livello di formazione o consapevolezza sulla sicurezza |
| `environment` | Contesto digitale abituale dell'utente |
| `traits` | Tratti comportamentali usati nel prompt |

### Tratti comportamentali

I tratti principali sono:

| Tratto | Significato |
|---|---|
| `impulsiveness` | Tendenza ad agire in fretta senza controllare troppo |
| `trust_in_brands` | Fiducia verso messaggi che sembrano provenire da brand o servizi noti |
| `tech_savvy` | Familiarità generale con tecnologia e strumenti digitali |
| `attention_level` | Capacità/tendenza a notare dettagli e segnali sospetti |
| `risk_aversion` | Prudenza davanti a rischi economici o operativi |

I tratti usano questa scala:

```text
molto_bassa → bassa → media → alta → molto_alta
```

La formazione sulla sicurezza usa invece questa scala:

```text
no → minima → basilare → autodidatta → si
```

Competenza tecnica e consapevolezza di sicurezza non sono la stessa cosa. Un utente può essere bravo con la tecnologia ma comunque vulnerabile alla pressione, alla fretta o a un messaggio molto credibile.

---

## Variazione tra istanze

La funzione `expand_profiles()` crea più versioni dello stesso archetipo. Le istanze possono differire per:

- età;
- impulsività;
- fiducia nei brand;
- competenza tecnologica;
- livello di attenzione;
- avversione al rischio;
- formazione sulla sicurezza;
- situazione personale del momento.

Esempi di situazioni assegnate agli agenti:

- ha poco tempo e legge i messaggi rapidamente;
- ha ricevuto da poco un vero avviso di sicurezza;
- si affida spesso alle notifiche sul telefono;
- prima di agire tende a cercare conferme online;
- usa servizi crypto ma non controlla sempre i dettagli;
- ha già visto tentativi di phishing simili;
- sta facendo più cose contemporaneamente;
- vuole risolvere in fretta problemi legati agli account;
- preferisce chiedere conferma a una persona più esperta;
- si fida molto dei messaggi che sembrano provenire da brand noti.

Queste variazioni servono a rendere gli agenti meno meccanici, senza perdere il controllo metodologico dell'esperimento.

---

## Modello degli scenari

Ogni scenario in `scenarios/messages.json` contiene:

| Campo | Significato |
|---|---|
| `id` | Identificativo dello scenario |
| `type` | `phishing` oppure `legittimo` |
| `channel` | Canale del messaggio, per esempio email, chat, social, mobile o phone_chat |
| `description` | Descrizione breve usata nell'analisi |
| `text` | Testo mostrato all'agente |
| `features` | Caratteristiche dello scenario |

Le feature principali sono:

| Feature | Significato |
|---|---|
| `urgency` | Livello di pressione temporale |
| `personalization` | Quanto il messaggio sembra personalizzato |
| `channel_brand` | Servizio, brand o contesto dichiarato dal messaggio |
| `reward` | Vantaggio promesso o danno evitato |
| `case_study` | Eventuale flag per gli scenari ispirati al caso studio |

Il testo mostrato agli agenti non deve contenere frasi come “scenario sintetico”, “link dimostrativo”, “non reale”, “simulazione” o simili. Queste note sono corrette a livello documentale, ma non devono comparire nel messaggio ricevuto dall'agente, altrimenti il modello viene condizionato verso risposte troppo prudenti.

---

## Domini `.test`

Tutti i link usano domini `.test`. Questo rende gli scenari non operativi e riduce il rischio di includere infrastrutture reali o link utilizzabili.

I domini `.test` servono quindi a mantenere il progetto sicuro, pur conservando una struttura di messaggio simile a quella che un utente potrebbe ricevere.

---

## Decisione guidata dall'LLM

La decisione dell'agente viene presa dall'LLM. Python prepara l'esperimento, vincola lo schema della risposta, valida gli output e salva i risultati, ma non decide con percentuali predefinite quale azione deve compiere l'utente.

La simulazione parte dal presupposto che l'utente abbia gia ricevuto e letto il messaggio. La lettura non e una scelta simulata. La prima scelta simulata e cosa fa dopo la lettura.

Per ogni coppia agente-messaggio, Python costruisce un prompt con:

- profilo dell'agente;
- tratti comportamentali;
- situazione personale del momento;
- testo del messaggio;
- azione di ingresso e azioni di compromissione compatibili con quello scenario;
- regole logiche di coerenza.

Il modello deve rispondere in JSON:

```json
{
  "decision": "...",
  "flow_outcome": "...",
  "compromise_action": "...",
  "motivation": "frase breve"
}
```

Il prompt specifica che il modello non deve comportarsi come un consulente di cybersecurity, ma deve impersonare un utente umano imperfetto. L'etichetta interna dello scenario non viene mostrata al modello.

---

## Decisione dopo la lettura

Le decisioni ammesse sono:

```text
IGNORA
RIMANDA_O_NON_DECIDE
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PROCEDE_CON_LA_RICHIESTA
```

`PROCEDE_CON_LA_RICHIESTA` significa che l'utente entra nel flow richiesto. L'apertura di link, bottone o chat e implicita e non viene trattata come azione finale.

Se la decisione non e `PROCEDE_CON_LA_RICHIESTA`, Python applica regole deterministiche di coerenza:

- `flow_outcome = NON_ENTRA_NEL_FLOW`;
- `compromise_action = NESSUNA`.

Nei messaggi di phishing, un utente che procede puo fermarsi prima della compromissione oppure completare una sola azione compromettente compatibile con lo scenario, per esempio `CONCEDE_ACCESSO_REMOTO`, `COLLEGA_WALLET`, `APPROVA_TRANSAZIONE`, `INVIA_FONDI` o `INSTALLA_APP_O_SOFTWARE`.

`compromised` viene calcolato scenario per scenario:

```python
compromised = (
    message["type"] == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in message.get("possible_compromise_actions", [])
)
```

I messaggi legittimi quindi non possono generare compromissione; se un flow legittimo viene completato, `flow_outcome = AZIONE_LEGITTIMA_COMPLETATA` e `compromise_action = NESSUNA`.

---

## Parametri della simulazione

### Modello Ollama

```python
OLLAMA_MODEL = "qwen3:8b"
```

Il modello locale consigliato è `qwen3:8b`. La richiesta usa `think: false` quando supportato dalla versione locale di Ollama, con fallback per runtime più vecchi.

### Endpoint Ollama

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
```

È l'endpoint locale usato dallo script per comunicare con Ollama.

### Seed generale

```python
RANDOM_SEED = 42
```

`RANDOM_SEED` è la seed generale dell'esperimento. Serve a rendere riproducibile la parte gestita da Python, quindi:

- espansione dei profili;
- variazione dell'età;
- variazione dei tratti;
- assegnazione del background.

Se si cambia `RANDOM_SEED`, si ottiene una versione diversa dell'esperimento, ma comunque riproducibile.

### Seed della singola interazione

Per ogni coppia agente-messaggio lo script calcola una seed specifica:

```python
def make_interaction_seed(agent_id: str, message_id: str) -> int:
    key = f"{RANDOM_SEED}|{agent_id}|{message_id}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:8], 16)
```

Questa funzione evita che tutte le chiamate al modello usino la stessa identica seed, ma mantiene la simulazione riproducibile.

In pratica:

```text
RANDOM_SEED = seed dell'esperimento intero
interaction_seed = seed della singola coppia agente-messaggio
```

L'unica seed da impostare manualmente è `RANDOM_SEED`. La `interaction_seed` viene calcolata automaticamente.

### Temperature

```python
TEMPERATURE = 0.3
```

La temperature è volutamente bassa: la simulazione deve essere più stabile che creativa.

### Modalità JSON

La richiesta a Ollama prova prima uno schema JSON per `decision`, `flow_outcome`, `compromise_action` e `motivation`. Se la versione locale di Ollama non supporta lo schema, lo script usa il fallback a JSON semplice e mantiene comunque la validazione Python.

---

## CSV di output

Ogni riga del CSV rappresenta una singola interazione tra un agente sintetico e uno scenario.

Le colonne principali sono:

| Colonna | Significato |
|---|---|
| `run_id` | Identificativo temporale della simulazione |
| `model` | Modello Ollama usato |
| `temperature` | Temperature usata per la run |
| `random_seed` | Seed generale dell'esperimento |
| `interaction_seed` | Seed stabile della specifica interazione agente-messaggio |
| `agent_id` | Identificativo dell'agente sintetico |
| `age` | Età dopo la variazione |
| `age_group` | Fascia d'età |
| `role` | Ruolo/profilo dell'agente |
| `crypto_experience` | Esperienza crypto |
| `security_training` | Formazione sulla sicurezza |
| `environment` | Contesto digitale abituale |
| `background` | Situazione momentanea assegnata all'agente |
| `impulsiveness` | Impulsività |
| `trust_in_brands` | Fiducia nei brand |
| `tech_savvy` | Competenza tecnologica |
| `attention_level` | Livello di attenzione |
| `risk_aversion` | Avversione al rischio |
| `message_id` | Identificativo dello scenario |
| `message_type` | `phishing` o `legittimo` |
| `channel` | Canale del messaggio |
| `scenario_description` | Descrizione dello scenario |
| `urgency` | Urgenza del messaggio |
| `personalization` | Personalizzazione del messaggio |
| `reward` | Ricompensa promessa o danno evitato |
| `raw_decision` | Decisione grezza prodotta dal modello |
| `decision` | Decisione dopo la lettura, normalizzata |
| `raw_flow_outcome` | Esito del flow grezzo prodotto dal modello |
| `flow_outcome` | Esito normalizzato del flow |
| `raw_compromise_action` | Azione di compromissione grezza prodotta dal modello |
| `compromise_action` | Azione di compromissione normalizzata, oppure `NESSUNA` |
| `entered_flow` | `True` se l'utente segue la richiesta del messaggio |
| `stopped_before_compromise` | `True` se entra nel flow ma si ferma prima della compromissione |
| `raw_initial_reaction` | Alias retrocompatibile di `raw_decision` |
| `initial_reaction` | Alias retrocompatibile di `decision` |
| `raw_final_action` | Alias retrocompatibile di `raw_compromise_action` |
| `final_action` | Alias retrocompatibile di `compromise_action` |
| `engaged` | Alias retrocompatibile di `entered_flow` |
| `compromised` | `True` solo per phishing con compromissione completata e coerente con lo scenario |
| `reported` | `True` se l'agente segnala il messaggio |
| `verified` | `True` se l'agente verifica tramite canali affidabili |
| `ignored` | `True` se l'agente ignora il messaggio |
| `delayed` | `True` se l'agente rimanda o non decide |
| `false_positive_report` | `True` se un messaggio legittimo viene segnalato come phishing |
| `legitimate_completion` | `True` se una richiesta legittima viene completata |
| `parse_error` | `True` se c'è stato un errore di parsing o validazione |
| `validation_error` | Motivo dell'errore di parsing/validazione |
| `motivation` | Motivazione sintetica generata dal modello |
| `raw_response` | Risposta grezza del modello |
| `raw_specific_action` | Alias retrocompatibile di `raw_compromise_action` |
| `specific_action` | Alias retrocompatibile di `compromise_action` |
| `proceeded` | Alias retrocompatibile di `entered_flow` |

---

## Metriche calcolate nell'analisi

Il notebook oppure `simulations/analyze_latest.py` possono calcolare diverse metriche, tra cui:

| Metrica | Significato |
|---|---|
| Distribuzione decisioni | Distribuzione delle decisioni dopo la lettura |
| Distribuzione flow outcome | Distribuzione degli esiti del flow |
| Distribuzione compromise action | Distribuzione delle azioni di compromissione completate |
| Entered flow rate | Percentuale di casi in cui l'utente segue la richiesta |
| Stopped before compromise rate | Percentuale di casi in cui entra nel flow ma si ferma prima della compromissione |
| Compromissione sui phishing | Percentuale di phishing con compromissione completata e coerente con lo scenario |
| Controllo legittimi | Verifica che i messaggi legittimi non producano compromissione |
| Tasso di segnalazione | Percentuale di messaggi segnalati come phishing |
| Tasso di verifica | Percentuale di messaggi verificati tramite canali affidabili |
| Completamento legittimo | Percentuale di messaggi legittimi completati normalmente |
| Falsi positivi | Percentuale di messaggi legittimi segnalati come phishing |

L'analisi separa sempre i messaggi di phishing dai messaggi legittimi.

---

## Scenari ispirati al caso studio

Il repository include scenari ispirati al caso studio discusso nella tesi. Questi scenari riguardano:

- finti operatori di supporto;
- avvisi di account compromesso;
- pressione temporale;
- richiesta di accesso remoto;
- verifica di wallet/dispositivo;
- profili ad alto valore nel mondo crypto.

Gli scenari sono sintetici e non operativi. Non sono copie letterali di comunicazioni reali degli attaccanti.

---

## Installazione

### 1. Clonare il repository

```bash
git clone https://github.com/leocop03/crypto-phishing-simulation-thesis.git
cd crypto-phishing-simulation-thesis
```

### 2. Creare e attivare l'ambiente virtuale

Su Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Su macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installare le dipendenze Python

```bash
pip install -r requirements.txt
```

### 4. Installare e avviare Ollama

Dopo aver installato Ollama, scarica il modello:

```bash
ollama pull qwen3:8b
```

Avvia Ollama se non è già attivo:

```bash
ollama serve
```

In un altro terminale puoi controllare il modello caricato con:

```bash
ollama ps
```

---

## Eseguire la simulazione

Dalla cartella principale del repository:

```bash
python simulations/run_simulation.py
```

Opzioni utili per test brevi:

```bash
python simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 100
```

Ogni esecuzione crea un nuovo file CSV:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

Le simulazioni precedenti non vengono sovrascritte, perché il nome del file contiene data e ora.

La cartella `results/` è ignorata da Git, così i risultati locali non vengono pubblicati per errore.

---

## Eseguire l'analisi

Avvia Jupyter:

```bash
jupyter lab
```

Apri:

```text
analysis.ipynb
```

Esegui tutte le celle, oppure usa l'analisi leggera da terminale:

```bash
python simulations/analyze_latest.py
```

Entrambi caricano il CSV più recente da `results/` e calcolano le metriche aggiornate su decisioni e azioni specifiche.

---

## Riproducibilità

Per ottenere risultati il più possibile confrontabili, bisogna mantenere invariati:

- stessa versione del repository;
- stesso `RANDOM_SEED`;
- stessa `TEMPERATURE`;
- stesso modello Ollama;
- stessa versione/runtime di Ollama;
- stessi file degli archetipi e degli scenari.

Anche con seed fisse, piccole differenze possono comparire se cambiano modello, versione di Ollama o ambiente di esecuzione. È un limite normale degli esperimenti basati su LLM locali.

---

## Prestazioni

Il tempo di esecuzione dipende soprattutto da:

- numero di agenti;
- numero di scenari;
- dimensione del modello;
- lunghezza del prompt;
- uso di CPU/GPU;
- configurazione di Ollama.

La configurazione di default produce 960 chiamate al modello. Su hardware consumer può richiedere parecchio tempo. Usa `--limit` per mini-run durante i test di prompt e validazione.

---

## Pulizia del repository

Il `.gitignore` esclude volutamente:

- `.venv/`;
- `__pycache__/`;
- `.ipynb_checkpoints/`;
- `results/`;
- file `.csv` generati;
- file `.env`.

In questo modo il repository pubblico rimane concentrato su codice, scenari, documentazione e notebook di analisi, senza includere artefatti locali o file inutili.

---

## Limiti etici e metodologici

Il progetto ha diversi limiti importanti:

1. Gli agenti sintetici non sono persone reali.
2. Gli LLM possono avere un forte bias verso risposte prudenti o “da manuale”.
3. Il modo in cui è scritto il prompt influenza molto i risultati.
4. Modelli diversi possono produrre comportamenti diversi.
5. La simulazione non è statisticamente rappresentativa.
6. I domini `.test` sono sicuri, ma potrebbero comunque influenzare la percezione del modello.
7. Gli scenari del caso studio sono approssimazioni sintetiche, non ricostruzioni esatte.
8. I risultati non devono essere usati per dichiarare percentuali reali di successo del phishing.

Per questi motivi, i risultati vanno discussi come simulazione esplorativa e confronto tra condizioni, non come misurazione empirica del comportamento umano reale.

---

## Come interpretare i risultati

La domanda corretta non è:

> questa percentuale rappresenta davvero il mondo reale?

La domanda più sensata è:

> con questo prompt, questo modello e questi scenari, come si distribuiscono le reazioni degli agenti sintetici tra profili e tecniche diverse?

Il valore del progetto sta nel confronto tra scenari, nell'osservazione dei limiti del modello e nella discussione metodologica su quanto sia difficile simulare il comportamento umano in cybersecurity tramite LLM.

---

## Contesto accademico

Il progetto è stato sviluppato come parte di una tesi triennale in Cybersecurity. Integra:

- analisi della social engineering;
- sicurezza nel mondo crypto;
- simulazione con agenti sintetici;
- sperimentazione locale con LLM;
- analisi dei risultati tramite notebook.

---

## Licenza e riuso

Al momento il repository non contiene una licenza open source esplicita, salvo aggiunta futura. In assenza di licenza, il riuso è limitato dalle regole ordinarie del diritto d'autore. Il progetto è condiviso per revisione accademica, trasparenza e discussione educativa.
