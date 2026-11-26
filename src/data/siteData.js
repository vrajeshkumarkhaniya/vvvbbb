export const SERVICES = [
  {
    id: 'web',
    title: 'Web Applications',
    description:
      'Fast, SEO-ready React & Next.js web apps engineered for conversion, accessibility, and zero-downtime Vercel deployments.',
  },
  {
    id: 'mobile',
    title: 'Mobile & Cross-Platform',
    description:
      'Native-feel React Native & Expo mobile apps with offline-first sync, clean gestures, and Play Store release pipelines.',
  },
  {
    id: 'ai',
    title: 'AI & Cloud Automation',
    description:
      'Autonomous workflows, Gemini-powered assistants, and real-time Telegram alerts that keep shipping 24/7.',
  },
];

export const PROJECTS = [
  {
    id: 'dairymanager',
    title: 'DairyManager Suite',
    category: 'Mobile',
    metric: '4x faster billing',
    summary:
      'End-to-end customer & owner mobile platform for daily milk delivery tracking, automated monthly invoicing, and instant receipts.',
    stack: ['React Native', 'Node.js', 'MongoDB', 'Expo'],
    highlights: [
      'Real-time delivery logs and automated customer statements',
      'QR receipt generation and offline queue recovery',
      'Separate Owner & Customer apps with role-based auth',
    ],
  },
  {
    id: 'audiview',
    title: 'AudiView 3D Showcase',
    category: 'Web',
    metric: '99 Lighthouse Score',
    summary:
      'Interactive 3D product configurator and high-FPS web experience built for instant browser rendering across desktop and mobile.',
    stack: ['React', 'Vite', 'WebGL', 'Vercel'],
    highlights: [
      'Sub-second initial paint with asset preloading',
      'Smooth camera presets and responsive touch controls',
      'Automated CI preview deployments on every PR',
    ],
  },
  {
    id: 'cloud-runner',
    title: '24/7 Cloud Autonomous Worker',
    category: 'AI',
    metric: 'Zero-downtime shipping',
    summary:
      'GitHub Actions + Gemini autonomous coding pipeline with syntax verification, self-healing retries, and live Telegram phone alerts.',
    stack: ['Python', 'GitHub Actions', 'Gemini API', 'Telegram Bot'],
    highlights: [
      'Reads ROADMAP.md tasks and executes verified commits',
      'Pushes live progress reports directly to Telegram',
      'Supports remote task creation directly from mobile chat',
    ],
  },
  {
    id: 'pulse-crm',
    title: 'Pulse Commerce Portal',
    category: 'Web',
    metric: '+42% checkout speed',
    summary:
      'Modern storefront and analytics dashboard featuring instant search, optimistic cart updates, and streamlined checkout flows.',
    stack: ['React', 'TypeScript', 'Edge Functions', 'Analytics'],
    highlights: [
      'Edge-cached catalog responses under 60ms',
      'Accessible keyboard-first navigation and dark/light themes',
      'Real-time order tracking and automated webhooks',
    ],
  },
];

export const PLANS = [
  {
    name: 'Launch Pad',
    price: '$499',
    period: 'one-time sprint',
    featured: false,
    description: 'Ideal for startups needing a high-converting landing page live in days.',
    features: [
      'Custom responsive design & dark/light theme',
      'GitHub repository + Vercel production deploy',
      'SEO metadata & performance optimization',
      'Interactive contact & lead capture form',
    ],
  },
  {
    name: 'Growth Product',
    price: '$1,299',
    period: 'full product build',
    featured: true,
    description: 'Complete full-stack web or mobile MVP with automated CI/CD.',
    features: [
      'Multi-page React / Next.js web application',
      'Backend API & database integration',
      '24/7 Cloud Runner + Telegram alerts setup',
      'Automated build & regression checks',
    ],
  },
  {
    name: 'Autonomous Retainer',
    price: '$799',
    period: 'per month',
    featured: false,
    description: 'Continuous feature shipping, cloud monitoring, and priority updates.',
    features: [
      'Weekly roadmap feature delivery',
      'Real-time uptime & Telegram notifications',
      'Performance & security audits',
      'Direct priority support',
    ],
  },
];

export const FAQS = [
  {
    q: 'How fast can a new website go live on Vercel?',
    a: 'Core landing pages and portfolios ship within 48 hours, with automatic GitHub-to-Vercel preview and production deployments.',
  },
  {
    q: 'Can updates continue automatically when my PC is turned off?',
    a: 'Yes. With GitHub Actions Cloud Runner connected to ROADMAP.md and Telegram, queued tasks run in the cloud and report progress to your phone.',
  },
  {
    q: 'Can I customize sections, branding, and colors later?',
    a: 'Everything is cleanly structured in modular React components and CSS variables so branding, copy, and pages can be updated in minutes.',
  },
];
