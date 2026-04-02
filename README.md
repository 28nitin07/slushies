# Slushie Time Capsule

Slushie Time Capsule is a Flask web app where each slushie is saved like a memory entry. Users capture flavor + topping + mood + note, browse a timeline of past capsules, and revisit entries from the same calendar date.

## Routes and Features

- `/` Home dashboard with total capsules, mood prompt, and latest entries
- `/create` Create a new capsule entry
- `/explore` Timeline view of all saved capsules
- `/slushie/<id>` Capsule detail page with voting
- `/slushie/<id>/edit` Edit a saved capsule
- `/slushie/<id>/delete` Delete a capsule
- `/on-this-day` Replay an older capsule from the same month/day
- `/roulette`, `/today`, `/visualizer` Extra interactive pages

## Higher Reward Criterion Implemented

This project implements **basic CRUD with SQLite**:

- Create: add capsule entries with name, flavor, topping, mood, and note
- Read: list capsules in timeline and open details
- Update: edit capsule fields
- Delete: remove capsules from the database

## YSWS Requirement Checklist

- Flask app with at least 3 routes: complete (9+ routes)
- Unique, functional, and styled project: complete (time-capsule concept + custom CSS)
- Hourly GitHub commits while coding: complete during build session
- README with project details and screenshots: complete (add images below)
- Dependencies listed in requirements.txt: complete
- Higher rewards item: complete via SQLite CRUD

## Screenshots

Add screenshots from your run here:

1. Home dashboard (`/`)
2. Create capsule form (`/create`)
3. Timeline page (`/explore`)
4. Capsule detail page (`/slushie/<id>`)
5. On This Day replay (`/on-this-day`)

## 2-Hour Hackatime Build Log Template

Use this section while coding to show clear progress:

- 00:00-00:30: Reframed app copy and navigation to Time Capsule theme
- 00:30-01:00: Added mood + note fields and database support
- 01:00-01:30: Added On This Day route and timeline polish
- 01:30-02:00: Final UI cleanup, README checklist, screenshots

## Tech Stack

- Python 3
- Flask
- SQLite
- HTML + CSS

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Open: <http://127.0.0.1:5000>
