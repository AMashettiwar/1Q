import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("LLM_PROVIDER", "none")
os.environ.setdefault("AUTH_MODE", "demo")


@pytest.fixture
def db(tmp_path, monkeypatch):
    url = f"sqlite:///{tmp_path}/t.sqlite3"
    monkeypatch.setenv("DATABASE_URL", url)
    from oneq.db import session
    return lambda: session(url)
