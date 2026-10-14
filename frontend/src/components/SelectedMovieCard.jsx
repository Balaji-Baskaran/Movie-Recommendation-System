import React from 'react';
import { Film, Star, Flame } from 'lucide-react';

export default function SelectedMovieCard({ movie }) {
  if (!movie) return null;

  const poster = movie.poster_path || '';
  const originalPoster = poster.startsWith('http')
    ? poster.replace('/w500/', '/original/')
    : null;

  const genres = Array.isArray(movie.genre_list) ? movie.genre_list.filter(Boolean) : [];
  const indCls = `i-${movie.industry}`;

  return (
    <div className="sel-card">
      {originalPoster ? (
        <div className="sel-poster">
          <img
            src={originalPoster}
            alt={movie.title}
            loading="eager"
            onError={(e) => {
              // fallback if original poster is unavailable
              e.currentTarget.onerror = null;
              e.currentTarget.src = poster;
            }}
          />
        </div>
      ) : (
        <div className="sel-no-poster">
          <Film size={54} strokeWidth={1.5} />
        </div>
      )}

      <div className="sel-info">
        <h2 className="sel-title">{movie.title}</h2>

        <div className="tag-row">
          <span className={`ind-tag ${indCls}`}>{movie.industry}</span>
          {movie.year > 0 && <span className="year-tag">{movie.year}</span>}
          {genres.map((g, idx) => (
            <span key={idx} className="genre-tag">
              {g.charAt(0).toUpperCase() + g.slice(1)}
            </span>
          ))}
        </div>

        <div className="star-row">
          <Star size={16} fill="#fbbf24" color="#fbbf24" />
          <span className="star-val">
            {movie.rating ? Number(movie.rating).toFixed(1) : '0.0'} / 10
          </span>
          <span style={{ color: 'var(--text-faint)', margin: '0 4px' }}>·</span>
          <span className="popularity-val">
            <Flame size={15} color="#fb923c" />
            {movie.popularity ? Number(movie.popularity).toFixed(1) : '0.0'} popularity
          </span>
        </div>

        <p className="sel-overview">
          {movie.overview || 'No overview available for this title.'}
        </p>
      </div>
    </div>
  );
}
