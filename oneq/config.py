"""Read settings from environment variables first, then Streamlit secrets."""
import os


def get(key: str, default=None):
    if key in os.environ:
        return os.environ[key]
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return default


def get_list(key: str) -> list[str]:
    val = get(key, "")
    if isinstance(val, (list, tuple)):
        return [str(v).strip().lower() for v in val if str(v).strip()]
    return [v.strip().lower() for v in str(val).split(",") if v.strip()]


def has_oidc() -> bool:
    try:
        import streamlit as st
        return "auth" in st.secrets
    except Exception:
        return False
