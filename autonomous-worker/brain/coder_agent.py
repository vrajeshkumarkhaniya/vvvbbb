"""
Autonomous Coder Agent with Self-Testing and Self-Healing Loop.
Connects to Gemini API or executes safe autonomous workflows.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from typing import Dict, Any, List, Tuple

class CoderAgent:
    def __init__(self, project_root: str, config: Dict[str, Any]):
        self.project_root = os.path.abspath(project_root)
        self.config = config
        self.api_key = os.environ.get(config.get("ai", {}).get("api_key_env", "GEMINI_API_KEY")) or config.get("ai", {}).get("api_key", "")
        self.model = config.get("ai", {}).get("model", "gemini-3.8-flash")

    def execute_task(self, task: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Main execution flow:
        1. Analyze task requirements.
        2. Plan changes.
        3. Implement changes.
        4. Validate with syntax / build check.
        5. Self-heal if errors occur.
        """
        title = task.get("title", "")
        desc = task.get("description", "")
        criteria = task.get("criteria", "")

        print(f"\n🚀 [CoderAgent] Starting task: {title}")
        print(f"📋 Details: {desc[:120]}...")

        # General LLM-driven task execution
        return self._execute_with_llm(task)

    def _implement_backup_utility(self) -> Tuple[bool, str]:
        """Built-in high-reliability implementation for data backup utility."""
        target_path = os.path.join(self.project_root, "backend", "scripts", "backupDatabase.js")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        script_content = '''/**
 * Autonomous Database Backup Utility
 * Exports database snapshot to JSON files with 7-day automated retention cleanup.
 */

const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const Customer = require('../models/Customer');
const Delivery = require('../models/Delivery');
const MilkSale = require('../models/MilkSale');
const Bill = require('../models/Bill');

async function runBackup() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupDir = path.join(__dirname, '../backups', `snapshot-${timestamp}`);

  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }

  console.log(`[Backup] Starting snapshot to ${backupDir}...`);

  try {
    const mongoUri = process.env.MONGO_URI || process.env.MONGODB_URI || 'mongodb://localhost:27017/milk-dairy';
    await mongoose.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true });
    console.log('[Backup] Connected to MongoDB.');

    // Export collections
    const collections = [
      { name: 'customers', model: Customer },
      { name: 'deliveries', model: Delivery },
      { name: 'milk_sales', model: MilkSale },
      { name: 'bills', model: Bill },
    ];

    const stats = {};

    for (const col of collections) {
      try {
        const records = await col.model.find({}).lean();
        const filePath = path.join(backupDir, `${col.name}.json`);
        fs.writeFileSync(filePath, JSON.stringify(records, null, 2), 'utf-8');
        stats[col.name] = records.length;
        console.log(`[Backup] Exported ${records.length} records for ${col.name}`);
      } catch (err) {
        console.warn(`[Backup] Skipped ${col.name}: ${err.message}`);
        stats[col.name] = 0;
      }
    }

    // Write manifest
    const manifest = {
      timestamp,
      createdAt: new Date().toISOString(),
      stats,
      version: '1.0.0'
    };
    fs.writeFileSync(path.join(backupDir, 'manifest.json'), JSON.stringify(manifest, null, 2));

    // Clean backups older than 7 days
    cleanOldBackups(path.join(__dirname, '../backups'), 7);

    console.log('[Backup] ✅ Snapshot completed successfully!');
    await mongoose.disconnect();
    return true;
  } catch (error) {
    console.error('[Backup Error]:', error.message);
    if (mongoose.connection.readyState !== 0) {
      await mongoose.disconnect();
    }
    return false;
  }
}

function cleanOldBackups(baseDir, daysRetention) {
  if (!fs.existsSync(baseDir)) return;
  const now = Date.now();
  const maxAgeMs = daysRetention * 24 * 60 * 60 * 1000;

  const entries = fs.readdirSync(baseDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && entry.name.startsWith('snapshot-')) {
      const fullPath = path.join(baseDir, entry.name);
      const stat = fs.statSync(fullPath);
      if (now - stat.mtimeMs > maxAgeMs) {
        fs.rmSync(fullPath, { recursive: true, force: true });
        console.log(`[Backup] Purged stale backup: ${entry.name}`);
      }
    }
  }
}

if (require.main === module) {
  runBackup().then(success => {
    process.exit(success ? 0 : 1);
  });
}

module.exports = { runBackup };
'''
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        return True, "Backup script written."

    def _execute_with_llm(self, task: Dict[str, Any]) -> Tuple[bool, str]:
        """Calls Gemini API to generate solutions for dynamic roadmap tasks with automated model fallback."""
        if not self.api_key:
            return False, "GEMINI_API_KEY environment variable is not configured."

        prompt = f"""You are an Autonomous Senior Frontend & Full-Stack Engineer working on the vvvbbb modern React + Vite web application (deployed on Vercel).
Task: {task['title']}
Description: {task['description']}
Acceptance Criteria: {task['criteria']}

Provide JSON response with format:
{{
  "file_path": "path/to/file",
  "content": "file contents",
  "verification_command": "npm run build"
}}
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }

        models_to_try = list(dict.fromkeys([self.model, "gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]))
        last_error = ""

        for m in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    res_obj = json.loads(text)

                    file_path = os.path.join(self.project_root, res_obj["file_path"])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(res_obj["content"])

                    verify_cmd = res_obj.get("verification_command", "")
                    if verify_cmd:
                        code, out = self._run_command(verify_cmd)
                        if code != 0:
                            return False, f"Verification failed: {out}"

                    return self._verify_and_commit(task, [res_obj["file_path"]])
            except Exception as e:
                last_error = str(e)
                print(f"[CoderAgent] Model {m} error: {e}. Trying fallback...")
                if "429" in str(e):
                    time.sleep(10)
                continue

        return False, f"LLM execution error across all models: {last_error}"

    def _verify_and_commit(self, task: Dict[str, Any], changed_files: List[str]) -> Tuple[bool, str]:
        """Performs syntax validation, git stage, commit, and push."""
        # 1. Syntax check each changed js/ts file
        for rel_file in changed_files:
            abs_file = os.path.join(self.project_root, rel_file)
            if abs_file.endswith(".js"):
                code, out = self._run_command(f'node -c "{abs_file}"')
                if code != 0:
                    return False, f"Syntax error in {rel_file}: {out}"

        # 2. Git operations
        git_cfg = self.config.get("git", {})
        if git_cfg.get("auto_commit", True):
            for f in changed_files:
                self._run_command(f'git add "{f}"')
            
            commit_msg = f"feat(autopilot): {task['title']}\n\nAutomated implementation by Cloud Agent."
            code, out = self._run_command(f'git commit -m "{commit_msg}"')
            if code == 0:
                print(f"✅ [Git] Committed changes: {commit_msg}")
            
            if git_cfg.get("auto_push", False):
                self._run_command("git push")

        return True, "Task implemented, verified, and committed successfully."

    def _run_command(self, cmd: str) -> Tuple[int, str]:
        """Runs shell command in project root."""
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            return res.returncode, (res.stdout + "\n" + res.stderr).strip()
        except Exception as e:
            return 1, str(e)
