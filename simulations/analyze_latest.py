import argparse
import csv
import glob
import os
from collections import Counter, defaultdict


RESULTS_DIR = "results"


def latest_csv(results_dir: str) -> str:
    candidates = glob.glob(os.path.join(results_dir, "sim_*.csv"))
    if not candidates:
        raise FileNotFoundError(f"Nessun CSV trovato in {results_dir!r}")
    return max(candidates, key=os.path.getmtime)


def read_rows(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def is_true(value) -> bool:
    return str(value).strip().lower() == "true"


def archetype_from_agent(agent_id: str) -> str:
    if "_" not in agent_id:
        return agent_id
    prefix, suffix = agent_id.rsplit("_", 1)
    return prefix if suffix.isdigit() else agent_id


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


def main():
    parser = argparse.ArgumentParser(description="Analizza l'ultimo CSV generato dalla simulazione.")
    parser.add_argument("--file", default=None, help="CSV specifico da analizzare. Default: ultimo in results/.")
    parser.add_argument("--results-dir", default=RESULTS_DIR, help="Directory dei risultati.")
    args = parser.parse_args()

    path = args.file or latest_csv(args.results_dir)
    rows = read_rows(path)
    total = len(rows)

    decision_counter = Counter(row.get("decision", "") for row in rows)
    action_counter = Counter(row.get("specific_action", "") for row in rows)
    parse_errors = sum(is_true(row.get("parse_error")) for row in rows)

    phishing_rows = [row for row in rows if row.get("message_type") == "phishing"]
    legitimate_rows = [row for row in rows if row.get("message_type") == "legittimo"]
    phishing_compromised = sum(is_true(row.get("compromised")) for row in phishing_rows)
    legitimate_compromised = sum(is_true(row.get("compromised")) for row in legitimate_rows)
    false_positive_reports = sum(is_true(row.get("false_positive_report")) for row in legitimate_rows)
    legitimate_completion = sum(is_true(row.get("legitimate_completion")) for row in legitimate_rows)

    by_scenario = defaultdict(lambda: {"rows": 0, "compromised": 0, "reported": 0, "verified": 0})
    for row in rows:
        item = by_scenario[row.get("message_id", "")]
        item["rows"] += 1
        item["compromised"] += int(is_true(row.get("compromised")))
        item["reported"] += int(is_true(row.get("reported")))
        item["verified"] += int(is_true(row.get("verified")))

    decisions_by_archetype = Counter()
    for row in rows:
        key = (archetype_from_agent(row.get("agent_id", "")), row.get("decision", ""))
        decisions_by_archetype[key] += 1

    motivation_counter = Counter(row.get("motivation", "").strip() for row in rows if row.get("motivation", "").strip())

    print(f"File analizzato: {path}")
    print(f"Righe totali: {total}")
    rate = (parse_errors / total * 100) if total else 0
    print(f"Parse error rate: {parse_errors}/{total} ({rate:.2f}%)")

    print_counter("1. Distribuzione decisioni", decision_counter)
    print_counter("2. Distribuzione azioni specifiche", action_counter)

    phishing_rate = (phishing_compromised / len(phishing_rows) * 100) if phishing_rows else 0
    print("\n3. Compromissione solo sui phishing")
    print(f"  phishing compromised: {phishing_compromised}/{len(phishing_rows)} ({phishing_rate:.2f}%)")

    print("\n4. Controllo messaggi legittimi")
    print(f"  legittimi compromised: {legitimate_compromised}/{len(legitimate_rows)}")
    print(f"  false positive report: {false_positive_reports}/{len(legitimate_rows)}")
    print(f"  legitimate completion: {legitimate_completion}/{len(legitimate_rows)}")
    if legitimate_compromised:
        print("  WARNING: compromised sui messaggi legittimi dovrebbe essere sempre 0")

    scenario_rows = [
        (
            scenario,
            values["rows"],
            values["compromised"],
            values["reported"],
            values["verified"],
        )
        for scenario, values in sorted(by_scenario.items())
    ]
    print_table("5. Compromissione per scenario: scenario | righe | compromised | reported | verified", scenario_rows)

    archetype_rows = [
        (archetype, decision, count)
        for (archetype, decision), count in decisions_by_archetype.most_common()
    ]
    print_table("6. Decisioni per profilo/archetipo: archetipo | decision | conteggio", archetype_rows)

    print("\n7. Parse error rate")
    print(f"  {parse_errors}/{total} ({rate:.2f}%)")

    motivation_rows = [
        (motivation[:140], count)
        for motivation, count in motivation_counter.most_common(10)
    ]
    print_table("8. Top motivazioni: motivazione | conteggio", motivation_rows)


if __name__ == "__main__":
    main()
