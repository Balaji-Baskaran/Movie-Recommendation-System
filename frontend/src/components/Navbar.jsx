import React from 'react';
import { Clapperboard, Moon, Sun } from 'lucide-react';

export default function Navbar({ theme, onToggleTheme }) {
  return (
    <nav className="navbar" aria-label="Main Navigation">
      <div className="nav-brand" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
        <div className="nav-logo">
          <Clapperboard size={22} strokeWidth={2.2} />
        </div>
        <div className="nav-title-group">
          <span className="nav-title">CineMatch</span>
        </div>
      </div>

      <div className="nav-actions">
        <button
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          <span className="theme-toggle-label">
            {theme === 'dark' ? 'Dark Mode' : 'Light Mode'}
          </span>
          <div className="toggle-track">
            <div className="toggle-thumb">
              {theme === 'dark' ? (
                <Moon size={11} strokeWidth={2.5} />
              ) : (
                <Sun size={11} strokeWidth={2.5} />
              )}
            </div>
          </div>
        </button>
      </div>
    </nav>
  );
}
