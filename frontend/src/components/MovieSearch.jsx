import React, { useState, useEffect, useRef, useMemo } from 'react';
import { Search, X, Sparkles } from 'lucide-react';

export default function MovieSearch({
  movies = [],
  selectedMovieIdx,
  onSelectMovie,
  onSearch,
  isLoading,
  topN,
  onChangeTopN,
}) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const wrapperRef = useRef(null);
  const listRef = useRef(null);

  // Set initial query text if a movie is selected
  useEffect(() => {
    if (selectedMovieIdx !== null && selectedMovieIdx !== undefined && movies.length > 0) {
      const match = movies.find((m) => m.idx === selectedMovieIdx);
      if (match) {
        setQuery(match.label);
      }
    }
  }, [selectedMovieIdx, movies]);

  // Filter movies with fast substring matching (capped at 40 for max speed)
  const filteredMovies = useMemo(() => {
    if (!query || query.trim().length === 0) {
      return movies.slice(0, 30);
    }
    const cleanQuery = query.toLowerCase().trim();
    const results = [];
    for (let i = 0; i < movies.length; i++) {
      if (movies[i].label.toLowerCase().includes(cleanQuery)) {
        results.push(movies[i]);
        if (results.length >= 40) break;
      }
    }
    return results;
  }, [query, movies]);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (movie) => {
    setQuery(movie.label);
    onSelectMovie(movie.idx);
    setIsOpen(false);
    setActiveIndex(-1);
  };

  const handleClear = () => {
    setQuery('');
    setIsOpen(true);
    setActiveIndex(-1);
  };

  const handleKeyDown = (e) => {
    if (!isOpen) {
      if (e.key === 'ArrowDown' || e.key === 'Enter') {
        setIsOpen(true);
      }
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((prev) => (prev < filteredMovies.length - 1 ? prev + 1 : prev));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex >= 0 && activeIndex < filteredMovies.length) {
        handleSelect(filteredMovies[activeIndex]);
      } else if (filteredMovies.length > 0) {
        handleSelect(filteredMovies[0]);
      } else {
        onSearch();
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  return (
    <div className="search-wrapper" ref={wrapperRef}>
      <div className="search-row">
        <div className="search-input-box">
          <Search className="search-input-icon" size={18} />
          <input
            type="text"
            className="search-input"
            placeholder="Search a movie title…"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setIsOpen(true);
              setActiveIndex(-1);
            }}
            onFocus={() => setIsOpen(true)}
            onKeyDown={handleKeyDown}
          />
          {query && (
            <button
              type="button"
              className="search-clear-btn"
              onClick={handleClear}
              aria-label="Clear search"
            >
              <X size={16} />
            </button>
          )}

          {isOpen && (
            <div className="search-dropdown" ref={listRef}>
              {filteredMovies.length === 0 ? (
                <div style={{ padding: '0.9rem 1rem', color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                  No movies found matching "{query}".
                </div>
              ) : (
                filteredMovies.map((movie, idx) => (
                  <div
                    key={movie.idx}
                    className={`search-dropdown-item ${idx === activeIndex ? 'active' : ''}`}
                    onClick={() => handleSelect(movie)}
                    onMouseEnter={() => setActiveIndex(idx)}
                  >
                    <span>{movie.label}</span>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        <button
          className="btn-primary"
          id="searchBtn"
          onClick={() => onSearch()}
          disabled={isLoading || selectedMovieIdx === null || selectedMovieIdx === undefined}
        >
          <Sparkles size={16} />
          <span>{isLoading ? 'Computing…' : 'Search'}</span>
        </button>
      </div>

      <div className="search-controls" style={{ justifyContent: 'flex-end' }}>
        <div className="k-selector">
          <span className="k-selector-label">Show top:</span>
          <select
            className="k-selector-select"
            value={topN}
            onChange={(e) => onChangeTopN(Number(e.target.value))}
          >
            <option value={5}>5 Recommendations</option>
            <option value={10}>10 Recommendations</option>
            <option value={15}>15 Recommendations</option>
            <option value={20}>20 Recommendations</option>
          </select>
        </div>
      </div>
    </div>
  );
}
