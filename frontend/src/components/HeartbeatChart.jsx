import React, { useEffect, useRef } from 'react';
import { Activity } from 'lucide-react';

export default function HeartbeatChart({ chartJson, theme }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartJson || !chartRef.current || !window.Plotly) return;

    try {
      const parsed = typeof chartJson === 'string' ? JSON.parse(chartJson) : chartJson;
      const data = parsed.data || [];
      const layout = { ...parsed.layout };

      // Synchronize Plotly theme styles with the current React theme
      const isLight = theme === 'light';
      layout.paper_bgcolor = isLight ? 'rgba(248, 250, 252, 0.98)' : 'rgba(6, 9, 26, 0.95)';
      layout.plot_bgcolor = isLight ? 'rgba(240, 244, 255, 0.6)' : 'rgba(10, 14, 38, 0.6)';
      
      if (layout.font) {
        layout.font.color = isLight ? '#1e293b' : '#f1f5f9';
      }

      window.Plotly.newPlot(chartRef.current, data, layout, {
        responsive: true,
        displayModeBar: false,
      });

      const handleResize = () => {
        if (chartRef.current && window.Plotly) {
          window.Plotly.Plots.resize(chartRef.current);
        }
      };
      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        if (chartRef.current && window.Plotly) {
          window.Plotly.purge(chartRef.current);
        }
      };
    } catch (err) {
      console.error('Error rendering Plotly heartbeat chart:', err);
    }
  }, [chartJson, theme]);

  if (!chartJson) return null;

  return (
    <div style={{ marginTop: '1rem', marginBottom: '2.5rem' }}>
      <div className="section-label">
        <span className="accent-bar"></span>
        <Activity size={18} color="#818cf8" />
        <span>Similarity Rhythm Visualization</span>
      </div>

      <div className="chart-container">
        <div ref={chartRef} style={{ width: '100%', minHeight: '440px' }} />
      </div>
    </div>
  );
}
