# 1Q

A daily cancer-biology quiz for the 1cell.ai team. Twelve multiple-choice questions a day, adaptive per person, with a small mascot called 1Q who keeps you company.

Entry file: `app.py`

## Run locally

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then edit
streamlit run app.py
pytest -q
```

With no secrets at all, the app runs in demo sign-in mode, uses SQLite (`oneq.sqlite3`) and serves questions from the built-in seed bank.

## Secrets

| Key | Purpose |
| --- | --- |
| `AUTH_MODE` | `google`, `email_otp` or `demo` (default `demo`) |
| `ALLOWED_DOMAIN` | Sign-in domain, default `1cell.ai` |
| `ADMIN_EMAILS` | Comma-separated admin emails; first entry `ankith@1cell.ai` |
| `DATABASE_URL` | SQLAlchemy URL. SQLite for dev, Postgres for production |
| `LLM_PROVIDER` | `groq` (default), `openai` (any OpenAI-compatible API) or `none` |
| `LLM_MODEL` | Default `llama-3.3-70b-versatile` |
| `GROQ_API_KEY` | Groq key |
| `OPENAI_API_KEY`, `OPENAI_BASE_URL` | For the OpenAI-compatible provider |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | One-time codes and reminders |
| `APP_URL` | Link placed in reminder emails |
| `[auth]`, `[auth.google]` | Google OIDC settings for `st.login` |

Never commit `.streamlit/secrets.toml`. It is in `.gitignore`.

## Sign-in modes

- **google**: Streamlit's built-in OIDC (`st.login`). In Google Cloud Console, create an OAuth client (Web application) and add the redirect URI `https://<your-app>.streamlit.app/oauth2callback`. Put `redirect_uri`, a random `cookie_secret`, `client_id`, `client_secret` and `server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"` in secrets. `client_kwargs = { hd = "1cell.ai" }` asks Google to show only workspace accounts, and the app also checks the email domain on every sign-in.
- **email_otp**: a 6-digit code sent over SMTP, valid for 10 minutes.
- **demo**: type any @1cell.ai address and you are in. **Demo mode does not prove that you own the email address.** Use it only for local testing or a trusted preview.

## Database and persistence

Streamlit Community Cloud's disk is ephemeral: a SQLite file is lost whenever the app restarts or redeploys. For real use, set `DATABASE_URL` to a hosted Postgres (Supabase, Neon, or similar), e.g. `postgresql://user:pass@host:5432/db?sslmode=require`. Tables are created on first start. `postgres://` URLs are accepted.

## Deploy on Streamlit Community Cloud

1. share.streamlit.io, then New app, then pick repo `AMashettiwar/1Q`, branch `main`, main file `app.py`.
2. Advanced settings: Python 3.12 or 3.13. Paste your secrets (see `.streamlit/secrets.toml.example`).
3. Minimum production secrets: `AUTH_MODE="google"`, `[auth]` + `[auth.google]`, `DATABASE_URL` (Postgres), `GROQ_API_KEY`, `ADMIN_EMAILS`.
4. Deploy, then add the final app URL as the OAuth redirect URI in Google Cloud.

## How it works

- **Roles and levels**: `roles.yaml` maps each role to a starting level (basics, intermediate, advanced, expert). Edit it and redeploy. "Other" roles are matched by keywords, then by the LLM if one is configured. Users can change role in My Progress.
- **Placement**: about 5 adaptive questions set the starting rating.
- **Daily set**: 12 MCQs, one attempt, no skips. About 70% new, 30% review. Mastery is an Elo rating per subtopic. Missed concepts return reworded at 1, 3 and 7 days, then retire. Fridays end with 3 harder "boss" questions. Sometimes one slot is a wild card from another field.
- **Answers**: each answer locks when checked. A wrong answer shows the explanation right away, and every explanation appears on the final review screen.
- **Points**: 10 per correct answer plus 20 for finishing. No timer and no speed bonus.
- **Day and streaks**: the day resets at local midnight (timezone from the browser, overridable in settings). Weekends never break a streak. Each 7-day streak earns a shield (up to 3) that covers one missed weekday.
- **Leaderboards**: Daily, Weekly, Monthly and Overall, top 10 plus your own rank. The score blends points, streak and mastery. Correct and wrong counts are never shown.
- **Chat**: ask 1Q anything in the sidebar. It will not reveal the answer to a live question, and is rate limited (15 messages per 10 minutes, 80 a day).
- **LLM**: `oneq/llm.py` has a provider registry. All output is strict JSON validated with pydantic, retried once, and falls back to the seed bank. Daily sets are cached in the database.

## Reminders

`python send_reminders.py` emails opted-in users who have not finished today. Reminders are on by default and users can turn them off in My Progress. Run it once each weekday from cron or a scheduled GitHub Action with the same secrets as environment variables. Use `--dry-run` to preview.

## Fair play

1Q watches a few light signals: very fast answers, machine-regular timing, copy or paste, switching tabs during a question, and perfect runs that look unlikely. The response is a gentle in-character nudge, an "honest mode" badge for clean days, and a soft flag visible only on the admin page.

These signals cannot prove cheating. Fast readers, keyboard users and people with other windows open will trip them. Treat a flag as a reason for a friendly chat at most. Browser signals are best effort and may be blocked.

## Tone

All mascot lines and every LLM prompt follow the same rules: light and wholesome humor only. No jokes about patients, suffering, death, politics, religion, or anyone's mistakes. Fallback lines are filtered against a banned-word list in tests.

## Palette

The colours come from a heritage wardrobe: deep teal and midnight navy lead, greens and warm neutrals support. Tokens live in `oneq/ui.py` (`THEMES`, `PALETTE`, `TOPIC_TONES`, `PERIOD_TONES`, `SECTION_TONES`, `OUTFIT_TONES`). Each tone has a light-theme and a dark-theme value, and `tests/test_palette.py` checks WCAG AA contrast for all of them.

## Role adaptation (any role, not a fixed list)

`oneq/persona.py` turns any role text (a `roles.yaml` entry or free text typed under "Other") into a profile:

| Field | Values |
|---|---|
| function | executive, regulatory, clinical, computational, engineering, wet-lab, science, operations, business, general |
| seniority | early, mid, senior, exec |
| familiarity | low, medium, high (how close the job is to cancer biology) |
| hooks | wholesome humor hooks, e.g. pipettes, code review, board meetings, grants, audits, freezer inventory |

How the profile is built:

1. Keyword rules decide first. The first matching rule wins, e.g. "chief" → executive, "regulat" → regulatory, "lab" → wet-lab, "manager" → senior.
2. If no rule matches and an LLM is configured, the LLM classifies the title as JSON. Its hooks then go through the same tone guard.
3. If neither works, the role falls back to `general`.

Profiles are cached per role text with an LRU cache, and the app computes them per signed-in user.

What the profile drives:

- **Mascot lines.** These cover the login greeting, the home greeting, and right/wrong lines.
  - The fallback banks in `avatar.ROLE_LINES` are tagged by function: intern, tech, wetlab, comp, phd, clinical, regulatory, business, ops, cto, ceo and starter.
  - `persona.SENIORITY_TAGS` adds a seniority overlay, so any role gets a fitting line without the LLM.
  - Greetings also change for a first visit vs a returning visit, by time of day (night owl, morning, afternoon, evening) and by streak.
  - On the login screen, once a known email is entered, 1Q greets the person by name with a persona and streak line. Poking 1Q cycles through local banter, and 1Q bobs along while you type.
- **Chat.** `persona.chat_brief()` adds the function, seniority, familiarity, tone and hooks to the chat system prompt.
- **Feedback tone.** The explanation label is "In plain words", "Why", "Mechanism" or "Business takeaway", depending on seniority. The same tone goes into LLM prompts.
- **Starting level.** The order is:
  1. a `roles.yaml` entry
  2. a yaml keyword
  3. the profile (familiarity × seniority)
  4. the LLM guess
  5. basics

  Executives (CEO and CTO) start on a business-friendly intermediate track of science fundamentals.

All lines pass the wholesome tone guard (`avatar.is_safe`), and the tests check every bank.

## Progress charts (private)

The Progress page is private and shows only your own data:

- mastery radar (an animated inline SVG)
- topic-coverage donut
- per-topic mastery bars
- 12-week activity heatmap
- knowledge level over time (a replay of your answers through the rating model, shown as an area chart)
- rank-over-time sparkline

The charts use the wardrobe palette and animate in, and they respect prefers-reduced-motion. Public surfaces never show correct or wrong counts.
