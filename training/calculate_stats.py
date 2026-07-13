import json
import glob
import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

stats = {
    "total_samples": 0,
    "languages": {
        "python": 0,
        "cpp": 0
    },
    "categories": {
        "runtime_error": 0,
        "compiler_error": 0,
        "logical_bug": 0,
        "optimization": 0,
        "educational": 0
    }
}

for filepath in glob.glob("../datasets/**/*.json", recursive=True):
    # skip metadata folder
    if "metadata" in filepath:
        continue
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    stats["total_samples"] += 1
                    
                    lang = item.get("language")
                    if lang in stats["languages"]:
                        stats["languages"][lang] += 1
                        
                    category = item.get("category")
                    if category in stats["categories"]:
                        stats["categories"][category] += 1
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

ensure_dir("../datasets/metadata")
with open("../datasets/metadata/dataset_statistics.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=4)

print(f"Final Statistics: {json.dumps(stats, indent=2)}")
