import React from 'react';
import { Search, Filter } from 'lucide-react';

export default function TabBar({ activeTab, onSelectTab }) {
  return (
    <div className="tab-bar" role="tablist">
      <button
        id="tab-btn-search"
        role="tab"
        aria-selected={activeTab === 'search'}
        className={`tab-btn ${activeTab === 'search' ? 'active' : ''}`}
        onClick={() => onSelectTab('search')}
      >
        <Search size={16} strokeWidth={2.2} />
        <span>Find Similar Movies</span>
      </button>

      <button
        id="tab-btn-filter"
        role="tab"
        aria-selected={activeTab === 'filter'}
        className={`tab-btn ${activeTab === 'filter' ? 'active' : ''}`}
        onClick={() => onSelectTab('filter')}
      >
        <Filter size={16} strokeWidth={2.2} />
        <span>Recommend by Genre &amp; Year</span>
      </button>
    </div>
  );
}
