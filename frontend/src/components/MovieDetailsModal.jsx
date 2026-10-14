import React, { useEffect } from 'react';
import { X, Star, Flame, Film, Sparkles, ArrowRight } from 'lucide-react';

export default function MovieDetailsModal({ movie, onClose, onFindSimilar }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!movie) return null;

  const poster = movie.poster_path || '';
  const originalPoster = poster.startsWith('http')
    ? poster.replace('/w500/', '/original/')
    : null;

  const genres = Array.isArray(movie.genre_list) ? movie.genre_list.filter(Boolean) : [];
  const indCls = `i-${movie.industry}`;
  const simPct = (movie.score || 0) * 100;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} aria-label="Close modal">
          <X size={18} />
        </button>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', gap: '1.5rem', padding: '2rem 2rem 1.25rem' }}>
            {originalPoster ? (
              <div
                style={{
                  minWidth: '130px',
                  maxWidth: '130px',
                  height: '195px',
                  borderRadius: '14px',
                  overflow: 'hidden',
                  boxShadow: '0 12px 30px rgba(0,0,0,0.5)',
                  flexShrink: 0,
                }}
              >
                <img
                  src={originalPoster}
                  alt={movie.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>
            ) : (
              <div
                style={{
                  minWidth: '130px',
                  maxWidth: '130px',
                  height: '195px',
                  borderRadius: '14px',
                  background: 'linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.15))',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'rgba(165,180,252,0.5)',
                  flexShrink: 0,
                }}
              >
                <Film size={48} />
              </div>
            )}

            <div style={{ flex: 1 }}>
              <h3 style={{ fontSize: '1.45rem', fontWeight: 800, marginBottom: '0.45rem', lineHeight: 1.25 }}>
                {movie.title}
              </h3>

              <div className="tag-row" style={{ marginBottom: '0.65rem' }}>
                <span className={`ind-tag ${indCls}`}>{movie.industry}</span>
                {movie.year > 0 && <span className="year-tag">{movie.year}</span>}
                {genres.map((g, i) => (
                  <span key={i} className="genre-tag">
                    {g.charAt(0).toUpperCase() + g.slice(1)}
                  </span>
                ))}
              </div>

              <div className="star-row" style={{ marginBottom: '0.65rem' }}>
                <Star size={15} fill="#fbbf24" color="#fbbf24" />
                <span className="star-val">
                  {movie.rating ? Number(movie.rating).toFixed(1) : '0.0'} / 10
                </span>
                <span style={{ color: 'var(--text-faint)', margin: '0 4px' }}>·</span>
                <span className="popularity-val">
                  <Flame size={14} color="#fb923c" />
                  {movie.popularity ? Number(movie.popularity).toFixed(1) : '0.0'} popularity
                </span>
              </div>

              {simPct > 0 && (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.82rem', color: 'var(--accent)', fontWeight: 700 }}>
                  <Sparkles size={14} />
                  <span>Semantic Match: {simPct.toFixed(1)}%</span>
                </div>
              )}
            </div>
          </div>

          <div style={{ padding: '0 2rem 1.75rem' }}>
            <h5 style={{ fontSize: '0.82rem', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.8px', marginBottom: '0.5rem' }}>
              Synopsis
            </h5>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.65, maxHeight: '200px', overflowY: 'auto' }}>
              {movie.overview || 'No plot summary available for this title.'}
            </p>

            <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                type="button"
                className="btn-primary"
                onClick={() => {
                  onClose();
                  onFindSimilar(movie);
                }}
              >
                <Sparkles size={16} />
                <span>Find Similar to This Movie</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
