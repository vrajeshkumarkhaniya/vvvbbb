"""
Autonomous Coder Agent with Self-Testing and Self-Healing Loop.
Connects to Gemini API to execute roadmap tasks safely and verify builds.
"""

import os
import json
import time
import urllib.request
import urllib.error
import subprocess
from typing import Dict, Any, List, Tuple


class CoderAgent:
    def __init__(self, project_root: str, config: Dict[str, Any]):
        self.project_root = os.path.abspath(project_root)
        self.config = config
        self.api_key = (
            os.environ.get(config.get("ai", {}).get("api_key_env", "GEMINI_API_KEY"))
            or config.get("ai", {}).get("api_key", "")
        )
        self.model = config.get("ai", {}).get("model", "gemini-3.1-flash-lite")

    def execute_task(self, task: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """Executes a roadmap task via Gemini API and runs build verification."""
        title = task.get("title", "")
        desc = task.get("description", "")

        print(f"\n🚀 [CoderAgent] Starting task: {title}")
        print(f"📋 Details: {desc[:120]}...")

        return self._execute_with_llm(task)

    def _collect_context(self) -> str:
        """Collects key project files so the model understands the existing codebase."""
        candidates = [
            "package.json",
            "index.html",
            "src/App.jsx",
            "src/index.css",
            "src/data/siteData.js",
            "ROADMAP.md",
        ]
        snippets: List[str] = []
        for rel in candidates:
            abs_path = os.path.join(self.project_root, rel)
            if os.path.isfile(abs_path):
                try:
                    with open(abs_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if len(content) > 6000:
                        content = content[:6000] + "\n... [truncated]"
                    snippets.append(f"=== {rel} ===\n{content}")
                except Exception:
                    pass
        return "\n\n".join(snippets)

    def _is_safe_path(self, rel_path: str) -> bool:
        norm = rel_path.replace("\\", "/").lstrip("/")
        if not norm or ".." in norm.split("/"):
            return False
        blocked_prefixes = (
            ".git/",
            ".github/",
            "node_modules/",
            "autonomous-worker/",
            "api/",
            ".env",
            "package-lock.json",
        )
        return not norm.startswith(blocked_prefixes) and norm not in (".env", "package-lock.json")

    def _execute_with_llm(self, task: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """Calls Gemini API with model fallback and build verification."""
        if not self.api_key:
            return False, "GEMINI_API_KEY environment variable is not configured.", []

        project_context = self._collect_context()
        prompt = f"""You are an Autonomous Senior Frontend Engineer working on the vvvbbb React + Vite web application (deployed on Vercel).

Task Title: {task['title']}
Description: {task['description']}
Acceptance Criteria: {task['criteria']}

Current Project Files:
{project_context}

Return a valid JSON object ONLY with this exact schema:
{{
  "files": [
    {{
      "path": "relative/path/from/repo/root",
      "content": "complete updated file contents"
    }}
  ],
  "summary": "short 1-line summary of what changed"
}}

Rules:
- Only edit frontend website files (such as index.html, src/*, public/*). Never touch .github/, autonomous-worker/, api/, or package-lock.json.
- Provide COMPLETE file contents for every file you include (never placeholders or '...').
- Ensure React JSX and CSS compile cleanly with `npm run build`.
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
        }

        models_to_try = list(
            dict.fromkeys(
                [
                    self.model,
                    "gemini-3.1-flash-lite",
                    "gemini-3.5-flash",
                    "gemini-2.5-flash",
                    "gemini-flash-latest",
                ]
            )
        )
        last_error = ""

        for m in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=90) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                res_obj = json.loads(text)

                files_list = res_obj.get("files")
                if not files_list and res_obj.get("file_path") and res_obj.get("content") is not None:
                    files_list = [{"path": res_obj["file_path"], "content": res_obj["content"]}]

                if not files_list:
                    last_error = f"Model {m} returned no files."
                    continue

                written_files: List[str] = []
                for item in files_list:
                    rel_path = str(item.get("path", "")).strip()
                    content = item.get("content")
                    if not self._is_safe_path(rel_path) or content is None:
                        continue
                    abs_path = os.path.join(self.project_root, rel_path)
                    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                    with open(abs_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    written_files.append(rel_path)

                if not written_files:
                    last_error = f"Model {m} produced no valid writable paths."
                    continue

                code, out = self._run_command("npm run build")
                if code != 0:
                    # Revert modified tracked files before failing or trying fallback
                    self._run_command("git checkout -- src index.html public")
                    last_error = f"Build failed: {out[-400:]}"
                    print(f"[CoderAgent] {last_error}")
                    continue

                summary = res_obj.get("summary") or "Task implemented and build verified."
                return True, summary, written_files

            except Exception as e:
                last_error = str(e)
                print(f"[CoderAgent] Model {m} error: {e}. Trying fallback...")
                if "429" in str(e):
                    time.sleep(5)
                continue

        return False, f"LLM execution error across all models: {last_error}", []

    def _run_command(self, cmd: str) -> Tuple[int, str]:
        """Runs shell command in project root with timeout."""
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            return res.returncode, (res.stdout + "\n" + res.stderr).strip()
        except Exception as e:
            return 1, str(e)
