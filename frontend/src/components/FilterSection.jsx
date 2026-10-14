import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check, X, Filter, Zap } from 'lucide-react';

function MultiSelectDropdown({ id, label, placeholder, options = [], selected = [], onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleOption = (opt) => {
    if (selected.includes(opt)) {
      onChange(selected.filter((item) => item !== opt));
    } else {
      onChange([...selected, opt]);
    }
  };

  const getTriggerText = () => {
    if (selected.length === 0) return placeholder;
    if (selected.length <= 2) return selected.join(', ');
    return `${selected.length} selected`;
  };

  return (
    <div className="form-group" ref={containerRef}>
      <label className="form-label" htmlFor={id}>
        {label}
      </label>
      <button
        id={id}
        type="button"
        className="multi-select-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span style={{ color: selected.length === 0 ? 'var(--text-muted)' : 'var(--text-primary)' }}>
          {getTriggerText()}
        </span>
        <ChevronDown
          size={16}
          style={{
            transform: isOpen ? 'rotate(180deg)' : 'none',
            transition: 'transform 0.2s ease',
            color: 'var(--text-muted)',
          }}
        />
      </button>

      {isOpen && (
        <div className="multi-select-dropdown">
          {options.length === 0 ? (
            <div style={{ padding: '0.6rem', color: 'var(--text-muted)', fontSize: '0.84rem' }}>
              No options available
            </div>
          ) : (
            options.map((opt) => {
              const isSelected = selected.includes(opt);
              return (
                <div
                  key={opt}
                  className={`multi-select-option ${isSelected ? 'selected' : ''}`}
                  onClick={() => toggleOption(opt)}
                >
                  <div className="option-checkbox">
                    {isSelected && <Check size={12} strokeWidth={3} />}
                  </div>
                  <span>{opt}</span>
                </div>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}

export default function FilterSection({
  filterOptions = { genres: [], years: [], industries: [] },
  selectedGenres,
  onChangeGenres,
  selectedYears,
  onChangeYears,
  selectedIndustries,
  onChangeIndustries,
  onApplyFilter,
  isLoading,
  onClearAll,
}) {
  const hasActiveFilters =
    selectedGenres.length > 0 || selectedYears.length > 0 || selectedIndustries.length > 0;

  const handleSubmit = (e) => {
    e.preventDefault();
    onApplyFilter();
  };

  return (
    <div>
      <form className="filter-form" onSubmit={handleSubmit}>
        <MultiSelectDropdown
          id="genre-select"
          label="Genre(s)"
          placeholder="Choose genres…"
          options={filterOptions.genres || []}
          selected={selectedGenres}
          onChange={onChangeGenres}
        />

        <MultiSelectDropdown
          id="year-select"
          label="Year(s)"
          placeholder="Choose release years…"
          options={(filterOptions.years || []).map(String)}
          selected={selectedYears.map(String)}
          onChange={(newYears) => onChangeYears(newYears.map(Number))}
        />

        <MultiSelectDropdown
          id="industry-select"
          label="Language / Industry"
          placeholder="Choose industries…"
          options={filterOptions.industries || []}
          selected={selectedIndustries}
          onChange={onChangeIndustries}
        />

        <button type="submit" className="btn-primary" disabled={isLoading} id="filterBtn">
          <Zap size={16} />
          <span>{isLoading ? 'Filtering…' : 'Find Movies'}</span>
        </button>
      </form>

      {hasActiveFilters && (
        <div className="filter-active-chips">
          {selectedGenres.map((g) => (
            <span key={`genre-${g}`} className="filter-chip">
              <span>Genre: {g}</span>
              <span
                className="filter-chip-remove"
                onClick={() => onChangeGenres(selectedGenres.filter((item) => item !== g))}
                role="button"
                tabIndex={0}
              >
                <X size={13} />
              </span>
            </span>
          ))}

          {selectedYears.map((y) => (
            <span key={`year-${y}`} className="filter-chip">
              <span>Year: {y}</span>
              <span
                className="filter-chip-remove"
                onClick={() => onChangeYears(selectedYears.filter((item) => item !== y))}
                role="button"
                tabIndex={0}
              >
                <X size={13} />
              </span>
            </span>
          ))}

          {selectedIndustries.map((ind) => (
            <span key={`ind-${ind}`} className="filter-chip">
              <span>Industry: {ind}</span>
              <span
                className="filter-chip-remove"
                onClick={() => onChangeIndustries(selectedIndustries.filter((item) => item !== ind))}
                role="button"
                tabIndex={0}
              >
                <X size={13} />
              </span>
            </span>
          ))}

          <button type="button" className="filter-clear-all" onClick={onClearAll}>
            Clear All
          </button>
        </div>
      )}
    </div>
  );
}
