# Crypto Phishing Simulation Thesis

This repository contains the experimental component of a Bachelor's thesis in Cybersecurity focused on phishing, social engineering, and cryptocurrency-related fraud.

The project implements a controlled **agent-based simulation** in which synthetic user profiles interact with phishing and legitimate messages related to cryptocurrency ecosystems. The objective is to analyze how different user characteristics, message features, and security-awareness levels may influence risky or defensive behavior.

> **Important:** this project is intended exclusively for educational and academic research purposes.  
> It does not perform real phishing, does not collect credentials, and does not interact with real users or real malicious infrastructure.

---

## Thesis Context

The broader thesis investigates the relationship between cryptocurrencies and social engineering attacks, with particular attention to how human vulnerabilities can be exploited in blockchain and crypto-related environments.

Although blockchain systems are often technically robust, many successful attacks do not directly break the underlying protocol. Instead, they exploit users, communication channels, trust relationships, poor security awareness, and operational mistakes.

This repository supports the experimental part of the thesis by providing a reproducible framework to simulate user reactions to different phishing scenarios.

---

## Research Objective

The main objective of this project is to build a controlled simulation environment to study:

- how different synthetic user profiles react to phishing attempts;
- how message characteristics such as urgency, reward, impersonation, or technical language influence behavior;
- how security training and cryptocurrency experience affect simulated decision-making;
- how phishing messages differ from legitimate messages in terms of user response;
- how LLM-based agents can be used as an exploratory tool for behavioral cybersecurity research.

The simulation is **not** intended to estimate real-world phishing susceptibility rates. Instead, it is designed as an exploratory framework for comparing behavioral patterns across profiles and scenarios.

---

## Methodological Note

The agents used in this project are synthetic profiles generated from predefined archetypes. They are not real users and do not represent a statistically valid population sample.

Therefore, the results should not be interpreted as direct measurements of real human behavior. The experiment is useful for observing relative differences between scenarios, user archetypes, and message features under controlled conditions.

The simulation distinguishes between several levels of interaction, including:

- ignoring a message;
- opening a link;
- verifying the message through an official channel;
- reporting a message as phishing;
- connecting a wallet or approving a transaction;
- inserting credentials or seed phrases;
- sending funds.

This distinction is important because opening a link does not necessarily imply a full compromise. In real-world phishing campaigns, compromise usually occurs only after additional risky actions such as entering credentials, approving a malicious transaction, sharing a seed phrase, installing malware, or sending funds.

---

## Repository Structure

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
│   └── generated locally, ignored by Git
│
├── analysis.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Project Components

### `agents/`

Contains the synthetic user archetypes used in the simulation. Each archetype describes a user profile through variables such as:

- age;
- age group;
- role;
- cryptocurrency experience;
- security training;
- typical usage environment;
- impulsiveness;
- trust in brands;
- technical competence;
- attention level;
- risk aversion.

The simulation expands each archetype into multiple synthetic agents by applying small controlled variations.

### `scenarios/`

Contains phishing and legitimate message templates. Each scenario includes:

- message identifier;
- message type;
- communication channel;
- textual content;
- urgency level;
- personalization level;
- reward level.

All scenarios are synthetic. Potentially suspicious URLs use safe `.test` domains to avoid referencing or promoting real malicious infrastructure.

### `simulations/`

Contains the main simulation script. The script:

1. loads user archetypes;
2. expands them into synthetic agents;
3. loads message scenarios;
4. sends each agent-message pair to a local LLM through Ollama;
5. parses and normalizes the model response;
6. stores the results in a CSV file.

### `analysis.ipynb`

Contains the data analysis workflow used to process the generated CSV files. The notebook computes metrics such as:

- phishing click rate;
- strict compromise rate;
- loose failure rate;
- reporting rate;
- verification rate;
- false positive rate on legitimate messages.

It also generates summary tables and plots for thesis discussion.

---

## Requirements

The project requires Python 3.10 or later.

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

The current dependencies are:

```text
requests
pandas
matplotlib
seaborn
jupyter
```

The simulation also requires a local Ollama installation.

---

## LLM Setup with Ollama

Install Ollama from:

```text
https://ollama.com
```

Then download the model used by the simulation:

```bash
ollama pull llama3
```

Test that the model works:

```bash
ollama run llama3 "Hello"
```

The simulation uses Ollama's local API endpoint:

```text
http://localhost:11434/api/generate
```

Make sure Ollama is running before launching the simulation.

---

## Running the Simulation

From the root directory of the project, run:

```bash
python simulations/run_simulation.py
```

The script generates a CSV file inside the `results/` directory:

```text
results/sim_YYYYMMDD_HHMMSS.csv
```

Each execution creates a new file and does not overwrite previous results.

The CSV includes metadata such as:

- run identifier;
- model name;
- agent profile;
- message scenario;
- message features;
- raw LLM choice;
- normalized choice;
- parsing status;
- motivation;
- raw model response.

---

## Output Actions

The simulation asks each synthetic agent to choose exactly one action:

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

| Action | Meaning |
|---|---|
| `IGNORA` | The agent ignores the message. |
| `APRE_LINK` | The agent opens the link but does not perform further risky actions. |
| `COLLEGA_WALLET_O_APPROVA_TRANSAZIONE` | The agent connects a wallet or approves a potentially malicious transaction. |
| `INSERISCE_CREDENZIALI_O_SEED` | The agent enters credentials, OTP codes, seed phrases, or other sensitive information. |
| `INVIA_FONDI` | The agent sends cryptocurrency to an address indicated by the message. |
| `VERIFICA_TRAMITE_CANALE_UFFICIALE` | The agent verifies the message through an official website, app, support channel, or trusted expert. |
| `SEGNALA_COME_PHISHING` | The agent reports or classifies the message as phishing. |
| `PARSE_ERROR` | The model response could not be parsed or normalized correctly. |

`PARSE_ERROR` values are treated as technical errors and should be excluded from behavioral analysis.

---

## Running the Analysis

After generating at least one simulation CSV, open JupyterLab:

```bash
jupyter lab
```

Then open:

```text
analysis.ipynb
```

Run all cells:

```text
Run → Run All Cells
```

The notebook automatically loads the most recent CSV file from the `results/` directory and produces summary statistics and plots.

Generated plots are saved locally under:

```text
results/plots/
```

---

## Metrics

The analysis separates phishing messages from legitimate messages.

For phishing scenarios, the main metrics are:

| Metric | Description |
|---|---|
| Click rate | Percentage of phishing messages where the agent opened the link. |
| Strict compromise rate | Percentage of phishing messages where the agent performed a clearly compromising action. |
| Loose failure rate | Percentage of phishing messages where the agent performed any risky interaction. |
| Reporting rate | Percentage of phishing messages reported as phishing. |
| Verification rate | Percentage of phishing messages verified through official or trusted channels. |

For legitimate messages, the analysis focuses on:

| Metric | Description |
|---|---|
| Legitimate interaction rate | Percentage of legitimate messages where the agent interacted normally. |
| False positive rate | Percentage of legitimate messages incorrectly reported as phishing. |

---

## Reproducibility

The simulation uses a fixed random seed for deterministic profile expansion:

```python
RANDOM_SEED = 42
```

The model generation parameters are also configured in the simulation script.

Each CSV file stores the `run_id` and the model name, making it easier to compare different runs, prompts, or models.

---

## Ethical and Safety Considerations

This repository does not include or support:

- real phishing infrastructure;
- credential harvesting;
- malware;
- real malicious domains;
- real victims;
- real wallet interaction;
- automated attacks;
- offensive exploitation tools.

All phishing messages are synthetic and used only in a local, controlled simulation environment.

The purpose of the project is to support cybersecurity education, awareness, and academic research.

---

## Limitations

This project has several important limitations:

1. **Synthetic agents are not real users.**  
   Their behavior is generated by an LLM and depends on prompt design, model behavior, and simulation parameters.

2. **The results are not statistically representative.**  
   The synthetic profiles do not constitute a population sample and should not be interpreted as real-world phishing susceptibility rates.

3. **LLMs may show safety bias.**  
   The model may recognize obvious phishing indicators more easily than average users, especially in scenarios involving seed phrases or credentials.

4. **The simulation is exploratory.**  
   Its value lies in comparing scenarios, profiles, and behavioral patterns, not in estimating exact real-world percentages.

5. **Prompt design influences results.**  
   Different wording, models, temperatures, or action definitions may produce different outcomes.

These limitations are explicitly considered in the thesis discussion.

---

## Academic Use

This repository was developed as part of a Bachelor's thesis in Cybersecurity at the University of Milan.

The experimental framework is intended to complement the theoretical analysis of cryptocurrency-related social engineering attacks by providing a controlled, reproducible simulation environment.

---

## Disclaimer

This project is provided for educational and research purposes only.

The author does not endorse, enable, or encourage phishing, fraud, credential theft, or any form of unauthorized access. All scenarios are synthetic and designed exclusively for safe academic experimentation.
