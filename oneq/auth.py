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
