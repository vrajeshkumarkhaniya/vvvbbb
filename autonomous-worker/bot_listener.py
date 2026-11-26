"""
Interactive 2-Way Telegram Bot Listener.
Listens to messages from Vrajesh, answers queries about progress, adds new tasks, and controls agent.
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
        token_env = notif.get("telegram_bot_token_env", "TELEGRAM_BOT_TOKEN")
        chat_env = notif.get("telegram_chat_id_env", "TELEGRAM_CHAT_ID")
        self.token = os.environ.get(token_env) or notif.get("telegram_bot_token", "")
        self.chat_id = str(os.environ.get(chat_env) or notif.get("telegram_chat_id", ""))
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

    def handle_message(self, text: str):
        text_lower = text.lower().strip()
        print(f"📩 [User Message]: {text}")

        # 1. Status / Progress query
        if any(w in text_lower for w in ["kitna kam", "kitna kaam", "status", "progress", "update", "kya hua", "kya chal raha", "bhejega", "bhejo"]):
            tasks = self.engine.parse_roadmap()
            done = [t for t in tasks if t["is_done"]]
            pending = [t for t in tasks if not t["is_done"]]
            total = len(tasks)
            pct = int((len(done) / total) * 100) if total > 0 else 0

            done_list = "\n".join([f"  ✅ <s>{t['title']}</s>" for t in done]) if done else "  <i>Koi task complete nahi hua abhi</i>"
            next_task = pending[0]['title'] if pending else "Sabhi tasks complete ho chuke hain!"
            pending_list = "\n".join([f"  ⏳ {t['title']}" for t in pending[:3]]) if pending else "  <i>Koi pending task nahi hai</i>"

            reply = (
                f"📊 <b>Bhai, yeh raha aapka Live Progress Report:</b>\n\n"
                f"<b>Total Progress:</b> {pct}% ({len(done)}/{total} Tasks)\n\n"
                f"<b>✅ Completed Tasks:</b>\n{done_list}\n\n"
                f"<b>🎯 Abhi Agla Kaam (Next):</b>\n  👉 <b>{next_task}</b>\n\n"
                f"<b>📋 Upcoming Tasks:</b>\n{pending_list}\n\n"
                f"💡 <i>Tip: Aap mujhe bol sakte ho 'ye task add karo: XYZ' aur mai roadmap me daal dunga!</i>"
            )
            self.send_reply(reply)

        # 2. Add task command
        elif any(w in text_lower for w in ["add task", "task add", "ye add karo", "ye banao"]):
            clean_task = re.sub(r'^(add task|task add|ye add karo|ye banao)[:\s-]*', '', text, flags=re.IGNORECASE).strip()
            if clean_task:
                roadmap_path = os.path.join(self.project_root, "ROADMAP.md")
                new_entry = f"\n- [ ] **{clean_task}**\n  - **Type:** User Request (via Telegram)\n  - **Description:** Added remotely by Vrajesh from phone.\n  - **Acceptance Criteria:** Tested and build passes.\n"
                with open(roadmap_path, "a", encoding="utf-8") as f:
                    f.write(new_entry)
                self.send_reply(f"✅ <b>Bhai, naya task add ho gaya hai!</b>\n\n📋 <b>Task:</b> {clean_task}\n\nAb agent is task ko automatically pick karke build karega!")
            else:
                self.send_reply("Bhai, task ka naam toh likho! Jaise: <code>ye add karo: Dairy print receipt me QR code lagao</code>")

        # 3. Friendly conversational reply
        else:
            self.send_reply(
                f"Haan Vrajesh bhai! Bilkul, mai hi aapka <b>24/7 Coding Buddy</b> hoon! 🤖\n\n"
                f"Jab bhi aap PC band karoge, mai piche se:\n"
                f"1. Code likhunga aur test pass karunga.\n"
                f"2. Git par push karunga.\n"
                f"3. Aur har ek task ka update <b>aapke isi Telegram chat par bhejta rahunga!</b>\n\n"
                f"Aap jab chahein yahan <b>'kitna kaam hua'</b> ya <b>'status'</b> likh kar poochna, mai turant live report dunga! 🔥"
            )

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
                    # Only respond to Vrajesh or ignore /start
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
