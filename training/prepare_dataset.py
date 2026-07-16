"""
DebugGPT Dataset Preparation Script.

Reads raw JSON dataset files, validates them against the project schema,
normalises fields, and writes a single JSONL file for training.

This script has NO ML dependencies — no transformers, no torch, no tokenisation.
It only prepares data.

Usage:
    python prepare_dataset.py            # Full run — validate + write JSONL
    python prepare_dataset.py --dry-run  # Validate only — don't write output
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "datasets"
SCHEMA_PATH = Path(__file__).resolve().parent / "dataset_schema.json"
OUTPUT_PATH = DATASET_DIR / "debuggpt_training_dataset.jsonl"

EXCLUDED_FOLDERS = {"metadata"}


# ---------------------------------------------------------------------------
# Schema Loading
# ---------------------------------------------------------------------------

def load_schema() -> dict:
    """Load and return the JSON schema for dataset validation."""
    if not SCHEMA_PATH.exists():
        logger.error("Schema file not found: %s", SCHEMA_PATH)
        sys.exit(1)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Record Formatting
# ---------------------------------------------------------------------------

def format_record(item: dict) -> dict:
    """
    Convert a single raw dataset record into the flat
    instruction / input / response shape expected by the training pipeline.
    """
    # --- Instruction ---
    instruction = item.get("instruction", "").strip()

    # --- Input ---
    input_data = item.get("input", {})
    language = item.get("language", "Unknown").strip()
    title = input_data.get("title", "").strip()
    error_message = input_data.get("error_message", "").strip()
    code = input_data.get("code", "").strip()

    formatted_input = (
        f"Language: {language}\n"
        f"Title: {title}\n"
        f"Error/Issue: {error_message}\n\n"
        f"Code:\n{code}"
    )

    # --- Response ---
    output_data = item.get("output", {})
    technical = output_data.get("technical", "").strip()
    beginner = output_data.get("beginner", "").strip()
    analogy = output_data.get("analogy", "").strip()
    solution = output_data.get("solution", "").strip()
    optimized_code = output_data.get("optimized_code", "").strip()
    prevention = output_data.get("prevention", "").strip()

    complexity = output_data.get("complexity", {})
    comp_before = complexity.get("before", "").strip()
    comp_after = complexity.get("after", "").strip()

    formatted_response = (
        f"**Technical Explanation**:\n{technical}\n\n"
        f"**Beginner Explanation**:\n{beginner}\n\n"
        f"**Analogy**:\n{analogy}\n\n"
        f"**Solution**:\n{solution}\n\n"
        f"**Optimized Code**:\n{optimized_code}\n\n"
        f"**Prevention**:\n{prevention}\n\n"
        f"**Complexity Analysis**:\n"
        f"Before: {comp_before}\n"
        f"After: {comp_after}"
    )

    return {
        "instruction": instruction,
        "input": formatted_input,
        "response": formatted_response,
    }


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def discover_files() -> list[Path]:
    """Find all JSON dataset files, excluding metadata directories."""
    files = []
    for json_file in sorted(DATASET_DIR.rglob("*.json")):
        if any(folder in json_file.parts for folder in EXCLUDED_FOLDERS):
            continue
        files.append(json_file)
    return files


def prepare_dataset(dry_run: bool = False) -> None:
    """
    Full pipeline: discover → validate → normalise → write JSONL.

    Args:
        dry_run: If True, validate records but do not write the output file.
    """
    schema = load_schema()
    validator = Draft202012Validator(schema)

    files = discover_files()
    if not files:
        logger.error("No JSON files found in %s", DATASET_DIR)
        sys.exit(1)

    logger.info("Found %d dataset files", len(files))

    total_records = 0
    total_errors = 0
    skipped_files = 0
    records: list[dict] = []

    for filepath in files:
        relative = filepath.relative_to(PROJECT_ROOT)

        # --- Parse JSON ---
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning("Skipping %s — invalid JSON: %s", relative, e)
            skipped_files += 1
            continue

        if not isinstance(data, list):
            logger.warning("Skipping %s — expected a JSON array", relative)
            skipped_files += 1
            continue

        # --- Validate against schema ---
        errors = sorted(validator.iter_errors(data), key=lambda x: list(x.path))
        if errors:
            logger.warning("Skipping %s — %d schema errors", relative, len(errors))
            for error in errors[:5]:  # Show first 5 errors max
                path = ".".join(map(str, error.absolute_path))
                logger.warning("  • %s: %s", path or "(root)", error.message)
            if len(errors) > 5:
                logger.warning("  • ... and %d more errors", len(errors) - 5)
            skipped_files += 1
            total_errors += len(errors)
            continue

        # --- Normalise and collect ---
        for item in data:
            records.append(format_record(item))
            total_records += 1

    # --- Summary ---
    logger.info("-" * 40)
    logger.info("Records processed : %d", total_records)
    if skipped_files:
        logger.warning("Files skipped     : %d", skipped_files)
    if total_errors:
        logger.warning("Schema errors     : %d", total_errors)

    if dry_run:
        logger.info("Dry run complete — no output written.")
        return

    # --- Write JSONL ---
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_f:
        for record in records:
            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

    logger.info("Saved %d samples to %s", total_records, OUTPUT_PATH.relative_to(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare DebugGPT training dataset from raw JSON files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and count records without writing the output file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    prepare_dataset(dry_run=args.dry_run)
