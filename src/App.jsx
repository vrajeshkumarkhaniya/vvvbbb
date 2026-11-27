import React, { useEffect, useState } from 'react';
import {
  ArrowRight,
  Bot,
  Check,
  ChevronDown,
  Code2,
  Cpu,
  ExternalLink,
  GitBranch,
  Globe,
  Menu,
  Moon,
  Rocket,
  Send,
  Smartphone,
  Sparkles,
  Sun,
  X,
} from 'lucide-react';
import { FAQS, PLANS, PROJECTS, SERVICES } from './data/siteData';
import Testimonials from './components/Testimonials';

const SERVICE_ICONS = {
  web: Globe,
  mobile: Smartphone,
  ai: Bot,
};

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeFilter, setActiveFilter] = useState('All');
  const [selectedProject, setSelectedProject] = useState(null);
  const [openFaq, setOpenFaq] = useState(0);
  const [formState, setFormState] = useState({
    name: '',
    email: '',
    service: 'Web Applications',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const categories = ['All', 'Web', 'Mobile', 'AI'];
  const filteredProjects =
    activeFilter === 'All'
      ? PROJECTS
      : PROJECTS.filter((item) => item.category === activeFilter);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!formState.name.trim() || !formState.email.trim()) return;
    setSubmitted(true);
    setFormState({
      name: '',
      email: '',
      service: 'Web Applications',
      message: '',
    });
  };

  return (
    <>
      <div className="ambient-bg" aria-hidden="true" />

      <header className="navbar">
        <div className="container navbar-inner">
          <a href="#top" className="brand">
            <span className="brand-mark">
              <Sparkles size={18} />
            </span>
            <span>98.5 Studio</span>
          </a>

          <nav className={`nav-links ${menuOpen ? 'open' : ''}`} aria-label="Primary">
            <a href="#services" onClick={() => setMenuOpen(false)}>Services</a>
            <a href="#work" onClick={() => setMenuOpen(false)}>Work</a>
            <a href="#testimonials" onClick={() => setMenuOpen(false)}>Reviews</a>
            <a href="#pricing" onClick={() => setMenuOpen(false)}>Pricing</a>
            <a href="#faq" onClick={() => setMenuOpen(false)}>FAQ</a>
            <a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>
          </nav>

          <div className="nav-actions">
            <button
              type="button"
              className="icon-btn"
              onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
              aria-label="Toggle color theme"
            >
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            <a href="#contact" className="btn btn-primary btn-sm">
              Start Project
            </a>
            <button
              type="button"
              className="icon-btn mobile-menu-btn"
              onClick={() => setMenuOpen((o) => !o)}
              aria-label="Toggle navigation menu"
            >
              {menuOpen ? <X size={18} /> : <Menu size={18} />}
            </button>
          </div>
        </div>
      </header>

      <main id="top">
        {/* Hero */}
        <section className="hero">
          <div className="container hero-grid">
            <div>
              <div className="pill">
                <Rocket size={14} />
                <span>Cloud-Automated Web & AI Studio</span>
              </div>
              <h1>
                Build faster. Ship smarter.{' '}
                <span className="gradient-text">Scale without limits.</span>
              </h1>
              <p className="hero-sub">
                We design and engineer high-converting websites, mobile apps, and 24/7
                autonomous cloud workflows deployed straight from GitHub to Vercel.
              </p>

              <div className="hero-cta">
                <a href="#contact" className="btn btn-primary">
                  Launch Your Website <ArrowRight size={17} />
                </a>
                <a href="#work" className="btn btn-secondary">
                  Explore Showcase
                </a>
              </div>

              <div className="hero-stats">
                <div>
                  <div className="stat-value">99.9%</div>
                  <div className="stat-label">Vercel Edge Uptime</div>
                </div>
                <div>
                  <div className="stat-value">24/7</div>
                  <div className="stat-label">Cloud Runner Sync</div>
                </div>
                <div>
                  <div className="stat-value">&lt;1s</div>
                  <div className="stat-label">Global Page Load</div>
                </div>
              </div>
            </div>

            <aside className="hero-card" aria-label="Live deployment pipeline">
              <div className="hero-card-header">
                <strong>Deployment Pipeline</strong>
                <span className="status-dot">Cloud Active</span>
              </div>
              <div className="pipeline-list">
                <div className="pipeline-item">
                  <div className="pipeline-item-left">
                    <span className="pipeline-icon">
                      <Code2 size={17} />
                    </span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.94rem' }}>Vite + React Build</div>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        Zero-error production bundle
                      </div>
                    </div>
                  </div>
                  <span className="pipeline-badge">Verified</span>
                </div>

                <div className="pipeline-item">
                  <div className="pipeline-item-left">
                    <span className="pipeline-icon">
                      <GitBranch size={17} />
                    </span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.94rem' }}>GitHub Sync (vvvbbb)</div>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        Automated Cloud Runner active
                      </div>
                    </div>
                  </div>
                  <span className="pipeline-badge">Connected</span>
                </div>

                <div className="pipeline-item">
                  <div className="pipeline-item-left">
                    <span className="pipeline-icon">
                      <Cpu size={17} />
                    </span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.94rem' }}>Telegram Alerts</div>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        Live task status to your phone
                      </div>
                    </div>
                  </div>
                  <span className="pipeline-badge">Online</span>
                </div>
              </div>
            </aside>
          </div>
        </section>

        {/* Services */}
        <section id="services" className="section">
          <div className="container">
            <div className="section-header">
              <div>
                <div className="section-eyebrow">Capabilities</div>
                <h2 className="section-title">Everything needed to ship online</h2>
              </div>
              <p className="section-desc">
                From crisp interfaces to automated deployment pipelines, every layer is built
                for speed, reliability, and effortless maintenance.
              </p>
            </div>

            <div className="grid-3">
              {SERVICES.map((service) => {
                const Icon = SERVICE_ICONS[service.id] || Globe;
                return (
                  <article key={service.id} className="card">
                    <div className="card-icon">
                      <Icon size={22} />
                    </div>
                    <h3>{service.title}</h3>
                    <p>{service.description}</p>
                  </article>
                );
              })}
            </div>
          </div>
        </section>

        {/* Portfolio Work */}
        <section id="work" className="section">
          <div className="container">
            <div className="section-header">
              <div>
                <div className="section-eyebrow">Selected Work</div>
                <h2 className="section-title">Products shipped &amp; running live</h2>
              </div>
              <div className="filter-tabs" role="tablist" aria-label="Filter projects">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    role="tab"
                    aria-selected={activeFilter === cat}
                    className={`tab-btn ${activeFilter === cat ? 'active' : ''}`}
                    onClick={() => setActiveFilter(cat)}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid-2">
              {filteredProjects.map((project) => (
                <article key={project.id} className="card work-card">
                  <div>
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: '12px',
                      }}
                    >
                      <span className="tag">{project.category}</span>
                      <span style={{ color: 'var(--accent-2)', fontWeight: 600, fontSize: '0.86rem' }}>
                        {project.metric}
                      </span>
                    </div>
                    <h3>{project.title}</h3>
                    <p style={{ marginTop: '8px' }}>{project.summary}</p>
                    <div className="work-tag-row">
                      {project.stack.map((tech) => (
                        <span key={tech} className="tag">{tech}</span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => setSelectedProject(project)}
                    >
                      View Case Study <ExternalLink size={14} />
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Client Testimonials & Live Stats */}
        <Testimonials />

        {/* Pricing */}
        <section id="pricing" className="section">
          <div className="container">
            <div className="section-header">
              <div>
                <div className="section-eyebrow">Transparent Pricing</div>
                <h2 className="section-title">Pick the pace that fits your launch</h2>
              </div>
            </div>

            <div className="grid-3">
              {PLANS.map((plan) => (
                <article
                  key={plan.name}
                  className={`card price-card ${plan.featured ? 'featured' : ''}`}
                >
                  <h3>{plan.name}</h3>
                  <p style={{ marginTop: '6px' }}>{plan.description}</p>
                  <div className="price-amount">{plan.price}</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.84rem' }}>
                    {plan.period}
                  </div>
                  <ul className="feature-list">
                    {plan.features.map((feat) => (
                      <li key={feat}>
                        <Check size={16} color="var(--success)" />
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                  <a
                    href="#contact"
                    className={`btn ${plan.featured ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ width: '100%' }}
                  >
                    Choose {plan.name}
                  </a>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="section">
          <div className="container">
            <div className="section-header">
              <div>
                <div className="section-eyebrow">FAQ</div>
                <h2 className="section-title">Common questions</h2>
              </div>
            </div>

            <div className="faq-list">
              {FAQS.map((item, idx) => {
                const isOpen = openFaq === idx;
                return (
                  <div key={item.q} className="faq-item">
                    <button
                      type="button"
                      className="faq-trigger"
                      aria-expanded={isOpen}
                      onClick={() => setOpenFaq(isOpen ? -1 : idx)}
                    >
                      <span>{item.q}</span>
                      <ChevronDown
                        size={18}
                        style={{
                          transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                          transition: 'transform 0.2s ease',
                        }}
                      />
                    </button>
                    {isOpen && <div className="faq-answer">{item.a}</div>}
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Contact */}
        <section id="contact" className="section">
          <div className="container contact-grid">
            <div>
              <div className="section-eyebrow">Let&apos;s Build</div>
              <h2 className="section-title" style={{ marginBottom: '14px' }}>
                Ready to launch your next project?
              </h2>
              <p className="section-desc" style={{ marginBottom: '22px' }}>
                Share your goals and preferred timeline. Your project is synced with GitHub
                and ready for instant Vercel delivery.
              </p>
              <div className="card">
                <div style={{ fontWeight: 600, marginBottom: '6px' }}>24/7 Cloud Automation Ready</div>
                <p>
                  Every update committed to <code>vvvbbb</code> triggers clean builds and live
                  progress alerts straight to Telegram.
                </p>
              </div>
            </div>

            <form className="card" onSubmit={handleFormSubmit}>
              {submitted && (
                <div className="alert-success" role="status">
                  Thanks! Your inquiry was received — we&apos;ll reach out shortly.
                </div>
              )}

              <div className="form-group">
                <label htmlFor="name">Your Name</label>
                <input
                  id="name"
                  type="text"
                  className="input"
                  placeholder="Vrajesh"
                  value={formState.name}
                  onChange={(e) => setFormState({ ...formState, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  id="email"
                  type="email"
                  className="input"
                  placeholder="you@example.com"
                  value={formState.email}
                  onChange={(e) => setFormState({ ...formState, email: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="service">Project Type</label>
                <select
                  id="service"
                  className="input"
                  value={formState.service}
                  onChange={(e) => setFormState({ ...formState, service: e.target.value })}
                >
                  <option value="Web Applications">Web Applications</option>
                  <option value="Mobile & Cross-Platform">Mobile &amp; Cross-Platform</option>
                  <option value="AI & Cloud Automation">AI &amp; Cloud Automation</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="message">Project Details</label>
                <textarea
                  id="message"
                  rows="4"
                  className="input"
                  placeholder="Tell us about your website or app idea..."
                  value={formState.message}
                  onChange={(e) => setFormState({ ...formState, message: e.target.value })}
                />
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
                Send Inquiry <Send size={16} />
              </button>
            </form>
          </div>
        </section>
      </main>

      {selectedProject && (
        <div
          className="modal-backdrop"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
          onClick={() => setSelectedProject(null)}
        >
          <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '14px',
              }}
            >
              <span className="tag">{selectedProject.category}</span>
              <button
                type="button"
                className="icon-btn"
                onClick={() => setSelectedProject(null)}
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>
            <h3 id="modal-title" style={{ fontSize: '1.5rem', marginBottom: '10px' }}>
              {selectedProject.title}
            </h3>
            <p style={{ color: 'var(--text-muted)', marginBottom: '18px' }}>
              {selectedProject.summary}
            </p>
            <ul className="feature-list">
              {selectedProject.highlights.map((h) => (
                <li key={h}>
                  <Check size={16} color="var(--success)" />
                  <span>{h}</span>
                </li>
              ))}
            </ul>
            <div className="work-tag-row">
              {selectedProject.stack.map((tech) => (
                <span key={tech} className="tag">{tech}</span>
              ))}
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <div className="container footer-inner">
          <span>© {new Date().getFullYear()} 98.5 Studio (vvvbbb). Built for Vercel.</span>
          <span>Powered by Vite + React &amp; 24/7 Cloud Runner</span>
        </div>
      </footer>
    </>
  );
}
