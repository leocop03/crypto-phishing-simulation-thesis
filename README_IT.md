# Simulazione di Phishing Crypto per Tesi

Questo repository contiene la componente sperimentale di una tesi triennale in Cybersecurity dedicata al phishing, all'ingegneria sociale e alle frodi legate al mondo delle criptovalute.

Il progetto implementa una **simulazione agent-based controllata**, nella quale profili utente sintetici interagiscono con messaggi di phishing e messaggi legittimi relativi all'ecosistema crypto. L'obiettivo è analizzare come caratteristiche dell'utente, proprietà del messaggio e livello di consapevolezza sulla sicurezza possano influenzare comportamenti rischiosi o difensivi.

> **Importante:** questo progetto è destinato esclusivamente a finalità didattiche, accademiche e di ricerca.  
> Non esegue campagne di phishing reali, non raccoglie credenziali e non interagisce con utenti reali o infrastrutture malevole reali.

---

## Contesto della tesi

La tesi analizza il rapporto tra criptovalute e attacchi di ingegneria sociale, con particolare attenzione al modo in cui vulnerabilità umane e comportamentali possono essere sfruttate in ambienti blockchain e crypto.

Sebbene i sistemi blockchain siano spesso robusti dal punto di vista tecnico, molti attacchi di successo non violano direttamente il protocollo sottostante. Al contrario, sfruttano utenti, canali di comunicazione, relazioni di fiducia, scarsa consapevolezza della sicurezza ed errori operativi.

Questo repository supporta la parte sperimentale della tesi, fornendo un framework riproducibile per simulare la reazione di utenti sintetici a diversi scenari di phishing.

---

## Obiettivo della ricerca

L'obiettivo principale del progetto è costruire un ambiente di simulazione controllato per studiare:

- come profili utente sintetici differenti reagiscono a tentativi di phishing;
- come caratteristiche del messaggio, quali urgenza, promessa di ricompensa, impersonificazione o linguaggio tecnico, influenzano il comportamento;
- come formazione sulla sicurezza ed esperienza nel mondo crypto incidono sulle decisioni simulate;
- come le risposte ai messaggi di phishing differiscono dalle risposte ai messaggi legittimi;
- come agenti basati su LLM possano essere usati come strumento esplorativo nella ricerca comportamentale in cybersecurity.

La simulazione **non** ha lo scopo di stimare il tasso reale di vulnerabilità degli utenti al phishing. È invece pensata come framework esplorativo per confrontare pattern comportamentali tra profili e scenari diversi.

---

## Nota metodologica

Gli agenti usati in questo progetto sono profili sintetici generati a partire da archetipi predefiniti. Non sono utenti reali e non rappresentano un campione statisticamente valido della popolazione.

Di conseguenza, i risultati non devono essere interpretati come misurazioni dirette del comportamento umano reale. L'esperimento è utile per osservare differenze relative tra scenari, archetipi utente e caratteristiche dei messaggi in condizioni controllate.

La simulazione distingue diversi livelli di interazione, tra cui:

- ignorare un messaggio;
- aprire un link;
- verificare il messaggio tramite un canale ufficiale;
- segnalare un messaggio come phishing;
- collegare un wallet o approvare una transazione;
- inserire credenziali o seed phrase;
- inviare fondi.

Questa distinzione è importante perché aprire un link non implica necessariamente una compromissione completa. Nelle campagne di phishing reali, la compromissione avviene di solito solo dopo ulteriori azioni rischiose, come l'inserimento di credenziali, l'approvazione di una transazione malevola, la condivisione di una seed phrase, l'installazione di malware o l'invio di fondi.

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
│   └── generata localmente, ignorata da Git
│
├── analysis.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Componenti del progetto

### `agents/`

Contiene gli archetipi utente sintetici usati nella simulazione. Ogni archetipo descrive un profilo attraverso variabili come:

- età;
- fascia d'età;
- ruolo;
- esperienza con le criptovalute;
- formazione sulla sicurezza;
- ambiente d'uso tipico;
- impulsività;
- fiducia nei brand;
- competenza tecnica;
- livello di attenzione;
- avversione al rischio.

La simulazione espande ciascun archetipo in più agenti sintetici applicando piccole variazioni controllate.

### `scenarios/`

Contiene template di messaggi di phishing e messaggi legittimi. Ogni scenario include:

- identificativo del messaggio;
- tipo di messaggio;
- canale di comunicazione;
- contenuto testuale;
- livello di urgenza;
- livello di personalizzazione;
- livello di ricompensa promessa.

Tutti gli scenari sono sintetici. Gli URL potenzialmente sospetti usano domini sicuri `.test`, in modo da non fare riferimento a infrastrutture malevole reali.

### `simulations/`

Contiene lo script principale della simulazione. Lo script:

1. carica gli archetipi utente;
2. li espande in agenti sintetici;
3. carica gli scenari;
4. invia ogni coppia agente-messaggio a un LLM locale tramite Ollama;
5. effettua parsing e normalizzazione della risposta del modello;
6. salva i risultati in un file CSV.

### `analysis.ipynb`

Contiene il workflow di analisi dei dati generati. Il notebook calcola metriche come:

- tasso di apertura dei link nei messaggi di phishing;
- tasso di compromissione stretta;
- tasso di fallimento ampio;
- tasso di segnalazione;
- tasso di verifica;
- tasso di falsi positivi sui messaggi legittimi.

Genera inoltre tabelle e grafici utilizzabili nella discussione della tesi.

---

## Requisiti

Il progetto richiede Python 3.10 o superiore.

Installa le dipendenze Python con:

```bash
pip install -r requirements.txt
```

Le dipendenze attuali sono:

```text
requests
pandas
matplotlib
seaborn
jupyter
```

La simulazione richiede inoltre un'installazione locale di Ollama.

---

## Configurazione LLM con Ollama

Installa Ollama da:

```text
https://ollama.com
```

Poi scarica il modello usato dalla simulazione:

```bash
ollama pull llama3
```

Verifica che il modello funzioni:

```bash
ollama run llama3 "Ciao"
```

La simulazione usa l'endpoint API locale di Ollama:

```text
http://localhost:11434/api/generate
```

Assicurati che Ollama sia in esecuzione prima di avviare la simulazione.

---

## Esecuzione della simulazione

Dalla cartella principale del progetto, esegui:

```bash
python simulations/run_simulation.py
```

Lo script genera un file CSV nella cartella `results/`:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

Ogni esecuzione crea un nuovo file e non sovrascrive i risultati precedenti.

Il CSV include metadati come:

- identificativo della run;
- nome del modello;
- profilo agente;
- scenario del messaggio;
- caratteristiche del messaggio;
- scelta grezza prodotta dal LLM;
- scelta normalizzata;
- stato del parsing;
- motivazione;
- risposta grezza del modello.

---

## Azioni di output

La simulazione chiede a ogni agente sintetico di scegliere esattamente una delle seguenti azioni:

```text
IGNORA
APRE_LINK
COLLEGA_WALLET_O_APPROVA_TRANSAZIONE
INSERISCE_CREDENZIALI_O_SEED
INVIA_FONDI
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PARSE_ERROR
```

| Azione | Significato |
|---|---|
| `IGNORA` | L'agente ignora il messaggio. |
| `APRE_LINK` | L'agente apre il link, ma non compie ulteriori azioni rischiose. |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | L'agente collega il wallet o approva una transazione potenzialmente malevola. |
| `INSERISCE_CREDENZIALI_O_SEED` | L'agente inserisce credenziali, codici OTP, seed phrase o altre informazioni sensibili. |
| `INVIA_FONDI` | L'agente invia criptovalute all'indirizzo indicato dal messaggio. |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | L'agente verifica il messaggio tramite sito ufficiale, app ufficiale, supporto verificato o persona esperta. |
| `SEGNALA_COME_PHISHING` | L'agente segnala o classifica il messaggio come phishing. |
| `PARSE_ERROR` | La risposta del modello non è stata interpretata o normalizzata correttamente. |

I valori `PARSE_ERROR` sono trattati come errori tecnici e dovrebbero essere esclusi dall'analisi comportamentale.

---

## Esecuzione dell'analisi

Dopo aver generato almeno un file CSV, apri JupyterLab:

```bash
jupyter lab
```

Poi apri:

```text
analysis.ipynb
```

Esegui tutte le celle:

```text
Run → Run All Cells
```

Il notebook carica automaticamente il file CSV più recente dalla cartella `results/` e produce statistiche e grafici riassuntivi.

I grafici generati vengono salvati localmente in:

```text
results/plots/
```

---

## Metriche

L'analisi separa i messaggi di phishing dai messaggi legittimi.

Per gli scenari di phishing, le metriche principali sono:

| Metrica | Descrizione |
|---|---|
| Click rate | Percentuale di messaggi di phishing in cui l'agente apre il link. |
| Strict compromise rate | Percentuale di messaggi di phishing in cui l'agente compie un'azione chiaramente compromettente. |
| Loose failure rate | Percentuale di messaggi di phishing in cui l'agente compie una qualunque interazione rischiosa. |
| Reporting rate | Percentuale di messaggi di phishing segnalati come phishing. |
| Verification rate | Percentuale di messaggi di phishing verificati tramite canali ufficiali o affidabili. |

Per i messaggi legittimi, l'analisi si concentra su:

| Metrica | Descrizione |
|---|---|
| Legitimate interaction rate | Percentuale di messaggi legittimi in cui l'agente interagisce normalmente. |
| False positive rate | Percentuale di messaggi legittimi erroneamente segnalati come phishing. |

---

## Riproducibilità

La simulazione usa un seed fisso per rendere deterministica l'espansione dei profili:

```python
RANDOM_SEED = 42
```

Anche i parametri di generazione del modello sono configurati nello script di simulazione.

Ogni file CSV salva il `run_id` e il nome del modello, così da facilitare il confronto tra run, prompt o modelli diversi.

---

## Considerazioni etiche e di sicurezza

Questo repository non include e non supporta:

- infrastrutture reali di phishing;
- raccolta di credenziali;
- malware;
- domini malevoli reali;
- vittime reali;
- interazioni reali con wallet;
- attacchi automatizzati;
- strumenti offensivi di exploit.

Tutti i messaggi di phishing sono sintetici e usati esclusivamente in un ambiente locale e controllato.

Lo scopo del progetto è supportare didattica, consapevolezza sulla sicurezza e ricerca accademica.

---

## Limiti

Il progetto presenta alcuni limiti importanti:

1. **Gli agenti sintetici non sono utenti reali.**  
   Il loro comportamento è generato da un LLM e dipende dal prompt, dal modello e dai parametri della simulazione.

2. **I risultati non sono statisticamente rappresentativi.**  
   I profili sintetici non costituiscono un campione della popolazione e non devono essere interpretati come tassi reali di vulnerabilità al phishing.

3. **Gli LLM possono mostrare bias di sicurezza.**  
   Il modello può riconoscere indicatori evidenti di phishing più facilmente di un utente medio, soprattutto in scenari che coinvolgono seed phrase o credenziali.

4. **La simulazione è esplorativa.**  
   Il valore dell'esperimento sta nel confronto tra scenari, profili e pattern comportamentali, non nella stima di percentuali reali.

5. **Il prompt influenza i risultati.**  
   Formulazioni diverse, modelli diversi, temperature diverse o definizioni diverse delle azioni possono produrre esiti differenti.

Questi limiti devono essere considerati esplicitamente nella discussione della tesi.

---

## Uso accademico

Questo repository è stato sviluppato nell'ambito di una tesi triennale in Cybersecurity presso l'Università degli Studi di Milano.

Il framework sperimentale integra l'analisi teorica degli attacchi di ingegneria sociale legati alle criptovalute, fornendo un ambiente di simulazione controllato e riproducibile.

---

## Disclaimer

Questo progetto è fornito esclusivamente per finalità didattiche e di ricerca.

L'autore non approva, abilita o incoraggia phishing, frodi, furto di credenziali o qualunque forma di accesso non autorizzato. Tutti gli scenari sono sintetici e progettati esclusivamente per sperimentazione accademica sicura.
