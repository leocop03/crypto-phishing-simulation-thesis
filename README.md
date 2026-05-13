# Crypto Phishing Simulation Thesis

This repository contains the experimental component of a Bachelor's thesis in Cybersecurity about cryptocurrency-related phishing, social engineering, and user decision-making under pressure.

The project simulates how synthetic user profiles react to phishing and legitimate messages in crypto-related contexts. Each interaction is evaluated by a locally hosted Large Language Model (LLM) through Ollama. The LLM is the behavioral decision-maker: Python prepares the experiment, sends prompts, normalizes outputs, and stores results, but it does not assign actions through predefined statistical probabilities.

The simulation is exploratory. It is not meant to estimate real-world phishing success rates, nor to replace empirical studies on human users.

---

## Important disclaimer

This repository is intended only for:

- academic research;
- cybersecurity education;
- phishing awareness analysis;
- defensive behavioral simulation.

The project does **not**:

- perform real phishing;
- contact real users;
- collect credentials;
- interact with real wallets;
- use real attack infrastructure;
- automate offensive activity;
- provide phishing kits or operational attack instructions.

All scenarios are synthetic. Links use safe `.test` domains and are not intended to resolve to real infrastructure.

---

## Research context

Cryptocurrency attacks often exploit human behavior rather than weaknesses in blockchain protocols. Attackers may rely on urgency, fear, trust in known brands, fake support interactions, account compromise warnings, wallet verification procedures, remote access requests, or promises of financial reward.

This repository provides a reproducible local framework to explore how different synthetic users may react to these types of messages.

The broader thesis studies social engineering in the crypto ecosystem, with a specific focus on phishing dynamics and a case study inspired by a high-value cryptocurrency theft.

---

## Research objectives

The simulation is designed to explore:

- how different synthetic users react to crypto-related phishing messages;
- how urgency, personalization, and perceived reward influence behavior;
- how security training and crypto experience affect simulated decisions;
- the difference between ignoring, verifying, reporting, postponing, or proceeding with a scenario-specific action;
- how legitimate messages are handled by the same synthetic users;
- how targeted scenarios inspired by a real case study affect high-value crypto profiles;
- the strengths and weaknesses of using local LLM agents for exploratory cybersecurity research.

The results should be interpreted comparatively and methodologically, not as real-world population estimates.

---

## Repository structure

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
│   └── generated locally and ignored by Git
│
├── analysis.ipynb
├── requirements.txt
├── README.md
├── README_IT.md
└── .gitignore
```

---

## Main files

### `agents/profiles_archetypes.json`

Contains the base synthetic user archetypes. Each archetype describes a type of user through demographic, behavioral, and contextual variables.

### `scenarios/messages.json`

Contains phishing and legitimate messages used in the simulation. The dataset includes generic crypto phishing attempts, legitimate control messages, and targeted case-study-inspired scenarios.

### `simulations/run_simulation.py`

Runs the full simulation. It expands archetypes into individual synthetic agents, sends each agent-message pair to the local LLM, validates the JSON response, normalizes labels, and writes the output to a CSV file.

### `simulations/analyze_latest.py`

Loads the latest generated CSV and prints updated metrics for `decision`, `flow_outcome`, `compromise_action`, compromise, legitimate-message checks, parse errors, and warnings.

### `analysis.ipynb`

Analyzes simulation outputs. It loads the latest CSV from `results/`, computes metrics, creates tables/plots, and separates phishing scenarios from legitimate control messages.

---

## Synthetic agent model

The simulation starts from a set of base archetypes. Each archetype is expanded into several synthetic instances. This avoids treating each archetype as a rigid stereotype.

By default:

```python
INSTANCES_PER_ARCHETYPE = 6
```

With 16 archetypes, this generates:

```text
16 archetypes × 6 instances = 96 synthetic agents
```

If the scenario file contains 10 messages, the simulation produces:

```text
96 agents × 10 messages = 960 interactions
```

Each generated instance receives controlled variations in age, behavioral traits, security training, and situational background.

---

## Agent variables

Each archetype may include the following fields.

| Field | Meaning |
|---|---|
| `id` | Internal archetype identifier |
| `label` | Human-readable description of the archetype |
| `age` | Base age before small instance-level variation |
| `age_group` | Age range/category |
| `role` | Synthetic role or user profile |
| `crypto_experience` | Familiarity with crypto tools and ecosystems |
| `security_training` | Level of security awareness or training |
| `environment` | Typical digital context in which the user operates |
| `traits` | Behavioral dimensions used in the prompt |

### Behavioral traits

The main behavioral traits are:

| Trait | Meaning |
|---|---|
| `impulsiveness` | Tendency to act quickly without careful evaluation |
| `trust_in_brands` | Tendency to trust messages that appear to come from known brands/services |
| `tech_savvy` | General technical familiarity |
| `attention_level` | Tendency to notice details, inconsistencies, and warning signs |
| `risk_aversion` | Caution regarding financial or operational risks |

Trait values use this ordered scale:

```text
molto_bassa → bassa → media → alta → molto_alta
```

Security training uses this ordered scale:

```text
no → minima → basilare → autodidatta → si
```

Technical familiarity is not treated as identical to security awareness. A user can be technically skilled but still vulnerable to social pressure or contextual manipulation.

---

## Instance-level variation

The function `expand_profiles()` creates multiple instances for each archetype. Each instance can vary in:

- age, with a small random offset;
- impulsiveness;
- trust in brands;
- technical familiarity;
- attention level;
- risk aversion;
- security training;
- situational background.

Examples of background variants include:

- the user has little time and reads messages quickly;
- the user recently received a real security warning;
- the user often relies on phone notifications;
- the user tends to verify information online;
- the user often uses crypto services but does not always inspect details;
- the user has seen similar phishing attempts before;
- the user is multitasking;
- the user wants to resolve account-related issues quickly;
- the user prefers asking a more experienced person for confirmation;
- the user trusts messages that appear to come from known brands.

These variations are intended to make the simulated users less rigid while keeping the experiment interpretable.

---

## Scenario model

Each scenario in `scenarios/messages.json` contains:

| Field | Meaning |
|---|---|
| `id` | Scenario identifier |
| `type` | `phishing` or `legittimo` |
| `channel` | Communication channel, such as email, chat, social, mobile, or phone/chat |
| `description` | Short description used for analysis |
| `text` | Message shown to the synthetic agent |
| `features` | Scenario attributes used for analysis |

Scenario features include:

| Feature | Meaning |
|---|---|
| `urgency` | Pressure or time sensitivity |
| `personalization` | How tailored the message appears |
| `channel_brand` | Claimed source, service, platform, or brand context |
| `reward` | Perceived benefit or avoided loss |
| `case_study` | Optional flag for case-study-inspired messages |

The text shown to agents should not contain meta-labels such as “synthetic”, “fake simulation”, “non-real link”, or “demonstration”. Those safety notes belong in documentation or metadata, not in the message itself, because they would bias the LLM toward defensive behavior.

---

## Safe `.test` domains

All links use `.test` domains. This keeps the scenarios non-operational and prevents the repository from containing real phishing infrastructure.

The `.test` domain is intentionally reserved for testing and documentation contexts. The goal is to preserve safety while still giving the LLM a realistic-looking message structure.

---

## LLM-driven decision model

The LLM remains the behavioral decision-maker. Python prepares the experiment, constrains the response schema, validates outputs, and writes results, but it does not assign actions through predefined probabilities.

The simulation assumes the user has already received and read the message. Reading is not a simulated choice. The first simulated choice is what the user does after reading it.

For each agent-message pair, Python builds a prompt containing:

- the agent profile;
- behavioral traits;
- situational background;
- the message text;
- the entry action and scenario-specific compromise actions that are compatible with that message;
- logical consistency rules.

The model must return JSON with:

```json
{
  "decision": "...",
  "flow_outcome": "...",
  "compromise_action": "...",
  "motivation": "brief sentence"
}
```

The prompt explicitly asks the model to simulate an imperfect human user, not a cybersecurity advisor. The internal scenario label is not shown to the model.

---

## Post-read decision structure

Allowed decisions are:

```text
IGNORA
RIMANDA_O_NON_DECIDE
VERIFICA_TRAMITE_CANALE_UFFICIALE
SEGNALA_COME_PHISHING
PROCEDE_CON_LA_RICHIESTA
```

`PROCEDE_CON_LA_RICHIESTA` means the user enters the requested flow. Opening a link, button, or chat is implicit and is not treated as a final action.

If the decision is not `PROCEDE_CON_LA_RICHIESTA`, Python applies deterministic consistency rules:

- `flow_outcome = NON_ENTRA_NEL_FLOW`;
- `compromise_action = NESSUNA`.

For phishing messages, a proceeding user can either stop before compromise or complete one scenario-compatible compromise action such as `CONCEDE_ACCESSO_REMOTO`, `COLLEGA_WALLET`, `APPROVA_TRANSAZIONE`, `INVIA_FONDI`, or `INSTALLA_APP_O_SOFTWARE`.

`compromised` is calculated scenario by scenario:

```python
compromised = (
    message["type"] == "phishing"
    and flow_outcome == "COMPROMISSIONE_COMPLETATA"
    and compromise_action in message.get("possible_compromise_actions", [])
)
```

Legitimate messages therefore cannot generate compromise; if a legitimate flow is completed, `flow_outcome = AZIONE_LEGITTIMA_COMPLETATA` and `compromise_action = NESSUNA`.

---

## Simulation parameters

### Ollama model

```python
OLLAMA_MODEL = "qwen3:8b"
```

The recommended local model is `qwen3:8b`. The request uses `think: false` when supported by the local Ollama version, with a fallback for older runtimes.

### Ollama endpoint

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
```

This is the local Ollama API endpoint used by the simulation script.

### General random seed

```python
RANDOM_SEED = 42
```

`RANDOM_SEED` is the general seed of the experiment. It controls Python-side reproducibility, including:

- profile expansion;
- age variation;
- trait shifts;
- background assignment.

Changing `RANDOM_SEED` creates a different but still reproducible version of the experiment.

### Interaction seed

The script derives a stable seed for each agent-message pair:

```python
def make_interaction_seed(agent_id: str, message_id: str) -> int:
    key = f"{RANDOM_SEED}|{agent_id}|{message_id}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:8], 16)
```

This prevents every LLM call from using the exact same seed while keeping the full run reproducible.

Conceptually:

```text
RANDOM_SEED = seed of the whole experiment
interaction_seed = seed of one specific agent-message interaction
```

Only `RANDOM_SEED` is manually configured. `interaction_seed` is calculated automatically.

### Temperature

```python
TEMPERATURE = 0.3
```

Temperature is intentionally low because the simulation should be more stable than creative.

### JSON mode

The Ollama request first tries a JSON schema for `decision`, `flow_outcome`, `compromise_action`, and `motivation`. If the local Ollama version does not support schema format, the script falls back to plain JSON mode and still validates the response in Python.

---

## Output CSV

Each row in the output CSV represents one interaction between one synthetic agent and one scenario.

Main output columns include:

| Column | Meaning |
|---|---|
| `run_id` | Timestamp identifier of the run |
| `model` | Ollama model used |
| `temperature` | Temperature used for the run |
| `random_seed` | General experiment seed |
| `interaction_seed` | Stable seed for this agent-message interaction |
| `agent_id` | Synthetic agent identifier |
| `age` | Agent age after variation |
| `age_group` | Age group |
| `role` | Agent role/profile |
| `crypto_experience` | Crypto familiarity |
| `security_training` | Security training level |
| `environment` | Typical usage context |
| `background` | Situational background assigned to the instance |
| `impulsiveness` | Behavioral trait |
| `trust_in_brands` | Behavioral trait |
| `tech_savvy` | Behavioral trait |
| `attention_level` | Behavioral trait |
| `risk_aversion` | Behavioral trait |
| `message_id` | Scenario identifier |
| `message_type` | `phishing` or `legittimo` |
| `channel` | Communication channel |
| `scenario_description` | Human-readable scenario description |
| `urgency` | Scenario urgency |
| `personalization` | Scenario personalization |
| `reward` | Promised benefit or avoided loss |
| `raw_decision` | Raw LLM decision before normalization |
| `decision` | Normalized post-read decision |
| `raw_flow_outcome` | Raw flow outcome before normalization |
| `flow_outcome` | Normalized outcome after entering or not entering the flow |
| `raw_compromise_action` | Raw compromise action before normalization |
| `compromise_action` | Normalized compromise action, or `NESSUNA` |
| `entered_flow` | `True` when the user follows the message request |
| `stopped_before_compromise` | `True` when the user enters the flow but stops before compromise |
| `compromised` | `True` only for phishing scenarios with completed scenario-specific compromise |
| `verified` | `True` if the agent verifies through a trusted channel |
| `reported` | `True` if the agent reports the message |
| `ignored` | `True` if the agent ignores the message |
| `delayed` | `True` if the agent delays or does not decide |
| `legitimate_completion` | `True` if a legitimate requested action is completed |
| `parse_error` | `True` if parsing or label validation failed |
| `validation_error` | Reason for parse/validation failure |
| `motivation` | Short LLM-generated reason |
| `raw_response` | Raw model response |
| `raw_specific_action` | Backward-compatible alias of `raw_compromise_action` |
| `specific_action` | Backward-compatible alias of `compromise_action` |
| `proceeded` | Backward-compatible alias of `entered_flow` |
| `raw_initial_reaction` | Backward-compatible alias of `raw_decision` |
| `initial_reaction` | Backward-compatible alias of `decision` |
| `raw_final_action` | Backward-compatible alias of `raw_compromise_action` |
| `final_action` | Backward-compatible alias of `compromise_action` |
| `engaged` | Backward-compatible alias of `entered_flow` |
| `false_positive_report` | `True` if a legitimate message is reported as phishing |

---

## Metrics computed in analysis

The notebook or `simulations/analyze_latest.py` can compute metrics such as:

| Metric | Meaning |
|---|---|
| Decision distribution | Distribution of post-read decisions |
| Flow outcome distribution | Distribution of flow outcomes |
| Compromise action distribution | Distribution of completed compromise actions |
| Entered flow rate | Percentage that follows the message request |
| Stopped before compromise rate | Percentage that enters the flow but stops before compromise |
| Compromise rate on phishing | Percentage of phishing rows with completed scenario-specific compromise |
| Legitimate control check | Confirms legitimate messages do not produce compromise |
| Reporting rate | Percentage reported as phishing |
| Verification rate | Percentage verified through trusted channels |
| Legitimate completion rate | Percentage of legitimate messages completed normally |
| False positive rate | Percentage of legitimate messages reported as phishing |

The analysis separates phishing scenarios from legitimate control scenarios.

---

## Case-study scenarios

The repository includes case-study-inspired phishing scenarios. These focus on:

- fake support communications;
- account compromise warnings;
- urgency and pressure;
- remote assistance;
- wallet/device verification;
- high-value crypto holder behavior.

These are synthetic, non-operational scenarios inspired by the thesis case study. They are not verbatim reconstructions of real attacker communications.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/leocop03/crypto-phishing-simulation-thesis.git
cd crypto-phishing-simulation-thesis
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from the official website, then pull the model:

```bash
ollama pull qwen3:8b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

In another terminal, you can check the loaded model with:

```bash
ollama ps
```

---

## Running the simulation

From the repository root, run:

```bash
python simulations/run_simulation.py
```

Useful short-run options:

```bash
python simulations/run_simulation.py --model qwen3:8b --temperature 0.3 --limit 100
```

Each run creates a new CSV file:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

Previous simulations are not overwritten because the filename includes a timestamp.

The `results/` directory is ignored by Git so local outputs are not accidentally published.

---

## Running the analysis

Start Jupyter:

```bash
jupyter lab
```

Open:

```text
analysis.ipynb
```

Run all cells, or use the lightweight terminal analysis:

```bash
python simulations/analyze_latest.py
```

Both approaches load the latest simulation CSV from `results/` and compute the updated decision/action metrics.

---

## Reproducibility notes

To reproduce a run as closely as possible, keep the following unchanged:

- same repository version;
- same `RANDOM_SEED`;
- same `TEMPERATURE`;
- same Ollama model;
- same Ollama version/runtime;
- same scenario and archetype files.

Even with deterministic seeds, minor differences can occur across model/runtime versions. This is a known limitation of local LLM-based experiments.

---

## Performance notes

Runtime depends mainly on:

- number of agents;
- number of scenarios;
- model size;
- prompt length;
- CPU/GPU acceleration;
- Ollama configuration.

The default setup produces 960 LLM calls. On consumer hardware this can take a significant amount of time. Use `--limit` for mini-runs while testing prompt and validation changes.

---

## Git hygiene

The repository intentionally ignores:

- `.venv/`;
- `__pycache__/`;
- `.ipynb_checkpoints/`;
- `results/`;
- generated `.csv` files;
- `.env` files.

This keeps the public repository focused on code, scenarios, documentation, and analysis logic rather than local artifacts.

---

## Ethical and methodological limitations

This project has several important limitations:

1. Synthetic agents are not real humans.
2. LLMs may show strong safety or instruction-following bias.
3. Prompt wording can significantly affect behavior.
4. Different models may produce different results.
5. The simulation is not statistically representative.
6. `.test` links are safe but may still affect LLM perception.
7. Case-study scenarios are approximations, not exact reconstructions.
8. The output should not be used to claim real phishing prevalence or success rates.

For these reasons, the results should be interpreted as an exploratory comparison between scenarios and profiles, not as empirical measurement of real-world users.

---

## Suggested interpretation

A useful interpretation is not “this percentage represents the real world”. A better interpretation is:

> Under a given prompt, model, and scenario design, how do synthetic LLM agents distribute their reactions across different user profiles and phishing techniques?

The value of the project lies in comparing behaviors across conditions, identifying prompt/model limitations, and discussing how difficult it is to simulate human cybersecurity behavior with LLMs.

---

## Academic use

This project was developed as part of a Bachelor's thesis in Cybersecurity. It combines:

- social engineering analysis;
- cryptocurrency security;
- synthetic agent simulation;
- local LLM experimentation;
- exploratory data analysis.

---

## License and reuse

No explicit open-source license is provided unless one is later added to the repository. Without a license, reuse is limited by default copyright rules. The project is shared for academic review, transparency, and educational discussion.
