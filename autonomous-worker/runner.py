"""
Main Autonomous Cloud Agent Runner.
Executes pending ROADMAP.md tasks, verifies build, commits & pushes to GitHub, and notifies Telegram.
"""

import os
import sys
import json
import time
import argparse
import subprocess

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
    provider = config.get("notifications", {}).get("provider", "telegram").lower()
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


def run_git(project_root: str, args: list) -> tuple[int, str]:
    res = subprocess.run(
        ["git"] + args,
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return res.returncode, (res.stdout + "\n" + res.stderr).strip()


def commit_and_push(project_root: str, config: dict, task_title: str, changed_files: list[str]) -> tuple[bool, str]:
    git_cfg = config.get("git", {})
    if not git_cfg.get("auto_commit", True):
        return True, "auto_commit disabled"

    files_to_stage = list(dict.fromkeys(changed_files + ["ROADMAP.md", "autonomous-worker/AUTOPILOT_STATE.json"]))
    for rel_path in files_to_stage:
        if os.path.exists(os.path.join(project_root, rel_path)):
            run_git(project_root, ["add", rel_path])

    commit_msg = f"feat(autopilot): {task_title}"
    code, out = run_git(project_root, ["commit", "-m", commit_msg])
    if code != 0 and "nothing to commit" not in out.lower():
        return False, f"git commit failed: {out}"

    if git_cfg.get("auto_push", True):
        branch = git_cfg.get("branch", "main")
        run_git(project_root, ["pull", "--rebase", "origin", branch])
        p_code, p_out = run_git(project_root, ["push", "origin", branch])
        if p_code != 0:
            return False, f"git push failed: {p_out}"

    return True, "Committed & pushed to GitHub."


def run_autopilot(max_tasks: int = 1, daemon: bool = False):
    config = load_config()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), config.get("project_root", "..")))

    engine = TaskEngine(project_root=project_root)
    coder = CoderAgent(project_root=project_root, config=config)
    notifier = get_notifier(config)

    print("=" * 60)
    print("🤖 [Antigravity Cloud Autonomous Agent] Active")
    print(f"📁 Workspace: {project_root}")
    print(f"📱 Phone Alerts: {config.get('notifications', {}).get('provider', 'telegram').upper()}")
    print(f"⚙️ Mode: {'Daemon (Continuous)' if daemon else 'Batch (Scheduled)'}")
    print("=" * 60)

    attempts = 0
    tasks_completed = 0

    while True:
        task = engine.get_next_task()
        if not task:
            print("\n✨ All roadmap tasks completed! Nothing left to build right now.")
            break

        attempts += 1
        print(f"\n🎯 [Autopilot] Selected: {task['title']}")
        notifier.notify_task_start(task)

        success, message, changed_files = coder.execute_task(task)

        if success:
            engine.mark_task_done(task["title"], summary=message)
            git_ok, git_msg = commit_and_push(project_root, config, task["title"], changed_files)
            if git_ok:
                tasks_completed += 1
                notifier.notify_task_complete(task, len(engine.state["completed_tasks"]))
                print(f"✅ [Autopilot] Completed: {task['title']} ({git_msg})")
            else:
                print(f"❌ [Autopilot] Git sync failed: {git_msg}")
                notifier.notify_error(task, git_msg)
        else:
            print(f"❌ [Autopilot] Failed: {task['title']} - {message}")
            notifier.notify_error(task, message)
            if task["title"] not in engine.state["failed_tasks"]:
                engine.state["failed_tasks"].append(task["title"])
            engine.save_state()

        if not daemon and attempts >= max_tasks:
            print(f"\n🏁 Finished batch run ({tasks_completed}/{attempts} tasks succeeded).")
            break

        sleep_sec = config.get("safety", {}).get("sleep_between_tasks_sec", 5)
        print(f"⏳ Sleeping {sleep_sec}s before next task...")
        time.sleep(sleep_sec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Cloud Autonomous Agent")
    parser.add_argument("--once", action="store_true", help="Run 1 task and exit (ideal for GitHub Actions)")
    parser.add_argument("--max", type=int, default=1, help="Max tasks to attempt in this run")
    parser.add_argument("--daemon", action="store_true", help="Keep running indefinitely")

    args = parser.parse_args()
    run_autopilot(max_tasks=1 if args.once else args.max, daemon=args.daemon)
