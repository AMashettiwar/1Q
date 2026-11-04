from oneq import auth

K = b"k" * 32


def test_sign_and_verify_roundtrip():
    t = auth.sign_token("Ann@1cell.ai", K, now=1000)
    assert auth.verify_token(t, K, now=1001) == "ann@1cell.ai"


def test_expired_token_rejected():
    t = auth.sign_token("ann@1cell.ai", K, days=30, now=0)
    assert auth.verify_token(t, K, now=30 * 86400 - 1) == "ann@1cell.ai"
    assert auth.verify_token(t, K, now=30 * 86400 + 1) is None


def test_tampered_or_wrong_key_rejected():
    t = auth.sign_token("ann@1cell.ai", K, now=0)
    body, mac = t.split(".")
    forged = auth._b64(b"eve@1cell.ai|9999999999") + "." + mac
    assert auth.verify_token(forged, K, now=1) is None
    assert auth.verify_token(body + "." + mac[:-2] + "AA", K, now=1) is None
    assert auth.verify_token(t, b"x" * 32, now=1) is None
    for junk in (None, "", "abc", "a.b.c"):
        assert auth.verify_token(junk, K) is None


def test_domain_rechecked_on_verify():
    t = auth.sign_token("ann@gmail.com", K, now=0)
    assert auth.verify_token(t, K, now=1) is None


def test_cookie_js_sets_and_clears():
    assert "oq_auth=abc" in auth.cookie_js("abc") and "Max-Age=2592000" in auth.cookie_js("abc")
    assert "Max-Age=0" in auth.cookie_js(None)


def test_db_generated_secret_is_stable(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/s.db")
    for k in ("COOKIE_SECRET", "SMTP_PASSWORD", "OPENAI_API_KEY", "XAI_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    auth._SECRET_CACHE.clear()
    a = auth.cookie_secret()
    auth._SECRET_CACHE.clear()
    assert auth.cookie_secret() == a and len(a) == 32
    auth._SECRET_CACHE.clear()
