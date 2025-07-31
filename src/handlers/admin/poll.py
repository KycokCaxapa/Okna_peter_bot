from pathlib import Path

import json


POLL_FILE = Path('poll.json')


def save_poll_options(options: list[str]) -> None:
    '''Save current poll options to poll.json'''
    with open(POLL_FILE, 'w', encoding='utf-8') as f:
        json.dump(options, f)


def load_poll_options() -> list[str]:
    '''Load current poll options from poll.json'''
    if POLL_FILE.exists():
        with open(POLL_FILE, encoding='utf-8') as f:
            return json.load(f)
    return []


def clear_poll_options() -> None:
    '''Clear poll options'''
    if POLL_FILE.exists():
        POLL_FILE.unlink()
