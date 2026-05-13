# Crypto Phishing Simulation Thesis

This repository contains a local LLM-based simulation framework for studying how synthetic user archetypes react to crypto-related phishing and legitimate messages.

The project is intended for an academic cybersecurity thesis. It is not a phishing toolkit and it does not measure real-world phishing success rates.

## Purpose

The goal of the project is to explore, in a controlled and reproducible way, how different synthetic user profiles may react after reading crypto-related messages.

The simulation can be used to compare:

- user archetypes with different levels of security awareness, technical ability, crypto experience, impulsiveness, attention, trust, and risk aversion;
- phishing scenarios with different social-engineering mechanisms;
- legitimate control messages;
- behavioral outcomes such as verification, reporting, entering the flow, stopping before compromise, and completing a compromising action.

The output should be interpreted as an exploratory simulation, not as empirical evidence about real users.

## Ethical and Safety Scope

This repository is designed for defensive, educational, and academic use only.

Safety boundaries:

- All scenarios are synthetic.
- Domains use safe/test values such as `.test`.
- No real phishing infrastructure is created.
- No real users are contacted.
- No credentials, wallet data, seed phrases, or funds are collected.
- No operational phishing instructions are provided.
- Results are simulated and must not be interpreted as real-world attack success rates.

## Repository Structure

```text
agents/
  profiles_archetypes.json      Synthetic user archetypes

scenarios/
  messages.json                 Synthetic phishing and legitimate messages

simulations/
  run_simulation.py             Main simulation runner
  analyze_latest.py             Terminal analysis of generated CSV files

results/
  sim_*.csv                     Generated simulation outputs, ignored by Git

analysis.ipynb                  Optional notebook-based analysis
README.md                       English documentation
README_IT.md                    Italian documentation
requirements.txt                Python dependencies
```

## Simulation Design

The simulation is based on three main components:

1. **Synthetic agents**: user archetypes with behavioral and contextual attributes.
2. **Synthetic messages**: phishing and legitimate crypto-related scenarios.
3. **A local LLM**: the model interprets each archetype and returns a structured behavioral decision.

The user is assumed to have already received and read the message. Reading the message is not modeled as a choice. The first simulated choice is the user's behavioral reaction after reading.

The simulation follows a two-stage behavioral structure:

1. **Initial decision** after reading the message.
2. **Flow outcome** if the user proceeds with the message request.

The internal `message_type` label is used for validation and analysis, but it is not shown to the model as explicit decision information.

## Full Simulation Size

The default full run produces 960 simulated interactions:

```text
16 archetypes × 6 instances per archetype = 96 synthetic agents
96 synthetic agents × 10 messages = 960 interactions
```

Each CSV row represents one interaction between one synthetic agent and one message.

## Decision Schema

### `decision`

The first-level behavioral decision after the message has been read.

Allowed values:

- `IGNORA`: the user ignores the message.
- `RIMANDA_O_NON_DECIDE`: the user postpones the decision or does not act immediately.
- `VERIFICA_TRAMITE_CANALE_UFFICIALE`: the user checks through an independent official channel.
- `SEGNALA_COME_PHISHING`: the user reports or marks the message as suspicious.
- `PROCEDE_CON_LA_RICHIESTA`: the user enters the flow proposed by the message.

### `flow_outcome`

The behavioral outcome after the first-level decision.

Allowed values:

- `NON_ENTRA_NEL_FLOW`: the user does not enter the requested flow.
- `SI_FERMA_PRIMA_DELLA_COMPROMISSIONE`: the user enters the flow but stops before the final compromising action.
- `COMPROMISSIONE_COMPLETATA`: the user completes a scenario-compatible compromising action.
- `AZIONE_LEGITTIMA_COMPLETATA`: the user completes a legitimate requested action.

### `compromise_action`

The concrete compromising action, if a compromise is completed.

Allowed values:

- `NESSUNA`
- `INSERISCE_CREDENZIALI`
- `INSERISCE_DATI_KYC`
- `INSERISCE_SEED_PHRASE`
- `COLLEGA_WALLET`
- `APPROVA_TRANSAZIONE`
- `CONCEDE_ACCESSO_REMOTO`
- `INVIA_FONDI`
- `INSTALLA_APP_O_SOFTWARE`

`compromise_action` is scenario-specific. A completed compromise is valid only if the action belongs to that scenario's `possible_compromise_actions`.

## Compromise Calculation

The simulation does not use a global list of risky actions to determine compromise.

Instead, compromise is calculated through scenario-level compatibility:

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
- compromise requires a phishing message, a completed flow, and a scenario-compatible final action.

## Model

Recommended configuration:

- Model: `qwen3:8b` through Ollama.
- Temperature: `0.3`.
- Output: structured JSON when available, with fallback to JSON mode.
- Validation: model outputs are normalized, validated, and retried once if invalid.

The local model setup is useful because it allows repeated simulations without external API costs and keeps the experimental environment more controlled.

## Installation

From Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Make sure Ollama is running locally and that the selected model is available:

```powershell
ollama pull qwen3:8b
```

## How to Run

Short balanced run, useful for testing prompt and schema behavior:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 160 --balanced
```

Full simulation:

```powershell
.\.venv\Scripts\python.exe simulations/run_simulation.py --model qwen3:8b --temperature 0.3
```

Analyze the latest generated CSV:

```powershell
.\.venv\Scripts\python.exe simulations/analyze_latest.py
```

## CLI Options

Implemented options:

- `--model`: Ollama model name.
- `--temperature`: model temperature.
- `--instances`: number of generated instances per archetype.
- `--limit`: maximum number of interactions to run.
- `--seed`: global simulation seed.
- `--balanced`: when used with `--limit`, distributes interactions across scenarios.

## Output

Generated CSV files are saved in `results/` as `sim_*.csv`.

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

The CSV may also contain run metadata, agent traits, message features, and backward-compatible aliases for older analysis notebooks.

## Analysis

`simulations/analyze_latest.py` loads the latest CSV from `results/`, or a selected CSV if supported by the script, and prints a terminal summary.

The analysis focuses on:

- row count, model, and temperature;
- parse and validation error rates;
- distribution of `decision`;
- distribution of `flow_outcome`;
- distribution of `compromise_action`;
- entered-flow rate;
- stopped-before-compromise rate;
- phishing compromise rate;
- legitimate-message compromise check;
- verification, reporting, ignored, delayed, and legitimate-completion rates;
- scenario-level results;
- archetype-level results;
- possible methodological warnings.

Warnings are intended as methodological checks, not as targets to force through prompt tuning.

## Methodological Limitations

This project should be interpreted carefully.

Main limitations:

- LLMs may have safety-oriented or instruction-following biases.
- Synthetic users are not real users.
- Results depend on model, prompt, temperature, validation rules, and scenario design.
- Reported rates are simulated outputs, not real-world probabilities.
- The model may overuse verification or stopping before compromise.
- The model may underrepresent reporting behavior.
- Repeated runs may vary, even with a low temperature.
- The framework is exploratory and should be discussed as a simulation, not as a measurement of real populations.

## Suggested Workflow

1. Run a short balanced simulation.
2. Inspect the analysis output.
3. Check for parse errors, validation errors, legacy labels, and legitimate-message compromises.
4. Run the full simulation only after the schema and prompt behave correctly.
5. Compare outputs across prompt/model versions when useful.
6. Discuss both results and model limitations in the thesis.

## Suggested Thesis Placement

The project can be included as:

- a short experimental chapter;
- a methodological prototype;
- or an appendix supporting a broader thesis on crypto phishing and social engineering.

It should not replace empirical evidence from real users. Its value is methodological: it formalizes a phishing decision chain and allows controlled comparison between synthetic profiles and scenarios.
