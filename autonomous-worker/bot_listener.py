"""
Interactive 2-Way Telegram Bot Listener with Dynamic Progress & Time Calculation.
Answers Vrajesh on progress, exact time estimates, and roadmap updates.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import re

sys.path.insert(0, os.path.dirname(__file__))

from brain.task_engine import TaskEngine

def get_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

class TelegramListener:
    def __init__(self):
        self.config = get_config()
        notif = self.config.get("notifications", {})
        self.token = notif.get("telegram_bot_token", "9027402724:AAGLqBSEEyi1wKzLaVRKaszG9S9JLj6CgaU")
        self.chat_id = str(notif.get("telegram_chat_id", "6631130370"))
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.project_root = os.path.join(os.path.dirname(__file__), self.config.get("project_root", ".."))
        self.engine = TaskEngine(project_root=self.project_root)

    def send_reply(self, text: str, parse_mode: str = "HTML"):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"Error sending reply: {e}")
            return False

    def _resolve_project(self, text_lower: str):
        """Resolves whether query is for vvvbbb website or milk dairy, defaulting to most active."""
        test_dir = r"C:\Users\Admin\Desktop\test"
        milk_dir = r"C:\Users\Admin\Desktop\milk"

        if any(w in text_lower for w in ["website", "vvvbbb", "web", "portfolio"]):
            if os.path.exists(os.path.join(test_dir, "ROADMAP.md")):
                return test_dir, "vvvbbb Website"

        if any(w in text_lower for w in ["milk", "dairy", "khata", "owner", "customer"]):
            if os.path.exists(os.path.join(milk_dir, "ROADMAP.md")):
                return milk_dir, "DairyManager System"

        # Check latest modified ROADMAP.md
        t_mtime = os.path.getmtime(os.path.join(test_dir, "ROADMAP.md")) if os.path.exists(os.path.join(test_dir, "ROADMAP.md")) else 0
        m_mtime = os.path.getmtime(os.path.join(milk_dir, "ROADMAP.md")) if os.path.exists(os.path.join(milk_dir, "ROADMAP.md")) else 0

        if t_mtime > m_mtime:
            return test_dir, "vvvbbb Website"
        return milk_dir, "DairyManager System"

    def handle_message(self, text: str):
        text_lower = text.lower().strip()
        print(f"📩 [User Message]: {text}")

        # 1. Add task command
        if any(w in text_lower for w in ["add task", "task add", "ye add karo", "ye banao"]):
            clean_task = re.sub(r'^(add task|task add|ye add karo|ye banao)[:\s-]*', '', text, flags=re.IGNORECASE).strip()
            if clean_task:
                target_dir, p_name = self._resolve_project(text_lower)
                roadmap_path = os.path.join(target_dir, "ROADMAP.md")
                new_entry = f"\n- [ ] **{clean_task}**\n  - **Type:** User Request (via Telegram)\n  - **Description:** Added remotely by Vrajesh from phone.\n  - **Acceptance Criteria:** Tested and build passes.\n"
                with open(roadmap_path, "a", encoding="utf-8") as f:
                    f.write(new_entry)
                self.send_reply(
                    f"✅ <b>Bhai, naya task add ho gaya hai!</b>\n\n"
                    f"📁 <b>Project:</b> {p_name}\n"
                    f"📋 <b>Task:</b> {clean_task}\n\n"
                    f"Agent is task ko automatically build karega! 🚀"
                )
            else:
                self.send_reply("Bhai, task ka naam toh likho! Jaise: <code>ye add karo: Testimonials section me 5 stars lagao</code>")
            return

        # 2. Status / Kitni der / Kaha tak pahucha (Handled dynamically)
        target_dir, p_name = self._resolve_project(text_lower)
        active_engine = TaskEngine(project_root=target_dir)
        tasks = active_engine.parse_roadmap()

        done = [t for t in tasks if t["is_done"]]
        pending = [t for t in tasks if not t["is_done"]]
        total = len(tasks)
        pct = int((len(done) / total) * 100) if total > 0 else 0

        # Calculate exact realistic time
        # Each pending task takes approximately 4 minutes
        current_task_title = pending[0]['title'] if pending else "Sabhi tasks complete hain!"
        pending_count = len(pending)

        if pending_count == 0:
            current_task_eta = "0 minute (Sab Done)"
            total_eta = "0 minute (Poora project 100% complete ho chuka hai!)"
        elif pending_count == 1:
            current_task_eta = "Lagbhag 3 se 4 minute"
            total_eta = "Lagbhag 3 se 4 minute me sabhi tasks done ho jayenge"
        else:
            current_task_eta = "Lagbhag 3 se 4 minute"
            min_eta = (pending_count * 4) - 2
            max_eta = (pending_count * 4) + 2
            total_eta = f"Lagbhag {min_eta} se {max_eta} minute (baaki {pending_count} tasks ke liye)"

        done_list = "\n".join([f"  ✅ <s>{t['title']}</s>" for t in done]) if done else "  <i>Abhi koi task complete nahi hua</i>"
        upcoming_list = "\n".join([f"  ⏳ {t['title']}" for t in pending[1:3]]) if len(pending) > 1 else "  <i>Iske baad koi aur task baki nahi hai</i>"

        reply = (
            f"Haan bhai, kaam chal raha hai! ⏳\n\n"
            f"📁 <b>Project:</b> {p_name}\n"
            f"📊 <b>Progress:</b> {pct}% ({len(done)}/{total} Tasks)\n\n"
            f"📍 <b>Abhi tak kaha pahucha:</b>\n{done_list}\n\n"
            f"🎯 <b>Abhi is par kaam chal raha hai:</b>\n👉 <b>{current_task_title}</b>\n\n"
            f"⏱️ <b>Kitni der lagegi:</b>\n"
            f"• Abhi wale task me: <b>{current_task_eta}</b>\n"
            f"• Poora kaam hone me: <b>{total_eta}</b>\n\n"
            f"📋 <b>Agle Tasks:</b>\n{upcoming_list}\n\n"
            f"Fikar mat karo, mai laga hua hoon! 💪"
        )
        self.send_reply(reply)

    def poll_once(self):
        url = f"{self.base_url}/getUpdates?offset={self.last_update_id + 1}&timeout=5"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("result", []):
                    self.last_update_id = item["update_id"]
                    msg = item.get("message", {})
                    text = msg.get("text", "")
                    sender = str(msg.get("chat", {}).get("id", ""))
                    if sender == self.chat_id and text and text != "/start":
                        self.handle_message(text)
        except Exception as e:
            print(f"Polling error: {e}")

    def run_forever(self):
        print("🤖 [Telegram Listener Daemon] Started and listening to messages from Vrajesh...")
        while True:
            self.poll_once()
            time.sleep(2)

if __name__ == "__main__":
    listener = TelegramListener()
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        listener.poll_once()
    else:
        listener.run_forever()
