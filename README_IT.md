# Simulazione di phishing crypto per tesi

Questo repository contiene un framework locale basato su LLM per simulare come archetipi sintetici di utenti reagiscono a messaggi crypto fraudolenti e legittimi.

Il progetto è pensato per una tesi accademica in ambito cybersecurity. Non è uno strumento di phishing e non misura tassi reali di successo degli attacchi.

## Scopo del progetto

L'obiettivo è esplorare, in modo controllato e riproducibile, come profili sintetici diversi potrebbero reagire dopo aver letto messaggi crypto.

La simulazione permette di confrontare:

- archetipi con diversi livelli di consapevolezza di sicurezza, competenza tecnica, esperienza crypto, impulsività, attenzione, fiducia e avversione al rischio;
- scenari di phishing basati su tecniche diverse di social engineering;
- messaggi legittimi usati come controllo;
- esiti comportamentali come verifica, segnalazione, ingresso nel flow, arresto prima della compromissione e completamento dell'azione compromettente.

I risultati devono essere interpretati come output esplorativi di una simulazione, non come dati empirici su utenti reali.

## Ambito etico e di sicurezza

Il repository è pensato solo per finalità difensive, educative e accademiche.

Limiti di sicurezza:

- tutti gli scenari sono sintetici;
- i domini usano valori sicuri o di test, come `.test`;
- non viene creata alcuna infrastruttura reale di phishing;
- non vengono contattati utenti reali;
- non vengono raccolte credenziali, dati wallet, seed phrase o fondi;
- non vengono fornite istruzioni operative per condurre phishing reale;
- gli output sono simulati e non devono essere interpretati come tassi reali di successo degli attacchi.

## Struttura del repository

```text
agents/
  profiles_archetypes.json      Archetipi sintetici di utenti

scenarios/
  messages.json                 Messaggi sintetici phishing e legittimi

simulations/
  run_simulation.py             Script principale della simulazione
  analyze_latest.py             Analisi terminale degli ultimi CSV generati

results/
  sim_*.csv                     Output generati localmente, ignorati da Git

analysis.ipynb                  Notebook opzionale per l'analisi
README.md                       Documentazione in inglese
README_IT.md                    Documentazione in italiano
requirements.txt                Dipendenze Python
```

## Disegno della simulazione

La simulazione si basa su tre componenti principali:

1. **Agenti sintetici**: archetipi di utenti con attributi comportamentali e contestuali.
2. **Messaggi sintetici**: scenari crypto fraudolenti e legittimi.
3. **Modello LLM locale**: il modello interpreta ogni archetipo e produce una decisione comportamentale strutturata.

L'utente è considerato già esposto al messaggio e lo ha già letto. La lettura del messaggio non è una scelta simulata. La prima scelta modellata è la reazione comportamentale dopo la lettura.

La simulazione usa una struttura comportamentale a due livelli:

1. **Decisione iniziale** dopo la lettura.
2. **Esito del flow** se l'utente decide di procedere con la richiesta del messaggio.

L'etichetta interna `message_type` viene usata dal codice per validazione e analisi, ma non viene mostrata al modello come informazione esplicita per decidere.

## Dimensione della simulazione completa

La run completa predefinita produce 960 interazioni simulate:

```text
16 archetipi × 6 istanze per archetipo = 96 agenti sintetici
96 agenti sintetici × 10 messaggi = 960 interazioni
```

Ogni riga del CSV rappresenta una singola interazione tra un agente sintetico e un messaggio.

## Schema decisionale

### `decision`

Decisione comportamentale di primo livello dopo la lettura del messaggio.

Valori ammessi:

- `IGNORA`: l'utente ignora il messaggio.
- `RIMANDA_O_NON_DECIDE`: l'utente rimanda o non agisce subito.
- `VERIFICA_TRAMITE_CANALE_UFFICIALE`: l'utente controlla tramite un canale ufficiale indipendente.
- `SEGNALA_COME_PHISHING`: l'utente segnala o marca il messaggio come sospetto.
- `PROCEDE_CON_LA_RICHIESTA`: l'utente entra nel flow proposto dal messaggio.

### `flow_outcome`

Esito comportamentale dopo la decisione iniziale.

Valori ammessi:

- `NON_ENTRA_NEL_FLOW`: l'utente non entra nel flow richiesto.
- `SI_FERMA_PRIMA_DELLA_COMPROMISSIONE`: l'utente entra nel flow ma si ferma prima dell'azione finale compromettente.
- `COMPROMISSIONE_COMPLETATA`: l'utente completa un'azione compromettente compatibile con lo scenario.
- `AZIONE_LEGITTIMA_COMPLETATA`: l'utente completa una richiesta legittima.

### `compromise_action`

Azione concreta di compromissione, se la compromissione viene completata.

Valori ammessi:

- `NESSUNA`
- `INSERISCE_CREDENZIALI`
- `INSERISCE_DATI_KYC`
- `INSERISCE_SEED_PHRASE`
- `COLLEGA_WALLET`
- `APPROVA_TRANSAZIONE`
- `CONCEDE_ACCESSO_REMOTO`
- `INVIA_FONDI`
- `INSTALLA_APP_O_SOFTWARE`

`compromise_action` è specifica per scenario. Una compromissione completata è valida solo se l'azione appartiene alle `possible_compromise_actions` previste da quello scenario.

## Calcolo della compromissione

La simulazione non usa una lista globale di azioni rischiose per decidere se l'utente è compromesso.

La compromissione viene calcolata con una compatibilità a livello di scenario:

```python
compromised = (
    message_type == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in possible_compromise_actions
)
```

Questo significa che:

- i messaggi legittimi non possono produrre `compromised = True`;
- entrare nel flow non equivale automaticamente a essere compromessi;
- l'arresto prima della compromissione viene tracciato separatamente;
- per avere compromissione servono messaggio phishing, flow completato e azione finale compatibile con lo scenario.

## Modello usato

Configurazione consigliata:

- Modello: `qwen3:8b` tramite Ollama.
- Temperatura: `0.3`.
- Output: JSON strutturato quando disponibile, con fallback a JSON mode.
- Validazione: gli output del modello vengono normalizzati, validati e ritentati una volta se non validi.

L'uso di un modello locale permette di eseguire molte simulazioni senza costi API e con maggiore controllo sull'ambiente sperimentale.

## Installazione

Da Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Assicurarsi che Ollama sia in esecuzione e che il modello scelto sia disponibile:

```powershell
ollama pull qwen3:8b
```

## Come eseguire

Run breve bilanciata, utile per testare prompt e schema:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Run completa:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analisi dell'ultimo CSV generato:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## Opzioni CLI

Opzioni implementate:

- `--model`: nome del modello Ollama.
- `--temperature`: temperatura del modello.
- `--instances`: numero di istanze generate per ogni archetipo.
- `--limit`: numero massimo di interazioni da eseguire.
- `--seed`: seed globale della simulazione.
- `--balanced`: se usato con `--limit`, distribuisce le interazioni tra gli scenari.

## Output

I CSV generati vengono salvati in `results/` con nome `sim_*.csv`.

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

Il CSV può contenere anche metadati della run, attributi degli agenti, caratteristiche dei messaggi e alias retrocompatibili per vecchi notebook di analisi.

## Analisi dei risultati

`simulations/analyze_latest.py` carica l'ultimo CSV in `results/`, oppure un CSV selezionato se supportato dallo script, e stampa un riepilogo da terminale.

L'analisi include:

- numero di righe, modello e temperatura;
- tasso di parse error e validation error;
- distribuzione di `decision`;
- distribuzione di `flow_outcome`;
- distribuzione di `compromise_action`;
- tasso di ingresso nel flow;
- tasso di arresto prima della compromissione;
- tasso di compromissione sui soli messaggi phishing;
- controllo sui messaggi legittimi;
- tassi di verifica, segnalazione, ignorati, rimandati e completamenti legittimi;
- risultati per scenario;
- risultati per archetipo;
- eventuali warning metodologici.

I warning sono controlli metodologici, non obiettivi da forzare tramite prompt.

## Limiti metodologici

Il progetto va interpretato con cautela.

Principali limiti:

- gli LLM possono avere bias prudenziali o legati all'allineamento;
- gli utenti sintetici non sono utenti reali;
- i risultati dipendono da modello, prompt, temperatura, regole di validazione e disegno degli scenari;
- le percentuali prodotte sono output simulati, non probabilità reali;
- il modello può sovrautilizzare la verifica o l'arresto prima della compromissione;
- il modello può sottorappresentare la segnalazione del phishing;
- run ripetute possono variare anche con temperatura bassa;
- il framework è esplorativo e va discusso come simulazione, non come misurazione di popolazioni reali.

## Workflow consigliato

1. Eseguire una mini-run bilanciata.
2. Controllare l'output di analisi.
3. Verificare parse error, validation error, vecchie label e compromissioni sui messaggi legittimi.
4. Eseguire la run completa solo dopo aver verificato che schema e prompt si comportino correttamente.
5. Confrontare versioni diverse di prompt o modello se utile.
6. Discutere nella tesi sia i risultati sia i limiti del modello.

## Possibile inserimento nella tesi

Il progetto può essere inserito come:

- breve capitolo sperimentale;
- prototipo metodologico;
- appendice a supporto di una tesi più ampia sul phishing crypto e sul social engineering.

Non deve sostituire dati empirici su utenti reali. Il suo valore è metodologico: formalizza una catena decisionale del phishing e permette di confrontare in modo controllato profili sintetici e scenari.
