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
- the difference between opening a message/link and performing a dangerous follow-up action;
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
│   └── run_simulation.py
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

The LLM remains the decision-maker. The Python script does not randomly choose whether an agent ignores, opens, verifies, reports, or performs an operational action.

For each agent-message pair, Python builds a prompt containing:

- the agent profile;
- behavioral traits;
- situational background;
- the message text;
- the allowed initial reactions;
- the allowed final actions;
- logical consistency rules.

The model must return JSON with:

```json
{
  "initial_reaction": "...",
  "final_action": "...",
  "motivation": "..."
}
```

The prompt explicitly asks the model to simulate an imperfect human user, not a cybersecurity advisor. This is important because general-purpose LLMs often show a strong safety bias and may otherwise behave like ideal security-aware users.

---

## Two-level response structure

The simulation separates the first reaction from the final outcome.

This distinction is essential because opening a message or link is not the same as compromising an account, wallet, device, or funds.

### Initial reactions

```text
IGNORA
APRE_MESSAGGIO_O_LINK
SEGNALA_SUBITO
VERIFICA_SUBITO
PARSE_ERROR
```

| Initial reaction | Meaning |
|---|---|
| `IGNORA` | The agent ignores the message |
| `APRE_MESSAGGIO_O_LINK` | The agent opens the message or link; this alone does not imply compromise |
| `SEGNALA_SUBITO` | The agent reports the message immediately |
| `VERIFICA_SUBITO` | The agent checks through a trusted channel before proceeding |
| `PARSE_ERROR` | Technical parsing or output validation failure |

### Final actions

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

| Final action | Meaning |
|---|---|
| `NESSUNA_AZIONE_ULTERIORE` | The agent does not proceed further |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | The agent connects a wallet or approves a transaction/signature |
| `INSERISCE_CREDENZIALI_O_SEED` | The agent enters credentials, OTPs, private keys, or seed phrase |
| `CONCEDE_ACCESSO_REMOTO` | The agent grants remote access or screen sharing |
| `INVIA_FONDI` | The agent sends cryptocurrency funds |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | The agent verifies through trusted/official channels |
| `SEGNALA_COME_PHISHING` | The agent reports the message as phishing |
| `PARSE_ERROR` | Technical parsing or output validation failure |

### Logical rules

The script enforces consistency rules after parsing:

- if `initial_reaction` is `IGNORA`, `final_action` becomes `NESSUNA_AZIONE_ULTERIORE`;
- if `initial_reaction` is `SEGNALA_SUBITO`, `final_action` becomes `SEGNALA_COME_PHISHING`;
- if `initial_reaction` is `VERIFICA_SUBITO`, `final_action` becomes `VERIFICA_TRAMITE_CANALE_UFFICIALE`.

This normalization avoids inconsistent outputs without making Python the behavioral decision-maker.

---

## Simulation parameters

### Ollama model

```python
OLLAMA_MODEL = "llama3.2:3b"
```

The project uses a local Ollama model. `llama3.2:3b` is a practical choice for running many interactions locally while keeping execution time manageable.

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
TEMPERATURE = 0.7
```

Temperature controls variability in LLM responses.

Lower values make outputs more deterministic and repetitive. Higher values increase behavioral variety but can reduce consistency. A value of `0.7` is used to encourage plausible variation between agents while still keeping responses structured.

### JSON mode

The Ollama request uses:

```python
"format": "json"
```

This reduces parsing errors by encouraging the model to return valid JSON.

---

## Output CSV

Each row in the output CSV represents one interaction between one synthetic agent and one scenario.

Main output columns include:

| Column | Meaning |
|---|---|
| `run_id` | Timestamp identifier of the run |
| `model` | Ollama model used |
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
| `raw_initial_reaction` | Raw LLM initial reaction before normalization |
| `initial_reaction` | Normalized initial reaction |
| `raw_final_action` | Raw LLM final action before normalization |
| `final_action` | Normalized final action |
| `engaged` | `True` if the agent did not simply ignore the message |
| `compromised` | `True` if the final action exposes funds, accounts, wallet, or device |
| `reported` | `True` if the agent reports the message |
| `verified` | `True` if the agent verifies through a trusted channel |
| `parse_error` | `True` if parsing or label validation failed |
| `motivation` | Short LLM-generated reason |
| `raw_response` | Raw model response |

---

## Metrics computed in the notebook

The notebook computes metrics such as:

| Metric | Meaning |
|---|---|
| Engagement rate | Percentage of phishing messages not ignored |
| Open/click rate | Percentage of phishing messages opened/clicked |
| Wallet/transaction approval rate | Percentage leading to wallet connection or transaction approval |
| Credential/seed disclosure rate | Percentage leading to credential or seed entry |
| Remote access rate | Percentage leading to remote access or screen sharing |
| Fund transfer rate | Percentage leading to cryptocurrency transfer |
| Compromise rate | Percentage involving a clearly dangerous final action |
| Loose failure rate | Broader measure including opening/clicking and final compromise |
| Reporting rate | Percentage reported as phishing |
| Verification rate | Percentage verified through trusted channels |
| Legitimate interaction rate | Percentage of legitimate messages handled through normal interaction or verification |
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
ollama pull llama3.2:3b
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

Run all cells. The notebook loads the latest simulation CSV from `results/`, computes metrics, displays tables, and exports plots/tables under the results directory.

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

The default setup produces 960 LLM calls. On consumer hardware this can take a significant amount of time. Smaller local models such as `llama3.2:3b` are generally faster than larger models.

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
