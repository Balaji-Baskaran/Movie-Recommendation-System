# CineMatch – Movie Recommendation System

An AI-powered Movie Recommendation System migrated to a modern **React (Vite) frontend** and **Django REST backend**.

---

## 🌟 Tech Stack

- **Frontend**: React 19, Vite, Lucide Icons, Plotly.js, Vanilla CSS Design System with Dark/Light Mode.
- **Backend**: Django 5.2, Django CORS Headers, ASGI/WSGI.
- **Machine Learning**: Scikit-learn, Cosine Similarity, TF-IDF / Semantic Embeddings, Pandas, NumPy, Joblib.

---

## 📁 Project Structure

```text
├── backend/                  # Django project root
│   ├── cinematch/            # Django project settings & URL configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── movies/               # Django API app
│   │   ├── services.py       # Recommendation model loader & cache
│   │   ├── views.py          # API endpoints (health, search, filter, options)
│   │   ├── urls.py           # API routes
│   │   ├── tests.py          # Automated Django test suite
│   │   ├── recommender.py    # Cosine similarity recommendation algorithm
│   │   ├── data_utils.py     # Model loading and embeddings normalizer
│   │   └── chart_heartbeat.py # Plotly heartbeat chart visualizer
│   ├── model/                # Serialized recommendation models (.pkl)
│   ├── dataset/              # Indian movies dataset
│   └── manage.py
├── frontend/                 # Modern React single-page application (Vite)
│   ├── src/
│   │   ├── api/client.js     # API communication with Django
│   │   ├── components/       # Modular UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── TabBar.jsx
│   │   │   ├── MovieSearch.jsx
│   │   │   ├── SelectedMovieCard.jsx
│   │   │   ├── HeartbeatChart.jsx
│   │   │   ├── MovieCard.jsx
│   │   │   ├── MovieDetailsModal.jsx
│   │   │   ├── FilterSection.jsx
│   │   │   ├── LoadingSkeleton.jsx
│   │   │   └── EmptyState.jsx
│   │   ├── App.jsx           # Main application state & theme orchestrator
│   │   └── index.css         # Complete responsive design system
│   ├── dist/                 # Production React build (served by Django)
│   └── vite.config.js        # Vite config with backend proxy
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Django Backend

```bash
cd backend
python manage.py runserver 8000
```

The Django API is accessible at `http://127.0.0.1:8000/api/health`.

### 3. Run the React Frontend (Development Mode)

In a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173/` (or port assigned by Vite).

---

## ⚡ Direct Production Serving via Django

Django can serve the built React app directly:

```bash
cd frontend
npm run build
cd ../backend
python manage.py runserver 8000
```

Open `http://localhost:8000/` to use the full React interface directly from Django.

---

## 🧪 Testing

Run backend tests:

```bash
cd backend
python manage.py test
```

Build and test frontend:

```bash
cd frontend
npm run build
```
