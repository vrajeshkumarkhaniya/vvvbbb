const GITHUB_API = 'https://api.github.com';

function ghHeaders(token) {
  return {
    Authorization: `Bearer ${token}`,
    Accept: 'application/vnd.github+json',
    'User-Agent': 'vvvbbb-telegram-webhook/1.0',
    'X-GitHub-Api-Version': '2022-11-28',
  };
}

async function sendTelegram(botToken, chatId, text) {
  const res = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      parse_mode: 'HTML',
      disable_web_page_preview: true,
    }),
  });
  return res.ok;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function parseRoadmap(markdown) {
  const blocks = markdown.split(/\n(?=- \[[ xX]\] )/);
  const tasks = [];
  for (const block of blocks) {
    const match = block.match(/^- \[([ xX])\] \*\*(.*?)\*\*/);
    if (match) {
      tasks.push({
        done: match[1].toLowerCase() === 'x',
        title: match[2].trim(),
      });
    }
  }
  return tasks;
}

function insertPriorityTask(markdown, cleanTask) {
  const newEntry =
    `- [ ] **${cleanTask}**\n` +
    `  - **Type:** User Request (via 24/7 Telegram Webhook)\n` +
    `  - **Description:** ${cleanTask}\n` +
    `  - **Acceptance Criteria:** Implemented cleanly and \`npm run build\` passes with 0 errors.\n`;

  const firstPendingIdx = markdown.indexOf('\n- [ ] ');
  if (firstPendingIdx !== -1) {
    return (
      markdown.slice(0, firstPendingIdx + 1) +
      newEntry +
      '\n' +
      markdown.slice(firstPendingIdx + 1)
    );
  }
  return `${markdown.trimEnd()}\n\n${newEntry}`;
}

function isStatusQuery(lower) {
  const statusWords = [
    'status',
    'progress',
    'kitna kaam',
    'kitna kam',
    'kaha tak',
    'kya hua',
    'kya chal raha',
    'kitni der',
    'update',
    'report',
  ];
  return statusWords.some((w) => lower.includes(w));
}

function extractTaskTitle(rawText) {
  const cleaned = rawText
    .replace(/^(add task|task add|ye add karo|ye banao|new task|task)[:\s.\-]*/i, '')
    .trim();
  return cleaned || rawText.trim();
}

export default async function handler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).json({ ok: true, service: 'vvvbbb-24x7-telegram-trigger' });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const webhookSecret = process.env.TELEGRAM_WEBHOOK_SECRET;
  if (webhookSecret && req.headers['x-telegram-bot-api-secret-token'] !== webhookSecret) {
    return res.status(401).json({ error: 'Invalid webhook secret' });
  }

  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const allowedChatId = String(process.env.TELEGRAM_CHAT_ID || '');
  const ghToken = process.env.GITHUB_TOKEN;
  const ghOwner = process.env.GITHUB_OWNER || 'vrajeshkumarkhaniya';
  const ghRepo = process.env.GITHUB_REPO || 'vvvbbb';
  const ghBranch = process.env.GITHUB_BRANCH || 'main';

  if (!botToken || !allowedChatId || !ghToken) {
    return res.status(500).json({ error: 'Missing required environment variables' });
  }

  try {
    const update = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const msg = update.message || update.edited_message;
    if (!msg || !msg.text) {
      return res.status(200).json({ ok: true, ignored: true });
    }

    const chatId = String(msg.chat?.id || '');
    if (chatId !== allowedChatId) {
      return res.status(200).json({ ok: true, unauthorized_chat: true });
    }

    const text = msg.text.trim();
    const lower = text.toLowerCase();

    if (text === '/start' || text === '/help') {
      await sendTelegram(
        botToken,
        chatId,
        '🤖 <b>24/7 Cloud Trigger Active Hai!</b>\n\n' +
          'PC bandh hone par bhi aap mujhe seedha task de sakte ho:\n' +
          '• Koi bhi task likho (jaise: <code>ye banao: Hero section me stats badges add karo</code>)\n' +
          '• Status dekhne ke liye likho: <code>status</code> ya <code>kitna kaam hua</code>'
      );
      return res.status(200).json({ ok: true });
    }

    // Fetch current ROADMAP.md from GitHub
    const roadmapRes = await fetch(
      `${GITHUB_API}/repos/${ghOwner}/${ghRepo}/contents/ROADMAP.md?ref=${ghBranch}`,
      { headers: ghHeaders(ghToken) }
    );
    if (!roadmapRes.ok) {
      throw new Error(`Failed to fetch ROADMAP.md (${roadmapRes.status})`);
    }
    const roadmapJson = await roadmapRes.json();
    const currentRoadmap = Buffer.from(roadmapJson.content, 'base64').toString('utf-8');

    // 1. Handle status queries
    if (isStatusQuery(lower)) {
      const tasks = parseRoadmap(currentRoadmap);
      const done = tasks.filter((t) => t.done);
      const pending = tasks.filter((t) => !t.done);
      const pct = tasks.length ? Math.round((done.length / tasks.length) * 100) : 0;

      const runsRes = await fetch(
        `${GITHUB_API}/repos/${ghOwner}/${ghRepo}/actions/workflows/autonomous-agent.yml/runs?per_page=1`,
        { headers: ghHeaders(ghToken) }
      );
      let runnerState = 'Idle';
      if (runsRes.ok) {
        const runsData = await runsRes.json();
        const latest = runsData.workflow_runs?.[0];
        if (latest) {
          runnerState = `${latest.status}${latest.conclusion ? ` (${latest.conclusion})` : ''}`;
        }
      }

      const nextTitle = pending[0]?.title || 'Sabhi tasks complete hain!';
      const reply =
        `📊 <b>Live 24/7 Cloud Status (vvvbbb)</b>\n\n` +
        `• <b>Progress:</b> ${pct}% (${done.length}/${tasks.length} tasks)\n` +
        `• <b>Cloud Runner:</b> ${escapeHtml(runnerState)}\n` +
        `• <b>Agla Task:</b> ${escapeHtml(nextTitle)}\n\n` +
        `🔗 https://test-eta-snowy-j4wco9595m.vercel.app`;

      await sendTelegram(botToken, chatId, reply);
      return res.status(200).json({ ok: true, mode: 'status' });
    }

    // 2. Handle new task / change request (explicit prefix OR natural request)
    const cleanTask = extractTaskTitle(text);
    const updatedRoadmap = insertPriorityTask(currentRoadmap, cleanTask);

    const updateRes = await fetch(
      `${GITHUB_API}/repos/${ghOwner}/${ghRepo}/contents/ROADMAP.md`,
      {
        method: 'PUT',
        headers: { ...ghHeaders(ghToken), 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `chore(telegram): queue task "${cleanTask.slice(0, 60)}"`,
          content: Buffer.from(updatedRoadmap, 'utf-8').toString('base64'),
          sha: roadmapJson.sha,
          branch: ghBranch,
        }),
      }
    );

    if (!updateRes.ok) {
      const errBody = await updateRes.text();
      throw new Error(`Failed to update ROADMAP.md: ${updateRes.status} ${errBody}`);
    }

    // Immediately trigger GitHub Actions Cloud Runner
    const dispatchRes = await fetch(
      `${GITHUB_API}/repos/${ghOwner}/${ghRepo}/actions/workflows/autonomous-agent.yml/dispatches`,
      {
        method: 'POST',
        headers: { ...ghHeaders(ghToken), 'Content-Type': 'application/json' },
        body: JSON.stringify({ ref: ghBranch }),
      }
    );

    const triggered = dispatchRes.status === 204;
    await sendTelegram(
      botToken,
      chatId,
      `✅ <b>Task Queue Ho Gaya &amp; Cloud Runner ${triggered ? 'Start' : 'Scheduled'}!</b>\n\n` +
        `📋 <b>Task:</b> ${escapeHtml(cleanTask)}\n` +
        `☁️ <b>Mode:</b> 24/7 GitHub Cloud + Vercel Auto-Deploy\n\n` +
        `⏱️ Lagbhag 2 se 4 minute mein build verify ho kar update yahan aa jayega!`
    );

    return res.status(200).json({ ok: true, mode: 'task_queued', triggered });
  } catch (err) {
    console.error('[Telegram Webhook Error]', err);
    return res.status(200).json({ ok: false, error: err.message });
  }
}
