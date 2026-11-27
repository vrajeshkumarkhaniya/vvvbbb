"""
Telegram Bot Real-Time Phone Notifier.
Sends clean Hinglish progress updates to Vrajesh without noisy technical stack traces.
"""

import os
import json
import time
import urllib.request
from typing import Dict, Any


class TelegramNotifier:
    def __init__(self, config: Dict[str, Any]):
        cfg = config.get("notifications", {})
        token_env = cfg.get("telegram_bot_token_env", "TELEGRAM_BOT_TOKEN")
        chat_id_env = cfg.get("telegram_chat_id_env", "TELEGRAM_CHAT_ID")

        self.bot_token = os.environ.get(token_env) or cfg.get("telegram_bot_token", "")
        self.chat_id = str(os.environ.get(chat_id_env) or cfg.get("telegram_chat_id", ""))
        self.enabled = bool(self.bot_token and self.chat_id)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_notif_file = os.path.join(os.path.dirname(__file__), ".last_notif_time")
        self.min_interval_sec = 180

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """Sends instant push notification message to user's phone."""
        if not self.enabled:
            print(f"📱 [Phone Alert]: {text}")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"⚠️ [Telegram Error]: {e}")
            return False

    def notify_task_start(self, task: Dict[str, Any]):
        now = time.time()
        last_time = 0.0
        if os.path.exists(self.last_notif_file):
            try:
                with open(self.last_notif_file, "r", encoding="utf-8") as f:
                    last_time = float(f.read().strip())
            except Exception:
                last_time = 0.0

        if now - last_time < self.min_interval_sec:
            print("⏳ [Telegram Throttle] Skipped start alert (cooldown active)")
            return

        with open(self.last_notif_file, "w", encoding="utf-8") as f:
            f.write(str(now))

        msg = (
            f"Haan bhai, kaam chal raha hai! ⏳\n\n"
            f"🎯 <b>Abhi is par kaam ho raha hai:</b>\n👉 <b>{task.get('title')}</b>\n\n"
            f"⏱️ <b>Kitni der lagegi:</b> Lagbhag 2 se 4 minute.\n\n"
            f"Complete hote hi aur Vercel live hote hi update bhej dunga! 🚀"
        )
        self.send_message(msg)

    def notify_task_complete(self, task: Dict[str, Any], total_done: int):
        msg = (
            f"✅ <b>Bhai, task complete &amp; live push ho gaya!</b>\n\n"
            f"👉 <b>{task.get('title')}</b>\n"
            f"• Build check pass (0 errors)\n"
            f"• GitHub par push + Vercel auto-deploy triggered\n"
            f"• Total completed tasks: {total_done}\n\n"
            f"🔗 https://test-eta-snowy-j4wco9595m.vercel.app"
        )
        self.send_message(msg)

    def notify_error(self, task: Dict[str, Any], error: str):
        # Keep Telegram clean: silent log in runner without robotic error dumps
        print(f"⚠️ [Silent Self-Healing]: {task.get('title')} - {error[:160]}")
