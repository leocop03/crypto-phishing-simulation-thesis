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

FLOW_NO_ENTRY = "NON_ENTRA_NEL_FLOW"
FLOW_STOPPED = "SI_FERMA_PRIMA_DELLA_COMPROMISSIONE"
FLOW_COMPROMISED = "COMPROMISSIONE_COMPLETATA"
FLOW_LEGITIMATE = "AZIONE_LEGITTIMA_COMPLETATA"

NO_COMPROMISE_ACTION = "NESSUNA"

FORBIDDEN_LABELS = [
    "APRE_" + "MESSAGGIO_O_LINK",
    "CLICCA_" + "LINK_SENZA_INSERIRE_DATI",
]

FLOW_ORDER = [
    FLOW_NO_ENTRY,
    FLOW_STOPPED,
    FLOW_COMPROMISED,
    FLOW_LEGITIMATE,
    "PARSE_ERROR",
]

COMPROMISE_ACTION_ORDER = [
    NO_COMPROMISE_ACTION,
    "INSERISCE_CREDENZIALI",
    "INSERISCE_DATI_KYC",
    "INSERISCE_SEED_PHRASE",
    "COLLEGA_WALLET",
    "APPROVA_TRANSAZIONE",
    "CONCEDE_ACCESSO_REMOTO",
    "INVIA_FONDI",
    "INSTALLA_APP_O_SOFTWARE",
    "PARSE_ERROR",
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
    return str(value).strip().lower() in {"true", "1", "yes", "si"}


def pct(count: int, total: int) -> float:
    return (count / total * 100) if total else 0.0


def rate_text(count: int, total: int) -> str:
    return f"{count}/{total} ({pct(count, total):.2f}%)"


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


def infer_archetype_id(agent_id: str) -> str:
    agent_id = str(agent_id)
    if "_" not in agent_id:
        return agent_id
    prefix, suffix = agent_id.rsplit("_", 1)
    return prefix if suffix.isdigit() else agent_id


def normalize_rows(rows: list[dict]) -> list[dict]:
    normalized = []
    for row in rows:
        item = dict(row)
        item["message_type"] = normalize_message_type(item.get("message_type", ""))

        # Current-schema columns are primary. Historical aliases are fallback only.
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
                flow_outcome = FLOW_NO_ENTRY
            elif legitimate_completion:
                flow_outcome = FLOW_LEGITIMATE
            elif compromised:
                flow_outcome = FLOW_COMPROMISED
            else:
                flow_outcome = FLOW_STOPPED

        if not compromise_action:
            compromise_action = NO_COMPROMISE_ACTION

        if not decision and is_true(item.get("parse_error")):
            decision = "PARSE_ERROR"
        if not flow_outcome and is_true(item.get("parse_error")):
            flow_outcome = "PARSE_ERROR"
        if not compromise_action and is_true(item.get("parse_error")):
            compromise_action = "PARSE_ERROR"

        agent_id = row_value(item, "agent_id", "")
        item["agent_id"] = agent_id
        item["archetype_id"] = row_value(item, "archetype_id", infer_archetype_id(agent_id))
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
        item["validation_error_flag"] = bool(str(item.get("validation_error", "")).strip())
        normalized.append(item)

    return normalized


def unique_values(rows: list[dict], key: str) -> str:
    values = sorted({str(row.get(key, "")).strip() for row in rows if str(row.get(key, "")).strip()})
    if not values:
        return "non disponibile"
    if len(values) == 1:
        return values[0]
    return ", ".join(values)


def print_counter(title: str, counter: Counter, total: int):
    print(f"\n{title}")
    if not counter:
        print("  nessun dato")
        return
    for key, value in counter.most_common():
        print(f"  {key}: {value} ({pct(value, total):.2f}%)")


def print_rate(label: str, count: int, total: int):
    print(f"  {label}: {rate_text(count, total)}")


def print_table(title: str, headers: list[str], rows: list[list]):
    print(f"\n{title}")
    if not rows:
        print("  nessun dato")
        return
    print("  " + " | ".join(headers))
    for row in rows:
        print("  " + " | ".join(str(value) for value in row))


def summarize_group(rows: list[dict], key: str) -> list[list]:
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key, "")].append(row)

    table = []
    for group_key, group_rows in sorted(groups.items(), key=lambda item: str(item[0])):
        total = len(group_rows)
        phishing_total = sum(row.get("message_type") == PHISHING_TYPE for row in group_rows)
        compromised_phishing = sum(
            row["compromised"]
            for row in group_rows
            if row.get("message_type") == PHISHING_TYPE
        )
        table.append(
            [
                group_key,
                total,
                rate_text(sum(row["entered_flow"] for row in group_rows), total),
                rate_text(sum(row["stopped_before_compromise"] for row in group_rows), total),
                rate_text(compromised_phishing, phishing_total),
                rate_text(sum(row["verified"] for row in group_rows), total),
                rate_text(sum(row["reported"] for row in group_rows), total),
                rate_text(sum(row["ignored"] for row in group_rows), total),
                rate_text(sum(row["delayed"] for row in group_rows), total),
                rate_text(sum(row["legitimate_completion"] for row in group_rows), total),
            ]
        )
    return table


def ordered_columns(counter_by_group: dict[str, Counter], preferred_order: list[str]) -> list[str]:
    seen = set()
    columns = []
    for value in preferred_order:
        if any(value in counter for counter in counter_by_group.values()):
            columns.append(value)
            seen.add(value)
    extras = sorted(
        {
            value
            for counter in counter_by_group.values()
            for value in counter
            if value not in seen
        }
    )
    return columns + extras


def build_crosstab(rows: list[dict], group_key: str, value_key: str, preferred_order: list[str]):
    counter_by_group = defaultdict(Counter)
    for row in rows:
        counter_by_group[row.get(group_key, "")][row.get(value_key, "")] += 1

    columns = ordered_columns(counter_by_group, preferred_order)
    table = []
    for group, counter in sorted(counter_by_group.items(), key=lambda item: str(item[0])):
        table.append([group] + [counter.get(column, 0) for column in columns])
    return columns, table


def collect_warnings(rows: list[dict], message_config: dict[str, dict]) -> list[str]:
    warnings = []
    total = len(rows)
    parse_error_count = sum(row["parse_error"] for row in rows)
    validation_error_count = sum(row["validation_error_flag"] for row in rows)
    legitimate_rows = [row for row in rows if row.get("message_type") == LEGITIMATE_TYPE]
    phishing_rows = [row for row in rows if row.get("message_type") == PHISHING_TYPE]
    entered_phishing = [row for row in phishing_rows if row["entered_flow"]]

    if parse_error_count > 0:
        warnings.append(
            f"parse_error > 0 ({rate_text(parse_error_count, total)}): possibili risposte non interpretabili, interpretare con cautela."
        )

    if validation_error_count > 0:
        warnings.append(
            f"validation_error > 0 ({rate_text(validation_error_count, total)}): controllare schema, retry e compatibilita scenario."
        )

    legitimate_compromised = sum(row["compromised"] for row in legitimate_rows)
    if legitimate_compromised > 0:
        warnings.append(
            f"messaggi legittimi con compromised > 0 ({rate_text(legitimate_compromised, len(legitimate_rows))}): controllo di coerenza fallito."
        )

    for forbidden_label in FORBIDDEN_LABELS:
        if any(forbidden_label in str(value) for row in rows for value in row.values()):
            warnings.append(
                f"etichetta obsoleta ancora presente: {forbidden_label}."
            )

    reported_count = sum(row["reported"] for row in rows)
    if total and reported_count == 0:
        warnings.append(
            "SEGNALA_COME_PHISHING = 0: il modello potrebbe sottorappresentare la segnalazione; interpretare con cautela."
        )

    stopped_entered_phishing = sum(row["stopped_before_compromise"] for row in entered_phishing)
    if entered_phishing and pct(stopped_entered_phishing, len(entered_phishing)) >= 70:
        warnings.append(
            "possibile bias prudenziale: SI_FERMA_PRIMA_DELLA_COMPROMISSIONE e molto alto tra i phishing in cui l'utente entra nel flow."
        )

    decision_counter = Counter(row["decision"] for row in rows)
    if total and decision_counter:
        dominant_decision, dominant_count = decision_counter.most_common(1)[0]
        if pct(dominant_count, total) >= 70:
            warnings.append(
                f"possibile collasso comportamentale: {dominant_decision} domina il {pct(dominant_count, total):.2f}% delle righe."
            )

    timeout_rows = [
        row
        for row in rows
        if "timeout" in str(row.get("raw_response", "")).lower()
        or "timed out" in str(row.get("raw_response", "")).lower()
        or "timeout" in str(row.get("validation_error", "")).lower()
        or "timed out" in str(row.get("validation_error", "")).lower()
    ]
    if timeout_rows:
        warnings.append(
            f"timeout rilevati in raw_response o validation_error ({rate_text(len(timeout_rows), total)})."
        )

    incompatible_actions = []
    for row in phishing_rows:
        if row["compromise_action"] in {NO_COMPROMISE_ACTION, "PARSE_ERROR"}:
            continue
        possible_actions = message_config.get(row.get("message_id", ""), {}).get(
            "possible_compromise_actions",
            [],
        )
        if row["compromise_action"] not in possible_actions:
            incompatible_actions.append((row.get("message_id", ""), row["compromise_action"]))
    if incompatible_actions:
        sample = ", ".join(f"{message}:{action}" for message, action in incompatible_actions[:5])
        warnings.append(
            f"azioni di compromissione non compatibili con lo scenario: {sample}."
        )

    return warnings


def main():
    parser = argparse.ArgumentParser(description="Analizza l'ultimo CSV generato dalla simulazione.")
    parser.add_argument("--file", default=None, help="CSV specifico da analizzare. Default: ultimo in results/.")
    parser.add_argument("--results-dir", default=RESULTS_DIR, help="Directory dei risultati.")
    args = parser.parse_args()

    path = args.file or latest_csv(args.results_dir)
    rows = normalize_rows(read_rows(path))
    message_config = load_message_config(MESSAGES_PATH)
    total = len(rows)

    parse_error_count = sum(row["parse_error"] for row in rows)
    validation_error_count = sum(row["validation_error_flag"] for row in rows)

    phishing_rows = [row for row in rows if row.get("message_type") == PHISHING_TYPE]
    legitimate_rows = [row for row in rows if row.get("message_type") == LEGITIMATE_TYPE]

    decision_counter = Counter(row["decision"] for row in rows)
    flow_counter = Counter(row["flow_outcome"] for row in rows)
    compromise_counter = Counter(row["compromise_action"] for row in rows)

    entered_flow = sum(row["entered_flow"] for row in rows)
    stopped_before_compromise = sum(row["stopped_before_compromise"] for row in rows)
    compromised_phishing = sum(row["compromised"] for row in phishing_rows)
    compromised_legitimate = sum(row["compromised"] for row in legitimate_rows)
    verified = sum(row["verified"] for row in rows)
    reported = sum(row["reported"] for row in rows)
    ignored = sum(row["ignored"] for row in rows)
    delayed = sum(row["delayed"] for row in rows)
    legitimate_completion = sum(row["legitimate_completion"] for row in rows)

    print(f"File analizzato: {path}")
    print(f"Righe: {total}")
    print(f"Modello: {unique_values(rows, 'model')}")
    print(f"Temperature: {unique_values(rows, 'temperature')}")
    print(f"Parse error: {rate_text(parse_error_count, total)}")
    print(f"Validation error: {rate_text(validation_error_count, total)}")

    print_counter("Distribuzione decision", decision_counter, total)
    print_counter("Distribuzione flow_outcome", flow_counter, total)
    print_counter("Distribuzione compromise_action", compromise_counter, total)

    print("\nMetriche principali")
    print_rate("entered_flow rate", entered_flow, total)
    print_rate("stopped_before_compromise rate", stopped_before_compromise, total)
    print_rate("compromised rate sui soli phishing", compromised_phishing, len(phishing_rows))
    print_rate("compromised rate sui legittimi", compromised_legitimate, len(legitimate_rows))
    print_rate("verified rate", verified, total)
    print_rate("reported rate", reported, total)
    print_rate("ignored rate", ignored, total)
    print_rate("delayed rate", delayed, total)
    print_rate("legitimate_completion rate", legitimate_completion, total)

    group_headers = [
        "gruppo",
        "n",
        "entered",
        "stopped",
        "compromised phishing",
        "verified",
        "reported",
        "ignored",
        "delayed",
        "legitimate_completion",
    ]
    print_table(
        "Risultati per scenario",
        group_headers,
        summarize_group(rows, "message_id"),
    )
    print_table(
        "Risultati per archetipo",
        group_headers,
        summarize_group(rows, "archetype_id"),
    )

    flow_columns, flow_table = build_crosstab(rows, "message_id", "flow_outcome", FLOW_ORDER)
    print_table(
        "Scenario x flow_outcome",
        ["scenario"] + flow_columns,
        flow_table,
    )

    action_columns, action_table = build_crosstab(
        rows,
        "message_id",
        "compromise_action",
        COMPROMISE_ACTION_ORDER,
    )
    print_table(
        "Scenario x compromise_action",
        ["scenario"] + action_columns,
        action_table,
    )

    validation_errors = Counter(
        str(row.get("validation_error", "")).strip()
        for row in rows
        if str(row.get("validation_error", "")).strip()
    )
    if validation_errors:
        print_counter("Validation error piu frequenti", validation_errors, validation_error_count)

    warnings = collect_warnings(rows, message_config)
    print("\nWarning metodologici")
    if not warnings:
        print("  nessun warning")
    else:
        for warning in warnings:
            print(f"  WARNING: {warning}")


if __name__ == "__main__":
    main()
