import React from 'react';

export default function LoadingSkeleton({ count = 5 }) {
  return (
    <div className="cards-grid">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton-poster"></div>
          <div style={{ padding: '0.8rem 0' }}>
            <div className="skeleton-line" style={{ width: '75%' }}></div>
            <div className="skeleton-line" style={{ width: '45%' }}></div>
            <div className="skeleton-line" style={{ width: '60%' }}></div>
          </div>
        </div>
      ))}
    </div>
  );
}
