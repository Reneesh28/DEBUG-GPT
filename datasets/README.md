# Debug GPT Datasets

This directory contains the complete **20,000+ sample synthetic training dataset** designed to fine-tune AI models for code debugging, explanation, and optimization tasks.

## Purpose of the Dataset

The primary goal of this dataset is to teach Large Language Models (LLMs) to act as senior software engineers and programming tutors. Rather than merely outputting a corrected code block, this dataset forces the model to:
1. Provide deep technical explanations.
2. Provide beginner-friendly analogies.
3. Offer prevention strategies.
4. Output algorithmic complexity (Big-O) analysis for both the broken and fixed code.

## Folder Hierarchy

The dataset is partitioned by error category, then by language:

```text
datasets/
├── compiler_errors/
│   ├── cpp/
│   └── python/
├── educational_explanations/
│   ├── cpp/
│   └── python/
├── logical_bugs/
│   ├── cpp/
│   └── python/
├── optimization_examples/
│   ├── cpp/
│   └── python/
├── runtime_errors/
│   ├── cpp/
│   └── python/
└── metadata/
    ├── categories.json
    ├── dataset_statistics.json
    └── README.md
```

## Schema Overview

All JSON files in this directory are structured as Arrays of Objects. Every object must strictly conform to the JSON schema defined in `training/dataset_schema.json`. 

Key schema fields:
- `id`: Globally unique identifier.
- `language`: Target language (`python` or `cpp`).
- `category`: Error classification.
- `input`: The broken code, title, and error message.
- `output`: The AI's ideal response (technical, beginner, analogy, solution, prevention, optimized_code, complexity).
- `metadata`: Tags, difficulty, and source.

## Naming Conventions

* **File Names:** Files should be descriptive and grouped by sub-concept (e.g., `index_and_key_errors.json`).
* **IDs:** All `id` fields must be globally unique across all files, formatted as `[LANG]_[CATEGORY]_[6-DIGIT-NUMBER]`.
  - Example: `PY_RUNTIME_000001` or `CP_COMPILER_001050`.

## Validation Instructions

Before any data is merged or finalized, it must pass strict schema and uniqueness validation.

To run the validator:
1. Ensure your virtual environment is active.
2. Navigate to the project root.
3. Run: `python training/validate_dataset.py`

If the validator outputs `🎉 Dataset validation completed successfully.`, your data is valid. It will automatically check for JSON syntax errors, Schema compliance, and Duplicate IDs across all 86+ files.

## How to Add New Samples

1. Determine the appropriate category and language folder.
2. Open or create a conceptually relevant JSON file.
3. Follow the schema to add your new JSON object to the file's JSON Array.
4. Manually assign a globally unique ID (or use a generation script like `generate_batch_X.py` in the `training` directory to auto-assign IDs).
5. Run the validation script (`python training/validate_dataset.py`).
6. Once passed, commit your changes.
