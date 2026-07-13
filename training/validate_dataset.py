import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from jsonschema import Draft202012Validator

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "datasets"
SCHEMA_PATH = Path(__file__).resolve().parent / "dataset_schema.json"

# -----------------------------
# Load Schema
# -----------------------------
try:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
except FileNotFoundError:
    print(f"❌ Schema not found: {SCHEMA_PATH}")
    sys.exit(1)

validator = Draft202012Validator(schema)

# -----------------------------
# Validation Counters
# -----------------------------
total_files = 0
valid_files = 0
invalid_files = 0

seen_ids = set()
duplicate_ids = []

# Ignore metadata folder
EXCLUDED_FOLDERS = {"metadata"}

print("=" * 60)
print("DebugGPT Dataset Validation")
print("=" * 60)

# -----------------------------
# Scan Dataset Files
# -----------------------------
for json_file in DATASET_DIR.rglob("*.json"):

    if any(folder in json_file.parts for folder in EXCLUDED_FOLDERS):
        continue

    total_files += 1

    print(f"\nChecking: {json_file.relative_to(PROJECT_ROOT)}")

    # -------------------------
    # JSON Parsing
    # -------------------------
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON")
        print(f"   {e}")
        invalid_files += 1
        continue

    # -------------------------
    # Schema Validation
    # -------------------------
    errors = sorted(validator.iter_errors(data), key=lambda x: x.path)

    if errors:
        print("❌ Schema validation failed")

        for error in errors:
            path = ".".join(map(str, error.absolute_path))
            if path:
                print(f"   • {path}: {error.message}")
            else:
                print(f"   • {error.message}")

        invalid_files += 1
        continue

    # -------------------------
    # Duplicate ID Check
    # -------------------------
    for item in data:
        record_id = item["id"]
        if record_id in seen_ids:
            duplicate_ids.append(record_id)
        else:
            seen_ids.add(record_id)

    print("✅ Passed")
    valid_files += 1

# -----------------------------
# Duplicate Report
# -----------------------------
if duplicate_ids:
    print("\nDuplicate IDs Found:")
    for item in duplicate_ids:
        print(f" - {item}")
    invalid_files += len(duplicate_ids)

# -----------------------------
# Summary
# -----------------------------
print("\n" + "=" * 60)
print("Validation Summary")
print("=" * 60)

print(f"Files Checked : {total_files}")
print(f"Passed        : {valid_files}")
print(f"Failed        : {invalid_files}")

if duplicate_ids:
    print(f"Duplicate IDs : {len(duplicate_ids)}")
else:
    print("Duplicate IDs : 0")

print("=" * 60)

if invalid_files == 0:
    print("🎉 Dataset validation completed successfully.")
    sys.exit(0)
else:
    print("❌ Dataset validation failed.")
    sys.exit(1)