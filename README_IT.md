# Simulazione di phishing crypto

Framework locale basato su LLM per simulare il comportamento di profili sintetici davanti a messaggi di phishing crypto e messaggi legittimi.

Il progetto gira localmente tramite Ollama. Python gestisce la generazione degli agenti, la costruzione dei prompt, la validazione JSON, la normalizzazione dei risultati e l'esportazione in CSV. Il modello linguistico viene usato come componente decisionale comportamentale.

## Ambito

Il repository è pensato per ricerca, formazione e analisi difensiva in ambito cybersecurity.

Il progetto non esegue phishing reale, non contatta utenti reali, non raccoglie credenziali, non interagisce con wallet e non crea infrastruttura offensiva. Tutti gli scenari sono sintetici e usano domini sicuri `.test`.

I risultati sono esplorativi. Non devono essere interpretati come tassi reali di successo del phishing o come misurazioni del comportamento di utenti reali.

## Struttura del repository

```text
crypto-phishing-simulation-thesis/
├── agents/
│   └── profiles_archetypes.json
├── scenarios/
│   └── messages.json
├── simulations/
│   ├── run_simulation.py
│   └── analyze_latest.py
├── results/              # generata localmente, ignorata da Git
├── analysis.ipynb
├── requirements.txt
├── README.md
└── README_IT.md
```

## Disegno della simulazione

La simulazione combina archetipi sintetici di utenti con messaggi legati al mondo crypto.

La configurazione completa predefinita usa:

```text
16 archetipi × 6 istanze per archetipo = 96 agenti sintetici
96 agenti × 10 messaggi = 960 interazioni simulate
```

Ogni agente riceve lo stesso insieme di messaggi. Per ogni coppia agente-messaggio, il modello restituisce una decisione strutturata in formato JSON.

Si assume che l'utente abbia già ricevuto e letto il messaggio. La lettura non è una scelta simulata. La simulazione parte dalla reazione successiva alla lettura.

## Modello decisionale

Ogni interazione è rappresentata da tre campi principali.

### `decision`

Reazione comportamentale iniziale dopo la lettura:

```text
IGNORA
RIMANDA_O_NON_DECIDE
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PROCEDE_CON_LA_RICHIESTA
```

`PROCEDE_CON_LA_RICHIESTA` significa che l'agente entra nel flow proposto dal messaggio. L'apertura di un link, pulsante o chat è implicita e non viene salvata come azione finale.

### `flow_outcome`

Esito del flow:

```text
NON_ENTRA_NEL_FLOW
SI_FERMA_PRIMA_DELLA_COMPROMISSIONE
COMPROMISSIONE_COMPLETATA
AZIONE_LEGITTIMA_COMPLETATA
```

Entrare nel flow non significa automaticamente essere compromessi. Un agente può procedere inizialmente e poi fermarsi prima di completare un'azione dannosa.

### `compromise_action`

Azione finale di compromissione, quando presente:

```text
NESSUNA
INSERISCE_CREDENZIALI
INSERISCE_DATI_KYC
INSERISCE_SEED_PHRASE
COLLEGA_WALLET
APPROVA_TRANSAZIONE
CONCEDE_ACCESSO_REMOTO
INVIA_FONDI
INSTALLA_APP_O_SOFTWARE
```

Le azioni di compromissione sono specifiche dello scenario. Per esempio, un giveaway può prevedere `INVIA_FONDI`, mentre una falsa migrazione wallet può prevedere `COLLEGA_WALLET` o `APPROVA_TRANSAZIONE`.

## Calcolo della compromissione

Una riga viene marcata come compromessa solo se tutte queste condizioni sono vere:

```python
compromised = (
    message_type == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in possible_compromise_actions
)
```

I messaggi legittimi non possono produrre `compromised = True`. Se un agente completa un flow legittimo, l'esito viene salvato come `AZIONE_LEGITTIMA_COMPLETATA` con `compromise_action = NESSUNA`.

## Configurazione del modello

Modello locale consigliato:

```text
qwen3:8b
```

Temperatura predefinita:

```text
0.3
```

Lo script usa output JSON strutturato quando disponibile e passa al JSON mode semplice quando necessario. Le risposte vengono validate in Python. Le risposte non valide vengono ritentate una volta prima di essere salvate come errori di parsing o validazione.

## Installazione

Installa e avvia Ollama, poi scarica il modello:

```powershell
ollama pull qwen3:8b
```

Crea e attiva un ambiente virtuale Python:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Esecuzione

Run di test bilanciata:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Run completa:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analisi dell'ultimo file generato:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## Opzioni CLI

```text
--model          nome del modello Ollama
--temperature    temperatura del modello
--instances      istanze generate per archetipo
--limit          numero massimo di interazioni da eseguire
--seed           seed dell'esperimento lato Python
--balanced       distribuisce le run limitate tra gli scenari
```

## Output

I risultati vengono salvati come file CSV nella cartella `results/`.

Colonne principali:

```text
agent_id
archetype_id
message_id
message_type
decision
flow_outcome
compromise_action
entered_flow
stopped_before_compromise
compromised
verified
reported
ignored
delayed
legitimate_completion
parse_error
validation_error
motivation
raw_response
```

## Analisi

`simulations/analyze_latest.py` carica il CSV più recente dalla cartella `results/` e stampa:

- numero di righe e metadati del modello;
- tasso di errori di parsing e validazione;
- distribuzione delle decisioni;
- distribuzione degli esiti del flow;
- distribuzione delle azioni di compromissione;
- tasso di compromissione sui messaggi phishing;
- controlli sui messaggi legittimi;
- risultati per scenario;
- risultati per archetipo;
- avvisi metodologici.

Il notebook `analysis.ipynb` può essere usato per analisi più approfondite, tabelle e grafici.

## Note metodologiche

Questo framework è una simulazione controllata, non uno studio empirico su utenti reali.

Limiti principali:

- gli agenti sintetici non sono utenti reali;
- gli output dipendono dal modello, dal prompt, dalla temperatura e dal disegno degli scenari;
- i modelli locali possono avere bias prudenziali o di coerenza;
- le percentuali simulate vanno interpretate in modo comparativo, non come probabilità reali;
- la formulazione degli scenari può influenzare il comportamento del modello;
- i risultati vanno discussi insieme all'ispezione qualitativa delle motivazioni e delle risposte raw.

## Workflow consigliato

1. Eseguire una mini-run bilanciata.
2. Controllare l'output di `analyze_latest.py`.
3. Verificare errori di parsing, errori di validazione e comportamento dei messaggi legittimi.
4. Eseguire la run completa solo quando la struttura è stabile.
5. Confrontare versioni diverse di modello o prompt, se necessario.
