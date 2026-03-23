# Slushie Lab

Slushie Lab is a Flask web app where you can create, explore, edit, vote on, and delete custom slushie recipes.

## Feature-by-Feature Implementation

### Feature 1: Core routes and app flow

- Home dashboard route: `/`
- Create route: `/create`
- Explore route: `/explore`
- Slushie details route: `/slushie/<id>`
- Bonus routes: `/roulette`, `/today`

### Feature 2: Basic CRUD with SQLite (reward criteria)

- **Create** slushies with custom or auto-generated names
- **Read** all slushies in gallery and each detail page
- **Update** existing slushies via `/slushie/<id>/edit`
- **Delete** slushies via `/slushie/<id>/delete`

### Feature 3: Voting interactions

- Like and dislike actions on saved slushies
- Vote counters stored persistently in SQLite

### Feature 4: Styling and responsive UI

- Shared layout with navigation
- Custom design system in `static/styles.css`
- Mobile-friendly cards/forms/navigation

## Tech Stack

- Python 3
- Flask
- SQLite (built into Python)
- HTML + CSS

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Then open: <http://127.0.0.1:5000>

## Dependencies

- Flask==3.1.0

## Suggested Screenshots for Submission

Add screenshots here after running the app:

1. Home page dashboard
2. Create form page
3. Explore gallery page
4. Slushie detail page with vote buttons
5. Edit flow and delete flow

## Project Notes for YSWS Checklist

- At least 3 routes: complete
- Unique and styled web app: complete
- Dependencies listed in requirements.txt: complete
- README includes project description: complete
- Higher reward criterion implemented: **Basic CRUD with SQLite**

Remember to:

- Commit at least once per hour while coding
- Log your project time on Hackatime
