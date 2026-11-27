import React, { useEffect, useState } from 'react';
import { ArrowRight, Bot, Code2, Menu, Moon, Rocket, Sparkles, Sun, X } from 'lucide-react';
import { PROJECTS } from './data/siteData';
import QuoteEstimator from './components/QuoteEstimator';

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <>
      <div className="ambient-bg" aria-hidden="true" />
      <header className="navbar">
        <div className="container navbar-inner">
          <a href="#top" className="brand">
            <span className="brand-mark"><Sparkles size={18} /></span>
            <span>98.5 Studio</span>
          </a>
          <div className="nav-actions">
            <button type="button" className="icon-btn" onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}>
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>
      <main className="container">
        <section className="hero">
          <h1>Build faster. Ship smarter.</h1>
          <QuoteEstimator />
        </section>
      </main>
    </>
  );
}