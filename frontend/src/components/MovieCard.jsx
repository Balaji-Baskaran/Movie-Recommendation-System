import React from 'react';
import { Film, Star, Sparkles } from 'lucide-react';

export default function MovieCard({ movie, onSelect, onFindSimilar }) {
  const poster = movie.poster_path || '';
  const originalPoster = poster.startsWith('http')
    ? poster.replace('/w500/', '/original/')
    : null;

  const simPct = (movie.score || 0) * 100;
  const year = movie.year || '—';
  const rat = movie.rating ? Number(movie.rating).toFixed(1) : '—';
  const genres = Array.isArray(movie.genre_list) ? movie.genre_list.slice(0, 2).filter(Boolean) : [];
  const indCls = `i-${movie.industry}`;

  return (
    <div
      className="movie-card"
      onClick={() => onSelect && onSelect(movie)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter') onSelect && onSelect(movie);
      }}
    >
      <div className="card-poster-wrap">
        {originalPoster ? (
          <img
            src={originalPoster}
            alt={movie.title}
            loading="lazy"
            decoding="async"
            onError={(e) => {
              e.currentTarget.onerror = null;
              e.currentTarget.src = poster;
            }}
          />
        ) : (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'rgba(165, 180, 252, 0.4)',
            }}
          >
            <Film size={44} strokeWidth={1.5} />
          </div>
        )}

        <div className="card-poster-overlay"></div>

        {movie.rank && <div className="rank-badge">#{movie.rank}</div>}

        {simPct > 0 && (
          <div className="sim-badge">
            <Sparkles size={11} />
            <span>{simPct.toFixed(0)}%</span>
          </div>
        )}
      </div>

      <div className="card-body">
        <h4 className="card-title" title={movie.title}>
          {movie.title}
        </h4>

        <div className="card-meta">
          <span className={`ind-tag ${indCls}`}>{movie.industry}</span>
          <span className="year-tag">{year}</span>
        </div>

        <div className="card-rating">
          <Star size={13} fill="#fbbf24" color="#fbbf24" />
          <span className="card-rat-val">{rat}</span>
        </div>

        <div className="card-genres">
          {genres.map((g, idx) => (
            <span key={idx} className="genre-tag">
              {g.charAt(0).toUpperCase() + g.slice(1)}
            </span>
          ))}
        </div>

        {simPct > 0 && (
          <div className="sim-bar-wrap" title={`Similarity: ${simPct.toFixed(1)}%`}>
            <div className="sim-bar-fill" style={{ width: `${simPct.toFixed(1)}%` }}></div>
          </div>
        )}
      </div>
    </div>
  );
}
