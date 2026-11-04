"""Sign-in. Modes: google (Streamlit OIDC), email_otp (SMTP code), demo (domain check only)."""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import smtplib
import time
from email.message import EmailMessage

from . import config

ALLOWED_DOMAIN = "1cell.ai"
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@([A-Za-z0-9.\-]+)$")


def allowed_domain() -> str:
    return str(config.get("ALLOWED_DOMAIN", ALLOWED_DOMAIN)).lower().lstrip("@")


def is_allowed_email(email: str | None, domain: str | None = None) -> bool:
    if not email:
        return False
    m = _EMAIL_RE.match(email.strip())
    if not m:
        return False
    return m.group(1).lower() == (domain or allowed_domain())  # exact match, no subdomains


def smtp_configured() -> bool:
    return all(config.get(k) for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM"))


def auth_mode() -> str:
    mode = config.get("AUTH_MODE")
    if mode in ("google", "email_otp", "demo"):
        return mode
    if config.has_oidc():
        return "google"
    if smtp_configured():
        return "email_otp"
    return "demo"


def is_admin(email: str) -> bool:
    return email.lower() in config.get_list("ADMIN_EMAILS")


def send_email(to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = config.get("SMTP_FROM"), to, subject
    msg.set_content(body)
    port = int(config.get("SMTP_PORT", 587))
    host = config.get("SMTP_HOST")
    if port == 465:
        srv = smtplib.SMTP_SSL(host, port, timeout=20)
    else:
        srv = smtplib.SMTP(host, port, timeout=20)
        srv.starttls()
    with srv:
        srv.login(config.get("SMTP_USER"), config.get("SMTP_PASSWORD"))
        srv.send_message(msg)


def new_otp() -> tuple[str, str, float]:
    code = f"{secrets.randbelow(10**6):06d}"
    return code, hashlib.sha256(code.encode()).hexdigest(), time.time() + 600


def check_otp(code: str, digest: str, expires: float) -> bool:
    if time.time() > expires:
        return False
    return hmac.compare_digest(hashlib.sha256(code.strip().encode()).hexdigest(), digest)


def google_user():
    """Return verified 1cell.ai email from st.user, or None."""
    import streamlit as st
    if not getattr(st.user, "is_logged_in", False):
        return None
    email = st.user.get("email")
    if st.user.get("email_verified") is False:
        return None
    hd = st.user.get("hd")
    if hd and hd.lower() != allowed_domain():
        return None
    return email.lower() if is_allowed_email(email) else None


# ---------------------------------------------------------------- remember-me token
COOKIE_NAME = "oq_auth"
REMEMBER_DAYS = 30
_SECRET_CACHE: dict[str, bytes] = {}


def _b64(b: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _unb64(s: str) -> bytes:
    import base64
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def cookie_secret() -> bytes:
    """COOKIE_SECRET, else derived from existing secrets, else generated once and stored in the DB."""
    if "k" in _SECRET_CACHE:
        return _SECRET_CACHE["k"]
    explicit = config.get("COOKIE_SECRET")
    if explicit:
        key = hashlib.sha256(b"1q-cookie|" + str(explicit).encode()).digest()
    else:
        base = [str(config.get(k)) for k in ("SMTP_PASSWORD", "OPENAI_API_KEY", "XAI_API_KEY", "DATABASE_URL") if config.get(k)]
        try:
            import streamlit as st
            cs = st.secrets.get("auth", {}).get("cookie_secret")
            if cs:
                base.append(str(cs))
        except Exception:  # noqa: BLE001
            pass
        if any(b for b in base if not b.startswith("sqlite")):
            key = hashlib.sha256(b"1q-cookie-derived|" + "|".join(base).encode()).digest()
        else:
            from .db import session
            from .models import AppSecret
            with session() as s:
                row = s.get(AppSecret, "cookie_secret")
                if not row:
                    row = AppSecret(name="cookie_secret", value=secrets.token_hex(32))
                    s.add(row)
                key = bytes.fromhex(row.value)
    _SECRET_CACHE["k"] = key
    return key


def sign_token(email: str, secret: bytes | None = None, days: int = REMEMBER_DAYS, now: float | None = None) -> str:
    exp = int((now if now is not None else time.time()) + days * 86400)
    body = _b64(f"{email.strip().lower()}|{exp}".encode())
    mac = _b64(hmac.new(secret or cookie_secret(), body.encode(), hashlib.sha256).digest())
    return f"{body}.{mac}"


def verify_token(token: str | None, secret: bytes | None = None, now: float | None = None) -> str | None:
    """Return the email if the token is authentic, unexpired and still on the allowed domain."""
    try:
        body, mac = (token or "").split(".", 1)
        good = _b64(hmac.new(secret or cookie_secret(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(good, mac):
            return None
        email, exp = _unb64(body).decode().rsplit("|", 1)
        if (now if now is not None else time.time()) > int(exp):
            return None
        return email if is_allowed_email(email) else None
    except Exception:  # noqa: BLE001
        return None


def cookie_js(token: str | None, days: int = REMEMBER_DAYS) -> str:
    """Script that sets (or clears, when token is None) the remember-me cookie on this browser."""
    if token:
        val = f"{COOKIE_NAME}={token}; Max-Age={days * 86400}; Path=/; SameSite=Strict"
    else:
        val = f"{COOKIE_NAME}=; Max-Age=0; Path=/; SameSite=Strict"
    return ("<script>(function(){var s=location.protocol==='https:'?'; Secure':'';"
            f"document.cookie='{val}'+s;}})();</script>")
