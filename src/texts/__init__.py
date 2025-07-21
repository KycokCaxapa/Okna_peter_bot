from pathlib import Path

BASE_PATH = Path(__file__).parent


def load_text(filename: str) -> str:
    path = BASE_PATH / filename
    return path.read_text(encoding='utf-8')
