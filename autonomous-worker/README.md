# 🤖 Antigravity 24/7 Cloud Autonomous Agent

A continuous, self-governing coding agent that works on your project **even when your PC is turned off**, makes architectural decisions, runs automated tests, self-heals bugs, commits clean code to Git, and alerts your phone in real time!

---

## 🌟 How It Works (The 3 Brains)

1. **Master Roadmap (`ROADMAP.md`):**
   * Acts as the shared memory between you and the Agent.
   * You write what you want (or let the Agent propose new features).
   * The Agent tracks `[ ]` (Pending) and changes it to `[x]` (Done) automatically.

2. **Self-Healing Code Loop (`coder_agent.py`):**
   * Writes the code based on the task description.
   * Immediately runs syntax and build verification (`node -c`, `npm run build`, `tsc --noEmit`).
   * If any error happens, it debugs itself, applies a fix, and re-verifies.
   * Only commits to Git when the build is 100% green!

3. **Telegram Phone Alerts (`telegram_notifier.py`):**
   * Sends real-time push alerts to your phone:
     * 🚀 Task Started
     * ✅ Task Completed with verification proof
     * ⚠️ Self-Healing alert if something breaks and is fixed

---

## ☁️ How To Run It When Your PC Is Off (GitHub Actions Cloud)

The repository includes a ready-to-use cloud runner at `.github/workflows/autonomous-agent.yml`:

1. **Push your code to GitHub:**
   ```bash
   git push origin <your-branch>
   ```

2. **Add GitHub Repository Secrets:**
   In your GitHub Repo ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions**:
   * `GEMINI_API_KEY`: Your Gemini API Key (free from Google AI Studio).
   * `TELEGRAM_BOT_TOKEN`: (Optional) Your Telegram bot token.
   * `TELEGRAM_CHAT_ID`: (Optional) Your personal Telegram user ID.

3. **That's it!**
   * GitHub's cloud runners will automatically wake up on schedule (every 3 hours) or whenever you tap **"Run workflow"** from the GitHub mobile app on your phone.
   * Your PC can be completely turned off. The Agent codes, tests, commits, and notifies your phone!

---

## 💻 How To Run Locally (If PC Is Left On)

Run a single task batch:
```bash
python autonomous-worker/runner.py --once
```

Run continuously as a daemon:
```bash
python autonomous-worker/runner.py --daemon
```

---

## 📱 How To Enable Phone Notifications (60 Seconds Setup)

1. Open Telegram on your phone and search for `@BotFather`.
2. Send `/newbot`, choose a name and username (e.g. `MyDairyDevBot`).
3. Copy the **HTTP API Token** and set it in your environment:
   ```bash
   $env:TELEGRAM_BOT_TOKEN="your_token_here"
   ```
4. Search `@userinfobot` on Telegram to get your **Chat ID** and set it:
   ```bash
   $env:TELEGRAM_CHAT_ID="your_chat_id_here"
   ```
5. From then on, every time a task starts or finishes, your phone will buzz with live progress!
