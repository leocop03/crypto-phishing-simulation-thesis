# Crypto Phishing Simulation

Local LLM-based simulation framework for studying how synthetic user profiles react to cryptocurrency-related phishing and legitimate messages.

The project runs fully locally through Ollama. Python handles profile expansion, prompt construction, JSON validation, result normalization and CSV export. The language model is used as the behavioral decision component.

## Scope

This repository is intended for cybersecurity research, education and defensive analysis.

The project does not perform phishing, contact real users, collect credentials, interact with wallets or deploy attack infrastructure. All scenarios are synthetic and use safe `.test` domains.

Simulation outputs are exploratory. They should not be interpreted as real-world phishing success rates or as measurements of actual user behavior.

## Repository structure

```text
crypto-phishing-simulation-thesis/
├── agents/
│   └── profiles_archetypes.json
├── scenarios/
│   └── messages.json
├── simulations/
│   ├── run_simulation.py
│   └── analyze_latest.py
├── results/              # generated locally, ignored by Git
├── analysis.ipynb
├── requirements.txt
├── README.md
└── README_IT.md
```

## Simulation design

The simulation combines synthetic user archetypes with crypto-related messages.

By default, the full run uses:

```text
16 archetypes × 6 instances per archetype = 96 synthetic agents
96 agents × 10 messages = 960 simulated interactions
```

Each agent receives the same set of messages. For each agent-message pair, the model returns a structured decision in JSON format.

The user is assumed to have already received and read the message. Reading the message is not modeled as a decision. The simulation starts from the reaction after reading.

## Decision model

Each interaction is represented through three main fields.

### `decision`

Initial behavioral response after reading the message:

```text
IGNORA
RIMANDA_O_NON_DECIDE
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PROCEDE_CON_LA_RICHIESTA
```

`PROCEDE_CON_LA_RICHIESTA` means that the agent enters the flow proposed by the message. Opening a link, button or chat is considered implicit and is not stored as a final action.

### `flow_outcome`

Outcome of the interaction flow:

```text
NON_ENTRA_NEL_FLOW
SI_FERMA_PRIMA_DELLA_COMPROMISSIONE
COMPROMISSIONE_COMPLETATA
AZIONE_LEGITTIMA_COMPLETATA
```

Entering the flow is not automatically counted as compromise. An agent may proceed initially and then stop before completing a harmful action.

### `compromise_action`

Final compromising action, when applicable:

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

Compromise actions are scenario-specific. For example, a giveaway scenario can involve `INVIA_FONDI`, while a fake wallet migration can involve `COLLEGA_WALLET` or `APPROVA_TRANSAZIONE`.

## Compromise calculation

A row is marked as compromised only when all of the following conditions hold:

```python
compromised = (
    message_type == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in possible_compromise_actions
)
```

Legitimate messages cannot produce `compromised = True`. If an agent completes a legitimate flow, the output is recorded as `AZIONE_LEGITTIMA_COMPLETATA` with `compromise_action = NESSUNA`.

## Model configuration

Recommended local model:

```text
qwen3:8b
```

Default temperature:

```text
0.3
```

The script uses structured JSON output when available and falls back to JSON mode when needed. Responses are validated in Python. Invalid responses are retried once before being saved as parse or validation errors.

## Installation

Install and start Ollama, then pull the model:

```powershell
ollama pull qwen3:8b
```

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Running the simulation

Balanced test run:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Full run:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analyze the latest result file:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## CLI options

```text
--model          Ollama model name
--temperature    model temperature
--instances      instances generated per archetype
--limit          maximum number of interactions to run
--seed           Python-side experiment seed
--balanced       distribute limited runs across scenarios
```

## Output

Simulation outputs are saved as CSV files in `results/`.

Main columns include:

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

## Analysis

`simulations/analyze_latest.py` loads the most recent CSV file from `results/` and prints:

- row count and model metadata;
- parse and validation error rates;
- decision distribution;
- flow outcome distribution;
- compromise action distribution;
- phishing compromise rate;
- legitimate-message checks;
- scenario-level results;
- archetype-level results;
- methodological warnings.

The notebook `analysis.ipynb` can be used for deeper inspection, tables and plots.

## Methodological notes

This framework is a controlled simulation, not an empirical user study.

Important limitations:

- synthetic agents are not real users;
- outputs depend on the chosen model, prompt, temperature and scenario design;
- local LLMs may show safety-oriented or consistency-oriented biases;
- simulated rates should be interpreted comparatively, not as real-world probabilities;
- scenario wording can influence model behavior;
- results should be discussed together with qualitative inspection of motivations and raw responses.

## Suggested workflow

1. Run a balanced mini-run.
2. Inspect `analyze_latest.py` output.
3. Check parse errors, validation errors and legitimate-message behavior.
4. Run the full simulation only after the structure looks stable.
5. Compare results across model or prompt versions when needed.
