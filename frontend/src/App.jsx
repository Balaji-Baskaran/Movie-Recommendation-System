import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import TabBar from './components/TabBar';
import MovieSearch from './components/MovieSearch';
import SelectedMovieCard from './components/SelectedMovieCard';
import HeartbeatChart from './components/HeartbeatChart';
import MovieCard from './components/MovieCard';
import MovieDetailsModal from './components/MovieDetailsModal';
import FilterSection from './components/FilterSection';
import LoadingSkeleton from './components/LoadingSkeleton';
import EmptyState from './components/EmptyState';
import { Sparkles, Film } from 'lucide-react';
import {
  checkHealth,
  fetchMovies,
  fetchFilterOptions,
  searchRecommendations,
  filterMovies,
} from './api/client';

const THEME_KEY = 'movie-recommender-theme';

export default function App() {
  // Theme state
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || 'dark');

  // Backend metadata
  const [isHealthy, setIsHealthy] = useState(false);
  const [totalMoviesCount, setTotalMoviesCount] = useState(0);

  // Movie dropdown and filter options
  const [moviesList, setMoviesList] = useState([]);
  const [filterOptions, setFilterOptions] = useState({ genres: [], years: [], industries: [] });

  // Navigation tab
  const [activeTab, setActiveTab] = useState('search');

  // Search tab state
  const [selectedMovieIdx, setSelectedMovieIdx] = useState(0);
  const [topN, setTopN] = useState(10);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchData, setSearchData] = useState(null);
  const [searchError, setSearchError] = useState(null);

  // Filter tab state
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedYears, setSelectedYears] = useState([]);
  const [selectedIndustries, setSelectedIndustries] = useState([]);
  const [filterLoading, setFilterLoading] = useState(false);
  const [filteredMovies, setFilteredMovies] = useState(null);
  const [filterError, setFilterError] = useState(null);

  // Modal dialog state
  const [modalMovie, setModalMovie] = useState(null);

  // Apply theme class to <body>
  useEffect(() => {
    if (theme === 'light') {
      document.body.classList.add('light');
    } else {
      document.body.classList.remove('light');
    }
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Initial data loading
  useEffect(() => {
    async function init() {
      try {
        const health = await checkHealth();
        setIsHealthy(health.status === 'healthy');
        setTotalMoviesCount(health.movies_loaded || 0);
      } catch (e) {
        console.warn('API health check pending:', e);
      }

      try {
        const [movies, opts] = await Promise.all([fetchMovies(), fetchFilterOptions()]);
        setMoviesList(movies || []);
        setFilterOptions(opts || { genres: [], years: [], industries: [] });

        // Trigger initial search for the first movie
        if (movies && movies.length > 0) {
          executeSearch(movies[0].idx, 10);
        }
      } catch (err) {
        console.error('Failed to load initial data:', err);
      }
    }
    init();
  }, []);

  // Perform semantic recommendation search
  const executeSearch = async (idx, n = topN) => {
    if (idx === null || idx === undefined) return;
    setSearchLoading(true);
    setSearchError(null);
    try {
      const data = await searchRecommendations(idx, n);
      setSearchData(data);
    } catch (err) {
      setSearchError(err.message || 'Error occurred while computing similarity.');
    } finally {
      setSearchLoading(false);
    }
  };

  // Perform multi-attribute database filter
  const executeFilter = async () => {
    setFilterLoading(true);
    setFilterError(null);
    try {
      const data = await filterMovies({
        genres: selectedGenres,
        years: selectedYears,
        industries: selectedIndustries,
      });
      if (data.movies && data.movies.length > 0) {
        setFilteredMovies(data.movies);
      } else {
        setFilteredMovies([]);
        setFilterError(data.error || 'No movies found matching these criteria.');
      }
    } catch (err) {
      setFilterError(err.message || 'Error occurred while filtering movies.');
    } finally {
      setFilterLoading(false);
    }
  };

  // Find similar to a movie clicked from recommendations or modal
  const handleFindSimilar = (movie) => {
    if (!movie) return;
    // Look up movie index in moviesList by title matching or use movie_idx
    let targetIdx = movie.idx !== undefined ? movie.idx : null;
    if (targetIdx === null && movie.title) {
      const cleanTitle = movie.title.toLowerCase();
      const match = moviesList.find((m) => m.label.toLowerCase().includes(cleanTitle));
      if (match) targetIdx = match.idx;
    }

    if (targetIdx !== null) {
      setSelectedMovieIdx(targetIdx);
      setActiveTab('search');
      executeSearch(targetIdx, topN);
      window.scrollTo({ top: 400, behavior: 'smooth' });
    }
  };

  const handleClearFilters = () => {
    setSelectedGenres([]);
    setSelectedYears([]);
    setSelectedIndustries([]);
    setFilteredMovies(null);
    setFilterError(null);
  };

  return (
    <>
      <Navbar
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <main className="main-content">
        <Hero />

        <TabBar activeTab={activeTab} onSelectTab={setActiveTab} />

        {/* TAB 1: SEMANTIC SIMILARITY SEARCH */}
        {activeTab === 'search' && (
          <section id="panel-search" aria-label="Similar Movies Search">
            <MovieSearch
              movies={moviesList}
              selectedMovieIdx={selectedMovieIdx}
              onSelectMovie={(idx) => {
                setSelectedMovieIdx(idx);
                executeSearch(idx, topN);
              }}
              onSearch={() => executeSearch(selectedMovieIdx, topN)}
              isLoading={searchLoading}
              topN={topN}
              onChangeTopN={(n) => {
                setTopN(n);
                if (selectedMovieIdx !== null) {
                  executeSearch(selectedMovieIdx, n);
                }
              }}
            />

            {searchLoading && <LoadingSkeleton count={topN} />}

            {searchError && !searchLoading && (
              <EmptyState
                type="error"
                title="Search Error"
                description={searchError}
                onAction={() => executeSearch(selectedMovieIdx, topN)}
                actionLabel="Retry Search"
              />
            )}

            {!searchLoading && searchData && (
              <>
                <SelectedMovieCard movie={searchData.selected} />

                {searchData.chart_json && (
                  <HeartbeatChart chartJson={searchData.chart_json} theme={theme} />
                )}

                <div className="section-label">
                  <span className="accent-bar"></span>
                  <Sparkles size={18} color="#818cf8" />
                  <span>Top Recommended Movies</span>
                </div>

                <div className="cards-grid">
                  {(searchData.recommendations || []).map((movie, idx) => (
                    <MovieCard
                      key={movie.idx || idx}
                      movie={movie}
                      onSelect={(m) => setModalMovie(m)}
                      onFindSimilar={handleFindSimilar}
                    />
                  ))}
                </div>
              </>
            )}
          </section>
        )}

        {/* TAB 2: MULTI-FACTOR DATABASE FILTER */}
        {activeTab === 'filter' && (
          <section id="panel-filter" aria-label="Genre and Year Filter">
            <div className="section-label" style={{ maxWidth: '760px', margin: '0 auto 1rem' }}>
              <span className="accent-bar"></span>
              <Film size={18} color="#818cf8" />
              <span>Multi-Factor Database Filter</span>
            </div>

            <FilterSection
              filterOptions={filterOptions}
              selectedGenres={selectedGenres}
              onChangeGenres={setSelectedGenres}
              selectedYears={selectedYears}
              onChangeYears={setSelectedYears}
              selectedIndustries={selectedIndustries}
              onChangeIndustries={setSelectedIndustries}
              onApplyFilter={executeFilter}
              isLoading={filterLoading}
              onClearAll={handleClearFilters}
            />

            {filterLoading && <LoadingSkeleton count={8} />}

            {filterError && !filterLoading && (
              <EmptyState
                type="warning"
                title="No Movies Found"
                description={filterError}
                onAction={handleClearFilters}
                actionLabel="Reset Filters"
              />
            )}

            {!filterLoading && filteredMovies && filteredMovies.length > 0 && (
              <>
                <div className="section-label">
                  <span className="accent-bar"></span>
                  <Film size={18} color="#818cf8" />
                  <span>Top {filteredMovies.length} Matching Movies</span>
                </div>

                <div className="cards-grid">
                  {filteredMovies.map((movie, idx) => (
                    <MovieCard
                      key={movie.title + idx}
                      movie={movie}
                      onSelect={(m) => setModalMovie(m)}
                      onFindSimilar={handleFindSimilar}
                    />
                  ))}
                </div>
              </>
            )}
          </section>
        )}
      </main>

      {/* Movie Details Modal */}
      {modalMovie && (
        <MovieDetailsModal
          movie={modalMovie}
          onClose={() => setModalMovie(null)}
          onFindSimilar={handleFindSimilar}
        />
      )}
    </>
  );
}
