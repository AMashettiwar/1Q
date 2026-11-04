"""Database engine and sessions. Uses DATABASE_URL, defaults to local SQLite."""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import config
from .models import Base

_engines: dict = {}


def _url() -> str:
    url = config.get("DATABASE_URL", "sqlite:///oneq.sqlite3")
    # Supabase/Heroku style URLs
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


def get_engine(url: str | None = None):
    url = url or _url()
    if url not in _engines:
        kwargs = {"pool_pre_ping": True}
        if url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        eng = create_engine(url, **kwargs)
        Base.metadata.create_all(eng)
        _engines[url] = (eng, sessionmaker(bind=eng, expire_on_commit=False))
    return _engines[url]


@contextmanager
def session(url: str | None = None):
    _, maker = get_engine(url)
    s = maker()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    except BaseException:
        # st.rerun() / st.stop() raise BaseException subclasses; keep the work done so far
        s.commit()
        raise
    finally:
        s.close()
