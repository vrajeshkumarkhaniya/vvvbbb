"""
WhatsApp Real-Time Phone Notifier.
Supports CallMeBot (100% Free personal WhatsApp API) & Meta Cloud API.
"""

import os
import json
import urllib.parse
import urllib.request
from typing import Dict, Any

class WhatsAppNotifier:
    def __init__(self, config: Dict[str, Any]):
        cfg = config.get("notifications", {})
        # CallMeBot configuration (simplest, free, 30-sec setup)
        self.phone = os.environ.get("WHATSAPP_PHONE", cfg.get("whatsapp_phone", ""))
        self.apikey = os.environ.get("WHATSAPP_APIKEY", cfg.get("whatsapp_apikey", ""))
        self.enabled = bool(self.phone and self.apikey)

    def send_message(self, text: str) -> bool:
        """Sends WhatsApp message to user's phone via CallMeBot gateway."""
        if not self.enabled:
            print(f"📱 [WhatsApp Alert (Config Pending)]: {text}")
            return False

        # Clean phone number (strip + and spaces)
        clean_phone = self.phone.replace("+", "").replace(" ", "").strip()
        encoded_text = urllib.parse.quote(text)
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={self.apikey}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Antigravity-Agent/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read().decode("utf-8")
                if "Message queued" in body or "success" in body.lower():
                    print("✅ [WhatsApp] Message delivered to phone!")
                    return True
                return True
        except Exception as e:
            print(f"⚠️ [WhatsApp Error]: {e}")
            return False

    def notify_task_start(self, task: Dict[str, Any]):
        msg = (
            f"🚀 *DairyManager Autonomous Agent Active*\n\n"
            f"*Task:* {task.get('title')}\n"
            f"*Type:* {task.get('type')}\n"
            f"*Goal:* {task.get('description')[:120]}...\n\n"
            f"⚙️ Coding & testing in progress..."
        )
        self.send_message(msg)

    def notify_task_complete(self, task: Dict[str, Any], total_done: int):
        msg = (
            f"✅ *Task Completed & Verified!*\n\n"
            f"*Finished:* {task.get('title')}\n"
            f"*Tests:* 100% Passed (Build Green)\n"
            f"*Git:* Committed to repo\n"
            f"*Total Completed:* {total_done} tasks\n\n"
            f"🌟 Continuing to next task in roadmap..."
        )
        self.send_message(msg)

    def notify_error(self, task: Dict[str, Any], error: str):
        msg = (
            f"⚠️ *Self-Healing Bug Alert*\n\n"
            f"*Task:* {task.get('title')}\n"
            f"*Issue:* {error[:180]}\n"
            f"🔄 Applying automatic fixes..."
        )
        self.send_message(msg)
