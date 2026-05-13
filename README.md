# Crypto Phishing Simulation Thesis

This repository contains a local LLM-based simulation framework for studying how synthetic user archetypes react to crypto-related phishing and legitimate messages.

## Purpose

The project is academic and defensive. It explores how simulated users may react after reading synthetic crypto-related messages, including fraudulent and legitimate scenarios.

The framework does not measure real phishing rates and must not be interpreted as an empirical estimate of attack success. Its purpose is to support methodological discussion, cybersecurity education, and exploratory comparison across profiles, scenarios, prompts, and models.

## Ethical and Safety Scope

- All scenarios are synthetic.
- Domains use safe/test values such as `.test`.
- No real phishing infrastructure is created.
- No real users are contacted.
- No credentials, wallet data, or funds are collected.
- The project is for cybersecurity education and research.
- Outputs are simulated and must not be interpreted as real-world attack success rates.

## Repository Structure

```text
agents/
  profiles_archetypes.json      Synthetic user archetypes
scenarios/
  messages.json                 Synthetic phishing and legitimate messages
simulations/
  run_simulation.py             Main simulation runner
  analyze_latest.py             Terminal analysis of the latest CSV
results/
  sim_*.csv                     Local generated outputs, ignored by Git
analysis.ipynb                  Optional notebook analysis
README_IT.md                    Italian documentation
requirements.txt                Python dependencies
```

## Simulation Design

Agents are synthetic archetypes with demographic, technical, behavioral, and contextual attributes. Messages include both phishing and legitimate scenarios.

The user is assumed to have already received and read the message. Reading the message is not a simulated choice. The first modeled choice is the behavioral reaction after reading.

The simulation uses a two-stage behavioral structure:

1. Initial decision after reading.
2. Flow outcome if the user proceeds with the message request.

The internal `message_type` label is used by validation and analysis, but it is not shown to the model as explicit decision information.

### `decision`

- `IGNORA`: the user ignores the message.
- `RIMANDA_O_NON_DECIDE`: the user postpones or leaves the message unresolved.
- `VERIFICA_TRAMITE_CANALE_UFFICIALE`: the user checks through an independent official channel.
- `SEGNALA_COME_PHISHING`: the user reports or marks the message as suspicious.
- `PROCEDE_CON_LA_RICHIESTA`: the user enters the flow proposed by the message.

### `flow_outcome`

- `NON_ENTRA_NEL_FLOW`: the user does not enter the requested flow.
- `SI_FERMA_PRIMA_DELLA_COMPROMISSIONE`: the user enters the flow but stops before the final compromising action.
- `COMPROMISSIONE_COMPLETATA`: the user completes a scenario-compatible compromising action.
- `AZIONE_LEGITTIMA_COMPLETATA`: the user completes a legitimate requested action.

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

`compromise_action` is scenario-specific. For a phishing scenario, a completed compromise is valid only if the action is listed in that scenario's `possible_compromise_actions`.

## Compromise Calculation

`compromised` no longer depends on a global list of risky actions. It is calculated with scenario-level compatibility:

```python
compromised = (
    message_type == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in possible_compromise_actions
)
```

This means:

- legitimate messages cannot produce `compromised = True`;
- entering the flow is not automatically a compromise;
- stopping before compromise is tracked separately;
- compromise requires phishing, completed flow, and a scenario-compatible final action.

## Model

- Recommended model: `qwen3:8b` through Ollama.
- Default temperature: `0.3`.
- JSON schema / structured output is used when available.
- A fallback to JSON mode is implemented for older Ollama runtimes.
- Model outputs are validated.
- Invalid responses are retried once.

## How to Run

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Short balanced run:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Full run:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analyze the latest result:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## CLI Options

- `--model`: Ollama model name.
- `--temperature`: model temperature.
- `--instances`: number of generated instances per archetype.
- `--limit`: maximum number of interactions to run.
- `--seed`: global simulation seed.
- `--balanced`: when used with `--limit`, distributes interactions across scenarios.

## Output

Each CSV row represents one interaction between one synthetic agent and one message.

Main columns:

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

The CSV also contains run metadata, agent traits, message features, and backward-compatible aliases for older notebooks.

## Analysis

`simulations/analyze_latest.py`:

- loads the latest CSV from `results/`, or a selected CSV with `--file`;
- prints row count, model, and temperature when present;
- reports parse and validation error rates;
- prints distributions of `decision`, `flow_outcome`, and `compromise_action`;
- computes entered-flow, stopped-before-compromise, verification, reporting, ignored, delayed, and legitimate-completion rates;
- computes the phishing compromise rate;
- checks that legitimate messages have `compromised = False`;
- reports scenario-level and archetype-level results;
- prints scenario x `flow_outcome` and scenario x `compromise_action` tables;
- warns about possible methodological issues without treating them as targets to force.

## Methodological Limitations

- LLMs may have safety-oriented biases.
- Synthetic users are not real users.
- Results depend on prompt, model, temperature, validation rules, and scenario design.
- Reported rates should not be interpreted as real-world probabilities.
- The model may overuse verification or stopping before compromise.
- The model may underrepresent reporting behavior.
- The framework is exploratory and should be discussed as a simulation, not as measurement of real populations.

## Suggested Workflow

1. Run a balanced mini-run.
2. Inspect the analysis output.
3. Run the full simulation only after the schema and prompt behave correctly.
4. Compare outputs across prompt/model versions when needed.
