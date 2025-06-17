import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR / "src"))

from scheduler import schedule_jobs


def test_schedule_jobs_structure():
    data_path = Path(__file__).resolve().parents[1] / "data" / "example.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    result = schedule_jobs(input_data)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "schedule" in result, "Result should contain 'schedule' key"
    assert isinstance(result["schedule"], list), "'schedule' should be a list"
