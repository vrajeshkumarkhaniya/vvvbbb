# Project Memory (`vvvbbb`)

- **Project:** Modern React + Vite web application (`vvvbbb`), configured for Vercel (`vercel.json`, `dist/` output).
- **GitHub Repository:** `https://github.com/vrajeshkumarkhaniya/vvvbbb` (`main` branch).
- **Cloud Autonomous Worker:** `autonomous-worker/` connected to `ROADMAP.md` and Telegram (`@Lazyy_byddy_bot`).
- **Security Rule:** Keep `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` out of `autonomous-worker/config.json` in git; load from environment variables / GitHub Repository Secrets.
- **Verification Rule:** Always run `npm.cmd run build` (Vite build check) and `python -m py_compile` on `autonomous-worker` scripts before pushing.
