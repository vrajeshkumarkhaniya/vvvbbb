"""
Main Autonomous Cloud Agent Runner.
Supports both Telegram and WhatsApp phone notifications.
"""

import os
import sys
import json
import time
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from brain.task_engine import TaskEngine
from brain.coder_agent import CoderAgent
from notifications.telegram_notifier import TelegramNotifier
from notifications.whatsapp_notifier import WhatsAppNotifier

def load_config() -> dict:
    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_notifier(config: dict):
    provider = config.get("notifications", {}).get("provider", "whatsapp").lower()
    if provider == "whatsapp":
        return WhatsAppNotifier(config)
    elif provider == "both":
        class MultiNotifier:
            def __init__(self, c):
                self.tg = TelegramNotifier(c)
                self.wa = WhatsAppNotifier(c)
            def notify_task_start(self, t):
                self.tg.notify_task_start(t)
                self.wa.notify_task_start(t)
            def notify_task_complete(self, t, n):
                self.tg.notify_task_complete(t, n)
                self.wa.notify_task_complete(t, n)
            def notify_error(self, t, e):
                self.tg.notify_error(t, e)
                self.wa.notify_error(t, e)
        return MultiNotifier(config)
    return TelegramNotifier(config)

def run_autopilot(max_tasks: int = 1, daemon: bool = False):
    config = load_config()
    project_root = os.path.join(os.path.dirname(__file__), config.get("project_root", ".."))
    
    engine = TaskEngine(project_root=project_root)
    coder = CoderAgent(project_root=project_root, config=config)
    notifier = get_notifier(config)

    print("=" * 60)
    print("🤖 [Antigravity Cloud Autonomous Agent] Active")
    print(f"📁 Workspace: {os.path.abspath(project_root)}")
    print(f"📱 Phone Alerts: {config.get('notifications', {}).get('provider', 'whatsapp').upper()}")
    print(f"⚙️ Mode: {'Daemon (Continuous)' if daemon else 'Batch (Scheduled)'}")
    print("=" * 60)

    tasks_completed = 0

    while True:
        task = engine.get_next_task()
        if not task:
            print("\n✨ All roadmap tasks completed! Nothing left to build right now.")
            break

        print(f"\n🎯 [Autopilot] Selected: {task['title']}")
        notifier.notify_task_start(task)

        success, message = coder.execute_task(task)

        if success:
            tasks_completed += 1
            engine.mark_task_done(task["title"], summary=message)
            notifier.notify_task_complete(task, len(engine.state["completed_tasks"]))
            print(f"✅ [Autopilot] Completed: {task['title']}")
        else:
            print(f"❌ [Autopilot] Failed: {task['title']} - {message}")
            notifier.notify_error(task, message)
            if task["title"] not in engine.state["failed_tasks"]:
                engine.state["failed_tasks"].append(task["title"])
            engine.save_state()

        if not daemon and tasks_completed >= max_tasks:
            print(f"\n🏁 Finished batch limit of {max_tasks} tasks.")
            break

        sleep_sec = config.get("safety", {}).get("sleep_between_tasks_sec", 5)
        print(f"⏳ Sleeping {sleep_sec}s before next task...")
        time.sleep(sleep_sec)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Cloud Autonomous Agent")
    parser.add_argument("--once", action="store_true", help="Run 1 task and exit (ideal for GitHub Actions)")
    parser.add_argument("--max", type=int, default=1, help="Max tasks to complete in this run")
    parser.add_argument("--daemon", action="store_true", help="Keep running indefinitely")

    args = parser.parse_args()
    run_autopilot(max_tasks=1 if args.once else args.max, daemon=args.daemon)
