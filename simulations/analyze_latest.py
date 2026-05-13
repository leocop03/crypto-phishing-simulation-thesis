import argparse
import csv
import glob
import json
import os
from collections import Counter, defaultdict


RESULTS_DIR = "results"
MESSAGES_PATH = os.path.join("scenarios", "messages.json")

PHISHING_TYPE = "phishing"
LEGITIMATE_TYPE = "legittimo"

DECISION_PROCEED = "PROCEDE_CON_LA_RICHIESTA"
DECISION_VERIFY = "VERIFICA_TRAMITE_CANALE_UFFICIALE"
DECISION_REPORT = "SEGNALA_COME_PHISHING"
DECISION_IGNORE = "IGNORA"
DECISION_DELAY = "RIMANDA_O_NON_DECIDE"

FLOW_STOPPED = "SI_FERMA_PRIMA_DELLA_COMPROMISSIONE"
FLOW_COMPROMISED = "COMPROMISSIONE_COMPLETATA"
FLOW_LEGITIMATE = "AZIONE_LEGITTIMA_COMPLETATA"

NO_COMPROMISE_ACTION = "NESSUNA"
FORBIDDEN_LABELS = [
    "APRE_" + "MESSAGGIO_O_LINK",
    "CLICCA_" + "LINK_SENZA_INSERIRE_DATI",
]


def latest_csv(results_dir: str) -> str:
    candidates = glob.glob(os.path.join(results_dir, "sim_*.csv"))
    if not candidates:
        raise FileNotFoundError(f"Nessun CSV trovato in {results_dir!r}")
    return max(candidates, key=os.path.getmtime)


def read_rows(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_message_config(path: str) -> dict[str, dict]:
    with open(path, "r", encoding="utf-8") as f:
        return {message["id"]: message for message in json.load(f)}


def is_true(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "si", "sì"}


def pct(count: int, total: int) -> float:
    return (count / total * 100) if total else 0.0


def archetype_from_agent(agent_id: str) -> str:
    if "_" not in agent_id:
        return agent_id
    prefix, suffix = agent_id.rsplit("_", 1)
    return prefix if suffix.isdigit() else agent_id


def normalize_message_type(value: str) -> str:
    mapping = {
        "legitimo": LEGITIMATE_TYPE,
        "legitimate": LEGITIMATE_TYPE,
        "legittima": LEGITIMATE_TYPE,
    }
    return mapping.get(str(value).strip().lower(), str(value).strip().lower())


def row_value(row: dict, key: str, fallback: str = "") -> str:
    value = row.get(key)
    if value is None or value == "":
        return fallback
    return value


def normalize_rows(rows: list[dict]) -> list[dict]:
    normalized = []
    for row in rows:
        item = dict(row)
        item["message_type"] = normalize_message_type(item.get("message_type", ""))

        decision = row_value(item, "decision", row_value(item, "initial_reaction", ""))
        flow_outcome = row_value(item, "flow_outcome", "")
        compromise_action = row_value(
            item,
            "compromise_action",
            row_value(item, "specific_action", row_value(item, "final_action", "")),
        )

        entered_flow = (
            is_true(item.get("entered_flow"))
            if "entered_flow" in item
            else decision == DECISION_PROCEED or is_true(item.get("proceeded"))
        )
        stopped_before_compromise = (
            is_true(item.get("stopped_before_compromise"))
            if "stopped_before_compromise" in item
            else flow_outcome == FLOW_STOPPED
        )
        compromised = is_true(item.get("compromised"))
        verified = (
            is_true(item.get("verified"))
            if "verified" in item
            else decision == DECISION_VERIFY
        )
        reported = (
            is_true(item.get("reported"))
            if "reported" in item
            else decision == DECISION_REPORT
        )
        ignored = (
            is_true(item.get("ignored"))
            if "ignored" in item
            else decision == DECISION_IGNORE
        )
        delayed = (
            is_true(item.get("delayed"))
            if "delayed" in item
            else decision == DECISION_DELAY
        )
        legitimate_completion = (
            is_true(item.get("legitimate_completion"))
            if "legitimate_completion" in item
            else flow_outcome == FLOW_LEGITIMATE
        )

        if not flow_outcome:
            if not entered_flow:
                flow_outcome = "NON_ENTRA_NEL_FLOW"
            elif legitimate_completion:
                flow_outcome = FLOW_LEGITIMATE
            elif compromised:
                flow_outcome = FLOW_COMPROMISED
            else:
                flow_outcome = FLOW_STOPPED

        if not compromise_action:
            compromise_action = NO_COMPROMISE_ACTION

        item["decision"] = decision
        item["flow_outcome"] = flow_outcome
        item["compromise_action"] = compromise_action
        item["entered_flow"] = entered_flow
        item["stopped_before_compromise"] = stopped_before_compromise
        item["compromised"] = compromised
        item["verified"] = verified
        item["reported"] = reported
        item["ignored"] = ignored
        item["delayed"] = delayed
        item["legitimate_completion"] = legitimate_completion
        item["parse_error"] = is_true(item.get("parse_error"))
        normalized.append(item)

    return normalized


def print_counter(title: str, counter: Counter):
    print(f"\n{title}")
    if not counter:
        print("  nessun dato")
        return
    for key, value in counter.most_common():
        print(f"  {key}: {value}")


def print_table(title: str, rows: list[tuple]):
    print(f"\n{title}")
    if not rows:
        print("  nessun dato")
        return
    for row in rows:
        print("  " + " | ".join(str(value) for value in row))


def rate_row(label: str, count: int, total: int) -> tuple:
    return (label, count, total, f"{pct(count, total):.2f}%")


def summarize_group(rows: list[dict], key_fn):
    groups = defaultdict(list)
    for row in rows:
        groups[key_fn(row)].append(row)

    table = []
    for key, group_rows in sorted(groups.items(), key=lambda item: str(item[0])):
        total = len(group_rows)
        table.append(
            (
                key,
                total,
                f"{pct(sum(row['entered_flow'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['stopped_before_compromise'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['compromised'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['reported'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['verified'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['ignored'] for row in group_rows), total):.2f}%",
                f"{pct(sum(row['delayed'] for row in group_rows), total):.2f}%",
            )
        )
    return table


def collect_warnings(rows: list[dict], valid_rows: list[dict], message_config: dict[str, dict]) -> list[str]:
    warnings = []
    phishing_rows = [row for row in valid_rows if row.get("message_type") == PHISHING_TYPE]
    legitimate_rows = [row for row in valid_rows if row.get("message_type") == LEGITIMATE_TYPE]

    if not any(row["decision"] == DECISION_REPORT for row in valid_rows):
        warnings.append("SEGNALA_COME_PHISHING = 0")

    proceed_phishing = sum(row["decision"] == DECISION_PROCEED for row in phishing_rows)
    if pct(proceed_phishing, len(phishing_rows)) > 80:
        warnings.append("PROCEDE_CON_LA_RICHIESTA supera l'80% sui phishing")

    rows_by_message = defaultdict(list)
    for row in phishing_rows:
        rows_by_message[row.get("message_id", "")].append(row)

    for message_id, group_rows in sorted(rows_by_message.items()):
        possible_actions = message_config.get(message_id, {}).get("possible_compromise_actions", [])
        if possible_actions and not any(row["flow_outcome"] == FLOW_COMPROMISED for row in group_rows):
            warnings.append(f"COMPROMISSIONE_COMPLETATA = 0 nello scenario {message_id}")

    legitimate_compromised = sum(row["compromised"] for row in legitimate_rows)
    if legitimate_compromised:
        warnings.append("Messaggi legittimi con compromised > 0")

    incompatible_actions = []
    for row in phishing_rows:
        action = row["compromise_action"]
        if action in {NO_COMPROMISE_ACTION, "PARSE_ERROR"}:
            continue
        possible_actions = message_config.get(row.get("message_id", ""), {}).get(
            "possible_compromise_actions",
            [],
        )
        if action not in possible_actions:
            incompatible_actions.append((row.get("message_id", ""), action))
    if incompatible_actions:
        sample = ", ".join(f"{message}:{action}" for message, action in incompatible_actions[:5])
        warnings.append(f"Azioni di compromissione incompatibili con lo scenario: {sample}")

    for forbidden_label in FORBIDDEN_LABELS:
        if any(forbidden_label in str(value) for row in rows for value in row.values()):
            warnings.append(f"Etichetta obsoleta ancora presente: {forbidden_label}")

    return warnings


def main():
    parser = argparse.ArgumentParser(description="Analizza l'ultimo CSV generato dalla simulazione.")
    parser.add_argument("--file", default=None, help="CSV specifico da analizzare. Default: ultimo in results/.")
    parser.add_argument("--results-dir", default=RESULTS_DIR, help="Directory dei risultati.")
    args = parser.parse_args()

    path = args.file or latest_csv(args.results_dir)
    rows = normalize_rows(read_rows(path))
    message_config = load_message_config(MESSAGES_PATH)
    valid_rows = [row for row in rows if not row["parse_error"]]
    total = len(rows)
    valid_total = len(valid_rows)

    phishing_rows = [row for row in valid_rows if row.get("message_type") == PHISHING_TYPE]
    legitimate_rows = [row for row in valid_rows if row.get("message_type") == LEGITIMATE_TYPE]

    parse_errors = total - valid_total
    decision_counter = Counter(row["decision"] for row in valid_rows)
    flow_counter = Counter(row["flow_outcome"] for row in valid_rows)
    compromise_counter = Counter(row["compromise_action"] for row in valid_rows)
    validation_errors = Counter(
        row.get("validation_error", "").strip()
        for row in rows
        if row["parse_error"] and row.get("validation_error", "").strip()
    )

    entered_flow = sum(row["entered_flow"] for row in valid_rows)
    stopped_before_compromise = sum(row["stopped_before_compromise"] for row in valid_rows)
    compromised_phishing = sum(row["compromised"] for row in phishing_rows)
    legitimate_compromised = sum(row["compromised"] for row in legitimate_rows)
    legitimate_completion = sum(row["legitimate_completion"] for row in legitimate_rows)
    reported = sum(row["reported"] for row in valid_rows)
    verified = sum(row["verified"] for row in valid_rows)
    ignored = sum(row["ignored"] for row in valid_rows)
    delayed = sum(row["delayed"] for row in valid_rows)

    print(f"File analizzato: {path}")
    print(f"Righe totali: {total}")
    print(f"Righe valide: {valid_total}")
    print(f"Parse error rate: {parse_errors}/{total} ({pct(parse_errors, total):.2f}%)")

    print_counter("1. Distribuzione decision", decision_counter)
    print_counter("2. Distribuzione flow_outcome", flow_counter)
    print_counter("3. Distribuzione compromise_action", compromise_counter)

    metric_rows = [
        rate_row("entered_flow rate", entered_flow, valid_total),
        rate_row("stopped_before_compromise rate", stopped_before_compromise, valid_total),
        rate_row("compromised rate sui phishing", compromised_phishing, len(phishing_rows)),
        rate_row("messaggi legittimi compromised", legitimate_compromised, len(legitimate_rows)),
        rate_row("legitimate_completion sui legittimi", legitimate_completion, len(legitimate_rows)),
        rate_row("reported rate", reported, valid_total),
        rate_row("verified rate", verified, valid_total),
        rate_row("ignored rate", ignored, valid_total),
        rate_row("delayed rate", delayed, valid_total),
    ]
    print_table("4. Metriche principali: metrica | count | totale | percentuale", metric_rows)

    scenario_rows = summarize_group(valid_rows, lambda row: row.get("message_id", ""))
    print_table(
        "5. Risultati per scenario: scenario | n | entered | stopped | compromised | reported | verified | ignored | delayed",
        scenario_rows,
    )

    archetype_rows = summarize_group(
        valid_rows,
        lambda row: archetype_from_agent(row.get("agent_id", "")),
    )
    print_table(
        "6. Risultati per archetipo: archetipo | n | entered | stopped | compromised | reported | verified | ignored | delayed",
        archetype_rows,
    )

    if validation_errors:
        print_counter("7. Validation error piu frequenti", validation_errors)

    warnings = collect_warnings(rows, valid_rows, message_config)
    print("\nWarning")
    if not warnings:
        print("  nessun warning")
    else:
        for warning in warnings:
            print(f"  WARNING: {warning}")


if __name__ == "__main__":
    main()
