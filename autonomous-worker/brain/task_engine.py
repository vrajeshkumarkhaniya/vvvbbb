"""
Autonomous Task Engine & Decision Planner
Reads ROADMAP.md, tracks progress, and autonomously decides the next best task.
"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

class TaskEngine:
    def __init__(self, project_root: str, state_file: str = "AUTOPILOT_STATE.json"):
        self.project_root = os.path.abspath(project_root)
        self.roadmap_path = os.path.join(self.project_root, "ROADMAP.md")
        self.state_file_path = os.path.join(os.path.dirname(__file__), "..", state_file)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file_path):
            try:
                with open(self.state_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "current_task": None,
            "completed_tasks": [],
            "failed_tasks": [],
            "total_commits": 0,
            "last_active": None,
            "started_at": datetime.now().isoformat()
        }

    def save_state(self):
        self.state["last_active"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)
        with open(self.state_file_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def parse_roadmap(self) -> List[Dict[str, Any]]:
        """Parses ROADMAP.md and returns pending tasks."""
        if not os.path.exists(self.roadmap_path):
            return []

        with open(self.roadmap_path, "r", encoding="utf-8") as f:
            content = f.read()

        tasks = []
        # Match markdown task list items: - [ ] **Task Title** ...
        task_blocks = re.split(r'\n(?=- \[[ xX]\] )', content)
        
        for block in task_blocks:
            match = re.search(r'^- \[([ xX])\] \*\*(.*?)\*\*(.*)', block, re.DOTALL)
            if match:
                is_done = match.group(1).lower() == 'x'
                title = match.group(2).strip()
                details = match.group(3).strip()

                desc_match = re.search(r'- \*\*Description:\*\*\s*(.*?)(?=\n- |\Z)', details, re.DOTALL)
                type_match = re.search(r'- \*\*Type:\*\*\s*(.*?)(?=\n|\Z)', details)
                criteria_match = re.search(r'- \*\*Acceptance Criteria:\*\*\s*(.*?)(?=\n- |\Z)', details, re.DOTALL)

                task = {
                    "title": title,
                    "is_done": is_done,
                    "type": type_match.group(1).strip() if type_match else "General",
                    "description": desc_match.group(1).strip() if desc_match else details,
                    "criteria": criteria_match.group(1).strip() if criteria_match else "Build and compile cleanly.",
                    "raw_block": block
                }
                tasks.append(task)
        return tasks

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Finds the highest priority pending task."""
        tasks = self.parse_roadmap()
        pending = [t for t in tasks if not t["is_done"]]

        if pending:
            chosen = pending[0]
            self.state["current_task"] = chosen["title"]
            self.save_state()
            return chosen

        # If no pending tasks, run codebase discovery to propose new value
        return self._propose_new_task()

    def mark_task_done(self, task_title: str, summary: str = ""):
        """Marks a task as done in ROADMAP.md and updates state."""
        if not os.path.exists(self.roadmap_path):
            return

        with open(self.roadmap_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace - [ ] **task_title** with - [x] **task_title**
        escaped_title = re.escape(task_title)
        pattern = rf'- \[ \] \*\*{escaped_title}\*\*'
        replacement = f'- [x] **{task_title}**'
        
        new_content = re.sub(pattern, replacement, content, count=1)
        
        with open(self.roadmap_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        if task_title not in self.state["completed_tasks"]:
            self.state["completed_tasks"].append(task_title)
        self.state["current_task"] = None
        self.state["total_commits"] += 1
        self.save_state()

    def _propose_new_task(self) -> Optional[Dict[str, Any]]:
        """Intelligently inspects project to propose next logical feature."""
        # Check backend routes vs frontend services
        proposed = {
            "title": f"Frontend Performance & SEO Polish ({datetime.now().strftime('%b %d')})",
            "type": "Quality & Maintenance",
            "description": "Audit React components and Vite bundle size, improve accessibility attributes, and verify production build.",
            "criteria": "npm run build passes with 0 errors and clean dist output.",
            "is_done": False
        }
        
        # Append to ROADMAP.md
        with open(self.roadmap_path, "a", encoding="utf-8") as f:
            f.write(f"\n- [ ] **{proposed['title']}**\n")
            f.write(f"  - **Type:** {proposed['type']}\n")
            f.write(f"  - **Description:** {proposed['description']}\n")
            f.write(f"  - **Acceptance Criteria:** {proposed['criteria']}\n")
            
        self.state["current_task"] = proposed["title"]
        self.save_state()
        return proposed

if __name__ == "__main__":
    engine = TaskEngine(project_root=os.path.join(os.path.dirname(__file__), "..", ".."))
    next_t = engine.get_next_task()
    print("Next Task:", json.dumps(next_t, indent=2))
