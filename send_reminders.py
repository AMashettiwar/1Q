"""Send the daily 1Q reminder email to opted-in users who have not finished today.

Run once a day from any scheduler (cron, GitHub Actions, etc.):
    DATABASE_URL=... SMTP_HOST=... SMTP_USER=... SMTP_PASSWORD=... SMTP_FROM=... APP_URL=... python send_reminders.py
Add --dry-run to print instead of sending.
"""
import sys
from datetime import date

from sqlalchemy import select

from oneq import auth, avatar, config
from oneq.db import session
from oneq.models import DailySet, User


def main(dry: bool = False) -> int:
    today = date.today()
    url = config.get("APP_URL", "")
    if not dry and not auth.smtp_configured():
        print("SMTP is not configured; nothing sent. Use --dry-run to preview.")
        return 0
    sent = 0
    with session() as s:
        done = set(s.scalars(select(DailySet.user_id).where(DailySet.day == today, DailySet.completed.is_(True))))
        for u in s.scalars(select(User).where(User.reminder_opt_in.is_(True), User.role.is_not(None))):
            if u.id in done or u.last_reminded == today:
                continue
            subject = avatar.reminder_subject(u.display_name, u.role, u.streak, today)
            teaser, _ = avatar.daily_pick(avatar.TEASERS, today, "teaser")
            body = (f"Hi {u.display_name},\n\nToday's cliffhanger: {teaser}\n"
                    f"The answer unlocks when you finish today's 12 questions. About 4 minutes.\n\n{url}\n\n"
                    f"{avatar.daily_pick(avatar.SAYS, today)}\n- 1Q\n\n"
                    "Don't want these? Turn off 'Daily reminder email' in 1Q > My Progress > Settings.")
            if dry:
                print(f"[dry-run] {u.email}: {subject}")
            else:
                try:
                    auth.send_email(u.email, subject, body)
                except Exception as e:  # noqa: BLE001
                    print(f"failed {u.email}: {e}")
                    continue
                u.last_reminded = today
            sent += 1
    print(f"{sent} reminder(s) {'previewed' if dry else 'sent'}.")
    return sent


if __name__ == "__main__":
    main(dry="--dry-run" in sys.argv)
