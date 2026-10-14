const API_BASE = import.meta.env.VITE_API_URL || '';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchMovies() {
  const res = await fetch(`${API_BASE}/api/movies`);
  if (!res.ok) throw new Error(`Failed to load movies: ${res.statusText}`);
  return res.json();
}

export async function fetchFilterOptions() {
  const res = await fetch(`${API_BASE}/api/filter-options`);
  if (!res.ok) throw new Error(`Failed to load filter options: ${res.statusText}`);
  return res.json();
}

export async function searchRecommendations(movieIdx, n = 10) {
  const res = await fetch(`${API_BASE}/api/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ movie_idx: parseInt(movieIdx, 10), n: parseInt(n, 10) }),
  });
  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(data.error || `Search failed with status ${res.status}`);
  }
  return data;
}

export async function filterMovies({ genres = [], years = [], industries = [] }) {
  const res = await fetch(`${API_BASE}/api/filter`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ genres, years, industries }),
  });
  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(data.error || `Filter request failed with status ${res.status}`);
  }
  return data;
}
