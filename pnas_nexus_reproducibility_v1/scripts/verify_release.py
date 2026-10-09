#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from release_tools.cohorts import validate_public_cohort_summary

PERSON_COLUMNS = {
    "uuid", "participant_id", "original_uuid", "email", "full_name",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_manuscript_assets() -> list[str]:
    failures: list[str] = []
    manuscript = ROOT / "manuscript"
    figure_pattern = re.compile(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}")
    input_pattern = re.compile(r"\\input\{(source_tables/[^}]+)\}")
    expected_counts = {"main.tex": (6, 0), "supplement.tex": (21, 21)}
    for name, expected in expected_counts.items():
        path = manuscript / name
        if not path.is_file():
            failures.append(f"missing manuscript source: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        figures = figure_pattern.findall(text)
        tables = input_pattern.findall(text)
        if (len(figures), len(tables)) != expected:
            failures.append(
                f"asset-reference count mismatch in {name}: "
                f"{len(figures)} figures, {len(tables)} tables"
            )
        for relative in figures:
            if not (manuscript / "figures" / relative).is_file():
                failures.append(f"missing figure referenced by {name}: {relative}")
        for relative in tables:
            if not (manuscript / relative).is_file():
                failures.append(f"missing table referenced by {name}: {relative}")
    for required in ["references.bib", "oup-authoring-template.cls", "oup-plain.bst"]:
        if not (manuscript / required).is_file():
            failures.append(f"missing manuscript dependency: {required}")
    extra_tex = {
        path.name for path in manuscript.glob("*.tex")
        if path.name not in {"main.tex", "supplement.tex"}
    }
    if extra_tex:
        failures.append(f"unexpected top-level manuscript sources: {sorted(extra_tex)}")
    if list(manuscript.glob("final_*_authoritative.pdf")):
        failures.append("superseded reference PDF present")
    return failures


def check_text_files() -> list[str]:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        relative = path.relative_to(ROOT).as_posix()
        if path.name == ".DS_Store":
            failures.append(f"system metadata present: {relative}")
        if path.suffix.lower() == ".csv":
            text = path.read_text(encoding="utf-8", errors="replace")
            try:
                header = next(csv.reader(text.splitlines()))
            except StopIteration:
                header = []
            normalized = {column.strip().lower() for column in header}
            if PERSON_COLUMNS.intersection(normalized):
                failures.append(f"person-level identifier column in {relative}")
    return failures


def check_hashes() -> tuple[list[str], int]:
    failures: list[str] = []
    hash_file = ROOT / "SHA256SUMS"
    if not hash_file.is_file():
        return ["missing SHA256SUMS"], 0
    recorded: dict[str, str] = {}
    for line in hash_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        recorded[relative] = expected
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    recorded_paths = set(recorded)
    for relative in sorted(actual - recorded_paths):
        failures.append(f"unrecorded file: {relative}")
    for relative in sorted(recorded_paths - actual):
        failures.append(f"missing recorded file: {relative}")
    for relative, expected in sorted(recorded.items()):
        path = ROOT / relative
        if path.is_file() and digest(path) != expected:
            failures.append(f"hash mismatch: {relative}")
    return failures, len(recorded)


def main() -> None:
    failures: list[str] = []
    validate_public_cohort_summary(ROOT / "config/adult_cohorts.csv")
    failures.extend(check_manuscript_assets())
    failures.extend(check_text_files())
    hash_failures, files_verified = check_hashes()
    failures.extend(hash_failures)
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        "{\n"
        '  "status": "passed",\n'
        '  "person_level_identifier_columns": 0,\n'
        f'  "files_verified": {files_verified}\n'
        "}"
    )


if __name__ == "__main__":
    main()
