import React from 'react';
import { Star, Quote, Award, TrendingUp, ShieldCheck, Zap } from 'lucide-react';
import { LIVE_STATS, TESTIMONIALS } from '../data/siteData';

const STAT_ICONS = [ShieldCheck, TrendingUp, Award, Zap];

export default function Testimonials() {
  return (
    <section id="testimonials" className="section" style={{ position: 'relative' }}>
      <div className="container">
        {/* Live Stats Counter Strip */}
        <div
          className="card"
          style={{
            marginBottom: '64px',
            background: 'var(--card-bg)',
            border: '1px solid var(--border)',
            padding: '36px 28px',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '24px',
          }}
        >
          {LIVE_STATS.map((stat, idx) => {
            const Icon = STAT_ICONS[idx % STAT_ICONS.length];
            return (
              <div key={stat.label} style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                <div
                  style={{
                    width: '42px',
                    height: '42px',
                    borderRadius: '10px',
                    background: 'var(--accent-glow)',
                    color: 'var(--accent)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  <Icon size={20} />
                </div>
                <div>
                  <div
                    style={{
                      fontFamily: 'var(--font-heading)',
                      fontSize: '1.8rem',
                      fontWeight: 800,
                      color: 'var(--text-main)',
                      lineHeight: 1.1,
                    }}
                  >
                    {stat.value}
                  </div>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)', marginTop: '4px' }}>
                    {stat.label}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {stat.description}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Section Header */}
        <div className="section-header">
          <div>
            <div className="section-eyebrow">Client Feedback</div>
            <h2 className="section-title">Verified words from founders &amp; leaders</h2>
          </div>
        </div>

        {/* Testimonials Cards Grid */}
        <div className="grid-3">
          {TESTIMONIALS.map((t) => (
            <article
              key={t.id}
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '28px',
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '16px' }}>
                  {[...Array(t.rating)].map((_, i) => (
                    <Star key={i} size={16} fill="#f59e0b" color="#f59e0b" />
                  ))}
                </div>
                <p
                  style={{
                    fontSize: '0.96rem',
                    lineHeight: '1.6',
                    color: 'var(--text-main)',
                    fontStyle: 'italic',
                    marginBottom: '20px',
                  }}
                >
                  "{t.quote}"
                </p>
              </div>

              <div
                style={{
                  borderTop: '1px solid var(--border)',
                  paddingTop: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                }}
              >
                <div
                  style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: '50%',
                    background: 'var(--accent)',
                    color: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: '0.9rem',
                    flexShrink: 0,
                  }}
                >
                  {t.author.charAt(0)}
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                    {t.author}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    {t.role}, {t.company}
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
