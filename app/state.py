import json
from pathlib import Path

STATE_FILE = Path(
    "last_state.json"
)


def load_state():

    if not STATE_FILE.exists():
        return None

    return json.loads(
        STATE_FILE.read_text()
    )


def save_state(data):

    STATE_FILE.write_text(
        json.dumps(data)
    )