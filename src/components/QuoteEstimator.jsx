import React, { useState, useMemo } from 'react';
import { Calculator } from 'lucide-react';

export default function QuoteEstimator() {
  const [type, setType] = useState('web');
  const [pages, setPages] = useState(5);
  const [timeline, setTimeline] = useState(2);

  const estimate = useMemo(() => {
    const base = type === 'web' ? 500 : type === 'mobile' ? 1200 : 1500;
    const pageCost = pages * 50;
    const timelineMultiplier = timeline < 2 ? 1.5 : 1;
    return Math.round((base + pageCost) * timelineMultiplier);
  }, [type, pages, timeline]);

  return (
    <div className="quote-estimator" style={{ background: 'var(--bg-card)', padding: '24px', borderRadius: '22px', border: '1px solid var(--border)', marginTop: '40px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <Calculator size={20} /> Instant Budget Estimator
      </h3>
      <div style={{ display: 'grid', gap: '16px' }}>
        <label>Project Type: 
          <select value={type} onChange={(e) => setType(e.target.value)} style={{ width: '100%', padding: '8px', marginTop: '5px', background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: '8px' }}>
            <option value="web">Web Application</option>
            <option value="mobile">Mobile App</option>
            <option value="ai">AI Automation</option>
          </select>
        </label>
        <label>Pages/Features Count: {pages}
          <input type="range" min="1" max="20" value={pages} onChange={(e) => setPages(Number(e.target.value))} style={{ width: '100%' }} />
        </label>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent)', marginTop: '10px' }}>
          Estimated: ${estimate}
        </div>
      </div>
    </div>
  );
}