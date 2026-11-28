import React, { useEffect, useState } from 'react';
import { Sparkles, Moon, Sun, Zap } from 'lucide-react';
import QuoteEstimator from './components/QuoteEstimator';

export default function App() {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <>
      <div className="ambient-bg" aria-hidden="true" />
      <header className="navbar">
        <div className="container navbar-inner">
          <a href="#top" className="brand" aria-label="98.5 Studio Home">
            <span className="brand-mark"><Sparkles size={18} /></span>
            <span>98.5 Studio</span>
          </a>
          <div className="nav-actions">
            <button 
              type="button" 
              className="icon-btn" 
              onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>
      <main className="container">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-content">
            <div className="pill">
              <Zap size={14} />
              <span>Available for new projects</span>
            </div>
            <h1 id="hero-title">Build faster. <br /><span className="gradient-text">Ship smarter.</span></h1>
            <p className="hero-sub">
              High-performance web, mobile, and AI products delivered with autonomous CI/CD pipelines. 
              Get an instant project estimate below.
            </p>
            <QuoteEstimator />
          </div>
        </section>
      </main>
    </>
  );
}