# Simulazione di Phishing Crypto per Tesi di Cybersecurity

## Panoramica

Questo repository contiene la parte sperimentale di una tesi triennale in Cybersecurity dedicata al phishing nel mondo delle criptovalute, all’ingegneria sociale e agli attacchi che sfruttano il comportamento umano.

Il progetto implementa una simulazione controllata in cui profili utente sintetici interagiscono con messaggi di phishing e messaggi legittimi legati all’ecosistema crypto. Le decisioni degli agenti vengono generate tramite un Large Language Model eseguito localmente con Ollama.

L’obiettivo non è creare strumenti offensivi o infrastrutture realistiche di phishing, ma studiare in modo sperimentale come diverse caratteristiche dell’utente e del messaggio possano influenzare comportamenti rischiosi o prudenti.

---

## Disclaimer importante

Questo progetto è stato sviluppato esclusivamente per:

- ricerca accademica;
- studio del social engineering;
- analisi comportamentale;
- sensibilizzazione sul phishing.

Il repository:

- NON esegue phishing reale;
- NON raccoglie credenziali;
- NON interagisce con utenti reali;
- NON utilizza wallet reali;
- NON usa infrastrutture malevole reali;
- NON automatizza attacchi.

Tutti gli scenari sono sintetici e confinati in un ambiente locale e controllato.

---

# Contesto della tesi

La tesi analizza il rapporto tra criptovalute e ingegneria sociale, con particolare attenzione al modo in cui gli attaccanti sfruttano:

- urgenza;
- paura;
- fiducia;
- sovraccarico cognitivo;
- impersonificazione;
- errori operativi;
- assistenza tecnica fasulla;
- procedure di recupero account;
- accesso remoto.

Molti attacchi crypto di successo non violano direttamente blockchain o smart contract. Spesso il vero punto debole è l’utente.

Questo repository nasce per simulare queste dinamiche in modo riproducibile.

---

# Obiettivi dell’esperimento

La simulazione serve a osservare:

- come profili diversi reagiscono a tentativi di phishing;
- quanto urgenza e personalizzazione influenzino il comportamento;
- come esperienza crypto e formazione sulla sicurezza cambino le decisioni;
- come gli utenti distinguano messaggi legittimi e malevoli;
- come attacchi mirati possano colpire utenti ad alto valore;
- come gli LLM possano essere usati in simulazioni comportamentali in ambito cybersecurity.

L’esperimento NON ha valore statistico sulla popolazione reale. Serve soprattutto a confrontare scenari e pattern comportamentali.

---

# Struttura del repository

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
│   └── generata localmente (ignorata da Git)
│
├── analysis.ipynb
├── requirements.txt
├── README.md
├── README_IT.md
└── .gitignore
```

---

# Componenti principali

## `agents/`

Contiene gli archetipi sintetici usati nella simulazione.

Ogni archetipo definisce:

- età;
- fascia d’età;
- ruolo;
- esperienza con le criptovalute;
- formazione sulla sicurezza;
- ambiente d’uso;
- tratti comportamentali.

Ogni archetipo viene poi espanso in più istanze sintetiche con piccole variazioni controllate.

---

## `scenarios/`

Contiene gli scenari dei messaggi.

Ogni scenario include:

- ID del messaggio;
- tipo (`phishing` o `legittimo`);
- canale di comunicazione;
- testo;
- livello di urgenza;
- livello di personalizzazione;
- beneficio percepito;
- eventuale collegamento al caso studio.

Gli URL sospetti usano domini `.test` sicuri.

---

## `simulations/`

Contiene il motore della simulazione.

Lo script:

1. carica gli archetipi;
2. genera gli agenti sintetici;
3. carica gli scenari;
4. invia i prompt al modello locale tramite Ollama;
5. normalizza le risposte;
6. salva tutto in CSV.

---

## `analysis.ipynb`

Contiene il notebook di analisi.

Il notebook:
- carica automaticamente l’ultimo CSV;
- separa phishing e messaggi legittimi;
- analizza i background individuali;
- analizza i tratti comportamentali;
- calcola metriche;
- genera grafici e tabelle;
- produce statistiche dedicate agli scenari ispirati al caso studio.

---

# Generazione degli agenti sintetici

Ogni archetipo viene espanso in più istanze.

Esempio:

```text
teen_gamer_lowsec_1
teen_gamer_lowsec_2
teen_gamer_lowsec_3
```

Tutti condividono la stessa identità generale, ma differiscono leggermente in:
- impulsività;
- attenzione;
- fiducia nei brand;
- competenza tecnica;
- prudenza;
- contesto personale.

Questo evita che gli agenti siano stereotipi troppo rigidi.

---

# Variabili comportamentali

La simulazione modella diverse dimensioni psicologiche e operative.

---

## `impulsiveness`

Indica quanto velocemente l’agente tende ad agire senza riflettere troppo.

Valori possibili:

```text
molto_bassa
bassa
media
alta
molto_alta
```

---

## `trust_in_brands`

Indica quanto facilmente l’agente si fida di messaggi che sembrano provenire da brand noti, exchange o servizi conosciuti.

---

## `tech_savvy`

Indica il livello di competenza tecnica.

NON significa automaticamente essere esperti di sicurezza.

---

## `attention_level`

Rappresenta quanto attentamente l’agente controlla dettagli, URL, mittenti e anomalie.

---

## `risk_aversion`

Indica quanto l’agente tende a evitare rischi finanziari o operativi.

---

# Background individuali

Ogni agente riceve anche un piccolo contesto personale casuale.

Esempi:
- ha recentemente visto video divulgativi sul phishing;
- è distratto dal multitasking;
- ha già subito tentativi di phishing;
- tende a fidarsi dei brand;
- controlla spesso URL e mittenti;
- ha fretta;
- è incuriosito dagli airdrop crypto.

Questi dettagli servono a rendere la simulazione meno rigida e più realistica.

---

# Parametri importanti della simulazione

---

## Seed fisso (`RANDOM_SEED`)

```python
RANDOM_SEED = 42
```

Il seed fisso serve a rendere la simulazione riproducibile.

Controlla la casualità generata da Python:
- variazioni di età;
- assegnazione dei background;
- modifiche dei tratti;
- generazione delle istanze.

Usare un seed fisso permette di confrontare più run in modo coerente.

---

## Temperature

```python
"temperature": 0.4
```

La temperature controlla quanto il modello sia:
- prevedibile;
- coerente;
- variabile.

Temperature basse:
- rendono il modello più rigido.

Temperature alte:
- aumentano casualità e variabilità.

Il valore `0.4` è stato scelto come compromesso tra coerenza e realismo comportamentale.

---

## Modalità JSON di Ollama

La simulazione usa:

```python
"format": "json"
```

Questo obbliga il modello a produrre output JSON strutturati.

Vantaggi:
- meno errori di parsing;
- CSV più puliti;
- risposte più consistenti;
- meno testo inutile.

---

# Configurazione LLM

Il progetto usa Ollama come motore locale.

Modello consigliato:

```text
llama3.2:3b
```

Inizialmente il progetto usava `llama3`, ma modelli più piccoli accelerano molto la simulazione mantenendo risultati sufficientemente coerenti.

---

# Installazione di Ollama

Scarica Ollama da:

```text
https://ollama.com
```

Scarica il modello:

```bash
ollama pull llama3.2:3b
```

Verifica che funzioni:

```bash
ollama run llama3.2:3b "Ciao"
```

---

# Esecuzione della simulazione

Avvia:

```bash
python simulations/run_simulation.py
```

Ogni esecuzione crea un nuovo file CSV:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

I risultati precedenti NON vengono sovrascritti.

---

# Variabili salvate nel CSV

Ogni riga rappresenta una singola interazione agente-messaggio.

Il CSV include:

| Colonna | Significato |
|---|---|
| `agent_id` | ID dell’agente sintetico |
| `age` | Età |
| `age_group` | Fascia d’età |
| `role` | Ruolo simulato |
| `crypto_experience` | Esperienza crypto |
| `security_training` | Formazione sicurezza |
| `environment` | Ambiente d’uso |
| `background` | Contesto individuale |
| `message_id` | ID scenario |
| `message_type` | Tipo messaggio |
| `channel` | Canale |
| `urgency` | Urgenza percepita |
| `personalization` | Personalizzazione |
| `reward` | Beneficio percepito |
| `choice` | Azione finale |
| `motivation` | Motivazione generata dal modello |
| `parse_error` | Errore tecnico di parsing |

---

# Azioni possibili

Gli agenti devono scegliere una sola azione finale.

```text
IGNORA
APRE_LINK
COLLEGA_WALLET_O_APPROVA_TRANSAZIONE
INSERISCE_CREDENZIALI_O_SEED
CONCEDE_ACCESSO_REMOTO
INVIA_FONDI
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PARSE_ERROR
```

---

# Significato delle azioni

| Azione | Significato |
|---|---|
| `IGNORA` | Ignora il messaggio |
| `APRE_LINK` | Apre il link ma si ferma prima di azioni pericolose |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | Collega wallet o approva una transazione |
| `INSERISCE_CREDENZIALI_O_SEED` | Inserisce credenziali o seed phrase |
| `CONCEDE_ACCESSO_REMOTO` | Concede accesso remoto o condivisione schermo |
| `INVIA_FONDI` | Invia criptovalute |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | Controlla tramite canali affidabili |
| `SEGNALA_COME_PHISHING` | Segnala il phishing |
| `PARSE_ERROR` | Errore tecnico |

---

# Estensione sul caso studio

La simulazione include scenari ispirati al caso studio analizzato nella tesi.

Gli scenari modellano:
- falso supporto tecnico;
- allarmi di sicurezza;
- urgenza;
- richiesta di verifica account;
- assistenza remota;
- protezione dei fondi.

È incluso anche un profilo sintetico di utente crypto ad alto valore.

Gli scenari NON ricostruiscono parola per parola l’attacco reale: sono modellazioni basate su informazioni pubbliche.

---

# Metriche principali

---

## Click rate

Percentuale di messaggi di phishing in cui l’agente apre il link.

---

## Wallet/transaction approval rate

Percentuale di messaggi in cui l’agente collega wallet o approva transazioni.

---

## Credential disclosure rate

Percentuale di messaggi in cui vengono inserite credenziali, OTP o seed phrase.

---

## Remote access rate

Percentuale di messaggi in cui viene concesso accesso remoto.

---

## Fund transfer rate

Percentuale di messaggi in cui vengono inviati fondi.

---

## Tasso di compromissione

Percentuale di messaggi in cui l’agente compie un’azione chiaramente pericolosa.

Comprende:
- collegamento wallet;
- approvazione transazioni;
- accesso remoto;
- inserimento credenziali;
- invio fondi.

---

## Loose failure rate

Percentuale di messaggi in cui l’agente compie una qualunque interazione rischiosa, incluso il semplice click sul link.

---

## Reporting rate

Percentuale di messaggi segnalati come phishing.

---

## Verification rate

Percentuale di messaggi verificati tramite canali affidabili.

---

# Esecuzione dell’analisi

Apri Jupyter:

```bash
jupyter lab
```

Poi:

```text
analysis.ipynb
```

Esegui tutte le celle.

Il notebook carica automaticamente l’ultimo CSV disponibile.

Grafici e tabelle vengono salvati in:

```text
results/plots/
```

---

# Prestazioni

La velocità della simulazione dipende soprattutto da:
- dimensione del modello;
- lunghezza del prompt;
- uso della GPU;
- numero di interazioni.

Usare:

```text
llama3.2:3b
```

riduce molto i tempi rispetto a modelli più grandi.

---

# Considerazioni etiche

Il repository NON include:
- malware;
- phishing kit;
- stealer;
- exploit;
- infrastrutture reali;
- automazione offensiva.

Tutti gli scenari sono sintetici.

Il progetto ha finalità esclusivamente difensive e accademiche.

---

# Limiti

Il progetto presenta diversi limiti importanti.

1. Gli agenti sintetici non sono persone reali.

2. I risultati non sono statisticamente rappresentativi.

3. Gli LLM possono avere bias di sicurezza.

4. Il prompt influenza molto i risultati.

5. Modelli diversi producono risultati diversi.

6. Gli scenari del caso studio sono approssimazioni.

7. Il comportamento umano reale non può essere riprodotto perfettamente.

Questi limiti vengono discussi esplicitamente nella tesi.

---

# Contesto accademico

Progetto sviluppato per una tesi triennale in Cybersecurity presso l’Università degli Studi di Milano.

Il lavoro combina:
- sicurezza crypto;
- social engineering;
- simulazioni comportamentali;
- LLM locali;
- analisi sperimentale.

---

# Licenza

Repository destinato a uso accademico e didattico.
