# KaamDo — Hyperlocal Task Marketplace

A full-stack hyperlocal task marketplace where users post tasks, nearby workers bid, and AI powers classification, pricing, and matching.

![KaamDo](https://img.shields.io/badge/KaamDo-Hyperlocal_Marketplace-1a5c38?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Flask-blue?style=flat-square)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat-square)
![AI](https://img.shields.io/badge/AI-scikit--learn-orange?style=flat-square)

---

## Features

- **Post Any Task** — Fix a fan, find a tutor, move furniture
- **Real-Time Bidding** — Workers bid live via WebSocket
- **AI Task Classification** — TF-IDF + Logistic Regression (85%+ accuracy)
- **Fair Price Estimation** — RandomForest regression model
- **Worker Match Scoring** — Weighted formula (skill fit + rating + proximity + experience)
- **Map-Based Discovery** — Leaflet.js + OpenStreetMap
- **Escrow Simulation** — Payment locked until task completion
- **Mutual Ratings** — Both poster and worker rate each other

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js + Tailwind CSS (v4) |
| Backend | Python Flask + Flask-SocketIO |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | JWT (PyJWT / flask-jwt-extended) |
| Real-Time | Flask-SocketIO + socket.io-client |
| Maps | Leaflet.js + OpenStreetMap |
| AI/ML | scikit-learn + joblib |
| Deployment | Render |

---

## Project Structure

```
KaamDo/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── config.py               # Configuration
│   ├── models/                 # Database models
│   ├── routes/                 # API routes
│   ├── ai/
│   │   ├── classifier.py       # Task classifier
│   │   ├── price_estimator.py  # Price estimator
│   │   ├── match_score.py      # Worker matching
│   │   └── models/             # Saved .pkl files
│   ├── notebooks/              # Training notebooks
│   └── requirements.txt
├── src/                        # React frontend
│   ├── pages/
│   ├── components/
│   ├── context/
│   └── App.jsx
├── index.html
├── package.json
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train AI models
python notebooks/train_classifier.py
python notebooks/train_price_estimator.py

# Run the server
python app.py
```

Server starts at `http://localhost:5000`

### Frontend Setup

```bash
# From project root
npm install
npm run dev
```

Frontend starts at `http://localhost:5173` (proxies API to Flask)

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Get current user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks?lat=X&lng=Y&radius=Z` | Get nearby tasks |
| GET | `/api/tasks/:id` | Get task detail |
| PATCH | `/api/tasks/:id/status` | Update status |

### Bids
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bids` | Place a bid |
| GET | `/api/tasks/:id/bids` | Get bids on task |
| PATCH | `/api/bids/:id/accept` | Accept a bid |

### AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/classify` | Classify task text |
| POST | `/api/ai/estimate-price` | Get price range |
| POST | `/api/ai/match-workers` | Rank workers |

### Ratings
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ratings` | Submit rating |
| GET | `/api/users/:id/ratings` | Get user ratings |

---

## AI Models

### Task Classifier
- **Model**: TF-IDF + Logistic Regression
- **Training Data**: 315 labeled task descriptions
- **Categories**: Home Repair, Education, Delivery, Labour & Moving, Cleaning, Tech Help, General
- **Accuracy**: ~86%

### Fair Price Estimator
- **Model**: RandomForest Regressor
- **Features**: Category (encoded), radius_km
- **Training Data**: 500 synthetic task records

### Worker Match Score
- **Method**: Weighted formula (no ML)
- **Weights**: Skill match (40%) + Rating (30%) + Proximity (20%) + Experience (10%)

---

## Team

Built by first-year CSE students as a capstone project.

---

## License

MIT
