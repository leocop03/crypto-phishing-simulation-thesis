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
- la differenza tra aprire un messaggio/link e compiere un'azione davvero pericolosa;
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
│   └── run_simulation.py
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

La decisione dell'agente viene presa dall'LLM. Python non sceglie con percentuali predefinite se un utente ignora, apre, verifica, segnala o procede con un'azione operativa.

Per ogni coppia agente-messaggio, Python costruisce un prompt con:

- profilo dell'agente;
- tratti comportamentali;
- situazione personale del momento;
- testo del messaggio;
- reazioni iniziali ammesse;
- azioni finali ammesse;
- regole logiche di coerenza.

Il modello deve rispondere in JSON:

```json
{
  "initial_reaction": "...",
  "final_action": "...",
  "motivation": "..."
}
```

Il prompt specifica che il modello non deve comportarsi come un consulente di cybersecurity, ma deve impersonare un utente umano imperfetto. Questo è importante perché molti LLM tendono spontaneamente a dare risposte molto sicure e razionali, anche quando si sta chiedendo loro di simulare un comportamento umano sotto pressione.

---

## Risposta a due livelli

La simulazione separa la prima reazione dall'esito finale.

Questa distinzione è fondamentale: aprire un messaggio o un link non significa automaticamente compromettere account, wallet, dispositivo o fondi.

### Reazioni iniziali

```text
IGNORA
APRE_MESSAGGIO_O_LINK
SEGNALA_SUBITO
VERIFICA_SUBITO
PARSE_ERROR
```

| Reazione iniziale | Significato |
|---|---|
| `IGNORA` | L'agente ignora il messaggio |
| `APRE_MESSAGGIO_O_LINK` | L'agente apre il messaggio o il link; da sola non è una compromissione |
| `SEGNALA_SUBITO` | L'agente segnala subito il messaggio |
| `VERIFICA_SUBITO` | L'agente verifica tramite canali affidabili prima di procedere |
| `PARSE_ERROR` | Errore tecnico di parsing o validazione |

### Azioni finali

```text
NESSUNA_AZIONE_ULTERIORE
COLLEGA_WALLET_O_APPROVA_TRANSAZIONE
INSERISCE_CREDENZIALI_O_SEED
CONCEDE_ACCESSO_REMOTO
INVIA_FONDI
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PARSE_ERROR
```

| Azione finale | Significato |
|---|---|
| `NESSUNA_AZIONE_ULTERIORE` | L'agente non fa altro dopo la prima reazione |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | Collega un wallet o approva una transazione/firma |
| `INSERISCE_CREDENZIALI_O_SEED` | Inserisce credenziali, codici OTP, chiavi private o seed phrase |
| `CONCEDE_ACCESSO_REMOTO` | Concede accesso remoto o condivisione schermo |
| `INVIA_FONDI` | Invia criptovalute |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | Verifica tramite canali affidabili o ufficiali |
| `SEGNALA_COME_PHISHING` | Segnala il messaggio come phishing |
| `PARSE_ERROR` | Errore tecnico di parsing o validazione |

### Regole di coerenza

Dopo la risposta del modello, lo script applica alcune regole di coerenza:

- se `initial_reaction` è `IGNORA`, allora `final_action` diventa `NESSUNA_AZIONE_ULTERIORE`;
- se `initial_reaction` è `SEGNALA_SUBITO`, allora `final_action` diventa `SEGNALA_COME_PHISHING`;
- se `initial_reaction` è `VERIFICA_SUBITO`, allora `final_action` diventa `VERIFICA_TRAMITE_CANALE_UFFICIALE`.

Questa normalizzazione evita combinazioni incoerenti, ma non trasforma Python nel decisore comportamentale.

---

## Parametri della simulazione

### Modello Ollama

```python
OLLAMA_MODEL = "llama3.2:3b"
```

Il progetto usa un modello locale tramite Ollama. `llama3.2:3b` è una scelta pratica perché permette di eseguire molte interazioni in tempi ragionevoli anche su hardware consumer.

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
TEMPERATURE = 0.7
```

La temperature controlla quanto il modello può variare le sue risposte.

Valori più bassi rendono le risposte più deterministiche e ripetitive. Valori più alti aumentano la varietà, ma possono ridurre la coerenza. Il valore `0.7` cerca un equilibrio: abbastanza variabilità da simulare comportamenti diversi, ma senza rendere le risposte troppo instabili.

### Modalità JSON

La richiesta a Ollama usa:

```python
"format": "json"
```

Questo aiuta il modello a restituire risposte strutturate e riduce gli errori di parsing.

---

## CSV di output

Ogni riga del CSV rappresenta una singola interazione tra un agente sintetico e uno scenario.

Le colonne principali sono:

| Colonna | Significato |
|---|---|
| `run_id` | Identificativo temporale della simulazione |
| `model` | Modello Ollama usato |
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
| `raw_initial_reaction` | Reazione iniziale grezza prodotta dal modello |
| `initial_reaction` | Reazione iniziale normalizzata |
| `raw_final_action` | Azione finale grezza prodotta dal modello |
| `final_action` | Azione finale normalizzata |
| `engaged` | `True` se l'agente non ha semplicemente ignorato il messaggio |
| `compromised` | `True` se l'azione finale espone fondi, account, wallet o dispositivo |
| `reported` | `True` se l'agente segnala il messaggio |
| `verified` | `True` se l'agente verifica tramite canali affidabili |
| `parse_error` | `True` se c'è stato un errore di parsing o validazione |
| `motivation` | Motivazione sintetica generata dal modello |
| `raw_response` | Risposta grezza del modello |

---

## Metriche calcolate nel notebook

Il notebook calcola diverse metriche, tra cui:

| Metrica | Significato |
|---|---|
| Tasso di interazione | Percentuale di messaggi phishing non ignorati |
| Tasso di apertura/click | Percentuale di messaggi phishing aperti/cliccati |
| Tasso di collegamento wallet/approvazione transazione | Percentuale di casi in cui l'agente collega il wallet o approva una transazione |
| Tasso di inserimento credenziali/seed | Percentuale di casi in cui vengono inserite credenziali, seed o informazioni sensibili |
| Tasso di accesso remoto | Percentuale di casi in cui viene concesso accesso remoto o condivisione schermo |
| Tasso di invio fondi | Percentuale di casi in cui vengono inviate criptovalute |
| Tasso di azione compromettente | Percentuale di casi con un'azione finale chiaramente pericolosa |
| Tasso di fallimento ampio | Misura più larga che include apertura/click e azioni compromettenti |
| Tasso di segnalazione | Percentuale di messaggi segnalati come phishing |
| Tasso di verifica | Percentuale di messaggi verificati tramite canali affidabili |
| Tasso di interazione legittima | Percentuale di messaggi legittimi gestiti tramite apertura normale o verifica |
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
ollama pull llama3.2:3b
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

Esegui tutte le celle. Il notebook carica il CSV più recente da `results/`, calcola le metriche, mostra tabelle e grafici, ed esporta i risultati nella cartella dei risultati.

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

La configurazione di default produce 960 chiamate al modello. Su hardware consumer può richiedere parecchio tempo. Modelli più piccoli, come `llama3.2:3b`, sono generalmente più veloci dei modelli più grandi.

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
