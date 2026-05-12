# Crypto Phishing Simulation Thesis

## Overview

This repository contains the experimental component of a Bachelor's thesis in Cybersecurity focused on cryptocurrency-related phishing, social engineering, and user manipulation attacks.

The project implements a controlled simulation in which synthetic user profiles interact with phishing and legitimate messages related to cryptocurrency ecosystems. Each interaction is evaluated by a locally hosted Large Language Model (LLM) through Ollama.

Agent responses are modeled in two levels: initial reaction to the message and final action, so the simulation separates simple engagement from actual compromise.

The objective is not to create offensive tooling or realistic phishing infrastructure, but to study how different user characteristics and message properties may influence risky or defensive behavior.

---

## Important Disclaimer

This repository is intended exclusively for:

- academic research;
- cybersecurity education;
- behavioral simulation;
- phishing awareness analysis.

The project:

- does NOT perform real phishing;
- does NOT collect credentials;
- does NOT contact real users;
- does NOT interact with real wallets;
- does NOT use real malicious infrastructure;
- does NOT automate attacks.

All scenarios are synthetic and isolated inside a local simulation environment.

---

# Research Context

The broader thesis investigates how social engineering attacks exploit human behavior in cryptocurrency ecosystems.

Many successful cryptocurrency attacks do not directly compromise blockchain protocols. Instead, attackers exploit:

- urgency;
- fear;
- trust;
- cognitive overload;
- impersonation;
- poor operational security;
- account recovery flows;
- remote assistance scams;
- fake support interactions.

This repository provides a reproducible framework to experimentally simulate these dynamics.

---

# Research Objectives

The project aims to explore:

- how different synthetic users react to phishing attempts;
- how urgency and personalization influence behavior;
- how security awareness affects simulated decision-making;
- how cryptocurrency experience changes attack susceptibility;
- how initial engagement differs from final compromise;
- how users react differently to legitimate and malicious messages;
- how targeted social engineering attacks affect high-value profiles;
- how LLM-based agents can be used in exploratory behavioral cybersecurity research.

The experiment is exploratory and comparative. It is NOT intended to estimate real-world phishing rates.

---

# Repository Structure

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
│   └── generated locally (ignored by Git)
│
├── analysis.ipynb
├── requirements.txt
├── README.md
├── README_IT.md
└── .gitignore
```

---

# Main Components

## `agents/`

Contains synthetic user archetypes.

Each archetype defines:

- age;
- age group;
- role;
- cryptocurrency experience;
- security training;
- environment;
- behavioral traits.

The simulation expands each archetype into multiple synthetic instances with small controlled variations.

---

## `scenarios/`

Contains phishing and legitimate message templates.

Each scenario includes:

- scenario ID;
- message type;
- communication channel;
- text content;
- urgency level;
- personalization level;
- perceived reward;
- optional case-study metadata.

All suspicious links use safe `.test` domains.

---

## `simulations/`

Contains the simulation engine.

The script:

1. loads archetypes;
2. generates synthetic agents;
3. loads scenarios;
4. sends prompts to a local LLM through Ollama;
5. normalizes outputs;
6. stores results in CSV format.

---

## `analysis.ipynb`

Contains the analysis workflow.

The notebook:

- loads the latest CSV;
- computes phishing metrics;
- separates phishing and legitimate scenarios;
- analyzes background/context variables;
- analyzes behavioral traits;
- generates tables and plots;
- computes case-study-specific metrics.

---

# Synthetic Agent Generation

Each archetype is expanded into multiple synthetic instances.

The goal is to avoid rigid stereotype-like agents.

For example:

```text
teen_gamer_lowsec_1
teen_gamer_lowsec_2
teen_gamer_lowsec_3
```

All share the same general identity, but differ slightly in:

- impulsiveness;
- attention level;
- trust in brands;
- technical competence;
- risk aversion;
- security awareness;
- personal context.

This introduces limited intra-archetype variability while preserving interpretability.

---

# Behavioral Traits

The simulation models several behavioral dimensions.

## `impulsiveness`

Represents how quickly an agent reacts without careful evaluation.

Possible values:

```text
molto_bassa
bassa
media
alta
molto_alta
```

---

## `trust_in_brands`

Represents how easily the agent trusts messages that appear to come from known companies, exchanges or services.

---

## `tech_savvy`

Represents technical competence and familiarity with digital systems.

This does NOT necessarily imply good security awareness.

---

## `attention_level`

Represents how carefully the agent evaluates messages and details.

---

## `risk_aversion`

Represents how cautious the agent is regarding financial or operational risks.

---

# Individual Background Variants

Each generated agent also receives a small contextual background.

Examples:

- recently watched cybersecurity content;
- distracted by multitasking;
- previously exposed to phishing attempts;
- tends to trust known brands;
- curious about crypto opportunities;
- verifies URLs frequently;
- often acts in a hurry.

These backgrounds help reduce unrealistic behavioral rigidity.

---

# Simulation Parameters

The simulation includes several important parameters.

---

## Fixed Random Seed

```python
RANDOM_SEED = 42
```

The fixed seed ensures reproducibility.

It controls Python-generated randomness such as:

- age variations;
- trait shifts;
- background assignment;
- synthetic profile expansion.

Using a fixed seed allows different runs to remain comparable.

---

## Temperature

```python
"temperature": 0.4
```

Temperature controls response variability in the LLM.

Lower values:
- produce more deterministic outputs;
- reduce variability.

Higher values:
- increase randomness;
- produce more diverse behavior.

A value of `0.4` was selected as a compromise between consistency and behavioral diversity.

---

## Ollama JSON Mode

The simulation uses:

```python
"format": "json"
```

This forces the model to generate structured JSON responses.

Advantages:
- fewer parsing errors;
- cleaner outputs;
- more stable CSV generation;
- easier normalization.

---

# LLM Configuration

The simulation uses Ollama as a local inference engine.

Recommended model:

```text
llama3.2:3b
```

The project originally used `llama3`, but smaller models significantly improve simulation speed while maintaining acceptable behavioral consistency.

---

# Ollama Installation

Install Ollama from:

```text
https://ollama.com
```

Pull the recommended model:

```bash
ollama pull llama3.2:3b
```

Verify installation:

```bash
ollama run llama3.2:3b "Hello"
```

---

# Running the Simulation

Run:

```bash
python simulations/run_simulation.py
```

Each execution creates a new CSV file:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

Previous results are never overwritten.

---

# Output Variables

Each CSV row represents one agent-message interaction.

The CSV includes:

| Column | Meaning |
|---|---|
| `agent_id` | Synthetic agent identifier |
| `age` | Agent age |
| `age_group` | Agent age category |
| `role` | Synthetic role |
| `crypto_experience` | Crypto familiarity |
| `security_training` | Security awareness level |
| `environment` | Typical usage context |
| `background` | Individual contextual variation |
| `message_id` | Scenario identifier |
| `message_type` | `phishing` or `legittimo` |
| `channel` | Communication channel |
| `urgency` | Perceived urgency |
| `personalization` | Personalization level |
| `reward` | Perceived benefit |
| `raw_initial_reaction` | Raw initial reaction produced by the model |
| `initial_reaction` | Normalized initial reaction |
| `raw_final_action` | Raw final action produced by the model |
| `final_action` | Normalized final action |
| `engaged` | The agent produces an active response instead of ignoring the message |
| `compromised` | The final action exposes an account, wallet, device or funds |
| `reported` | The message is reported as phishing |
| `verified` | The message is checked through a trusted channel |
| `motivation` | LLM explanation |
| `parse_error` | Parsing failure flag |

---

# Possible Reactions and Actions

The simulation uses a two-level response. The first level captures the initial reaction to the message; the second level captures the eventual final action.

## Initial Reaction

```text
IGNORA
APRE_MESSAGGIO_O_LINK
SEGNALA_SUBITO
VERIFICA_SUBITO
PARSE_ERROR
```

## Final Action

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

---

## Reaction and Action Meaning

| Initial reaction | Meaning |
|---|---|
| `IGNORA` | Ignores the message |
| `APRE_MESSAGGIO_O_LINK` | Opens the message or link; this alone does not imply compromise |
| `SEGNALA_SUBITO` | Reports the message without proceeding |
| `VERIFICA_SUBITO` | Checks through a trusted channel without proceeding |
| `PARSE_ERROR` | Technical parsing failure |

| Final action | Meaning |
|---|---|
| `NESSUNA_AZIONE_ULTERIORE` | Takes no further action after the initial reaction |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | Connects wallet or approves transaction |
| `INSERISCE_CREDENZIALI_O_SEED` | Enters credentials or seed phrase |
| `CONCEDE_ACCESSO_REMOTO` | Grants remote access or screen sharing |
| `INVIA_FONDI` | Sends cryptocurrency |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | Verifies through trusted channels |
| `SEGNALA_COME_PHISHING` | Reports phishing |
| `PARSE_ERROR` | Technical parsing failure |

---

# Case Study Extension

The simulation includes scenarios inspired by the cryptocurrency theft case study analyzed in the thesis.

The modeled attack patterns include:

- fake support interactions;
- account compromise warnings;
- urgency and pressure;
- remote assistance scams;
- security verification requests.

The repository also includes a synthetic high-value crypto holder archetype inspired by the type of victim discussed in the case study.

The scenarios are inspired by public information and are NOT verbatim reconstructions of real attacker communications.

---

# Metrics

The notebook computes several metrics.

---

## Engagement Rate

Percentage of phishing messages where the agent does not ignore the message and produces an active response.

---

## Opened/Clicked Rate

Percentage of phishing messages where the agent opens the message or link. This metric measures initial interaction, not compromise.

---

## Wallet/Transaction Approval Rate

Percentage of phishing messages where the agent connects a wallet or approves a transaction.

---

## Credential Disclosure Rate

Percentage of phishing messages where the agent enters credentials, OTP codes or seed phrases.

---

## Remote Access Rate

Percentage of phishing messages where the agent grants remote access or screen sharing.

---

## Fund Transfer Rate

Percentage of phishing messages where the agent sends funds.

---

## Compromise Rate

Percentage of phishing messages where the agent performs a clearly dangerous final action.

Dangerous actions include:

- wallet connection;
- transaction approval;
- credential disclosure;
- seed disclosure;
- remote access;
- fund transfer.

---

## Loose Failure Rate

Percentage of phishing messages where the agent performs any risky interaction, including opening/clicking or final compromise.

---

## Reporting Rate

Percentage of phishing messages reported as phishing.

---

## Verification Rate

Percentage of phishing messages verified through trusted channels.

---

# Running the Analysis

Launch Jupyter:

```bash
jupyter lab
```

Open:

```text
analysis.ipynb
```

Run all cells.

The notebook automatically loads the latest simulation CSV.

Plots and tables are exported to:

```text
results/plots/
```

---

# Performance Notes

Simulation speed depends mainly on:

- model size;
- prompt length;
- GPU usage;
- number of interactions.

Using:

```text
llama3.2:3b
```

significantly improves speed compared to larger models.

---

# Ethical Considerations

This repository does NOT contain:

- malware;
- phishing kits;
- credential stealers;
- real attack infrastructure;
- exploit automation;
- offensive tooling.

All scenarios are synthetic and isolated.

The project is intended exclusively for defensive and academic purposes.

---

# Limitations

Several important limitations exist.

1. Synthetic agents are not real humans.

2. The simulation is not statistically representative.

3. LLMs may exhibit safety bias.

4. Prompt wording strongly influences behavior.

5. Different models may produce different outcomes.

6. The case-study scenarios are modeled approximations.

7. Human psychology cannot be fully reproduced through synthetic agents.

These limitations are explicitly discussed in the thesis.

---

# Academic Context

Developed as part of a Bachelor's thesis in Cybersecurity at the University of Milan.

The project combines:
- social engineering analysis;
- cryptocurrency security;
- behavioral simulation;
- local LLM experimentation.

---

# License

This repository is intended for educational and academic use.
