# F1 Replay

An interactive Formula 1 race replay in the browser. Pick a season, Grand Prix and session, then watch the drivers move around the circuit, with optional braking zones overlaid on the track.

Built on [FastF1](https://github.com/theOehrly/Fast-F1) for timing and telemetry data, served by FastAPI, and rendered with plain HTML Canvas (no frontend framework).

## Features

- Circuit rendered from real GPS position data
- Animated multi-driver replay
- Optional braking zones, toggled from the UI
- Session selector (seasons 2018 onward)

## Tech stack

| Layer | Tool |
|---|---|
| Data | FastF1 (Python) |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML, CSS, JavaScript, Canvas |

## Getting started

### Prerequisites

- Python 3.10+
- An internet connection on first load (FastF1 downloads session data, then caches it)

### Installation

```bash
git clone <your-repo-url>
cd f1-replay
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

> The first load of a session can take a while because FastF1 downloads and caches the data. Later loads of the same session are much faster.

## Project structure

```
f1-replay/
├── main.py            # FastAPI app and endpoints
├── static/            # Frontend (HTML, CSS, JS, Canvas rendering)
├── requirements.txt
└── README.md
```

## Roadmap

- [ ] Dynamic session options per Grand Prix (hide invalid ones, e.g. Sprint on non-sprint weekends)
- [ ] Playback controls: play/pause and scrub
- [ ] Race strategy dashboard: tyre stints, degradation, pit stops, undercut/overcut detection
- [ ] Sprint and qualifying replays

## Data and credits

Race data comes from the FastF1 library, which accesses F1 timing data. This project is unofficial and is not associated with Formula 1, the FIA or any team.

## License

MIT
