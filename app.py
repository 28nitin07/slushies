from __future__ import annotations

import datetime
import random
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "slushie-lab-dev-key"
app.config["DATABASE"] = Path(app.root_path) / "slushies.db"

FLAVORS = [
    "Mango",
    "Cola",
    "Blue Raspberry",
    "Strawberry",
    "Grape",
    "Lemon",
    "Watermelon",
]

TOPPINGS = ["Boba", "Jelly", "Ice Cream", "Whipped Cream", "Sprinkles"]

MOODS = ["Chill", "Hyped", "Nostalgic", "Focused", "Chaotic"]

COLOR_MAP = {
    "Mango": "#f59e0b",
    "Cola": "#7c2d12",
    "Blue Raspberry": "#1d4ed8",
    "Strawberry": "#dc2626",
    "Grape": "#6d28d9",
    "Lemon": "#ca8a04",
    "Watermelon": "#16a34a",
}


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error: Exception | None = None) -> None:
    _ = error
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS slushies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            flavor TEXT NOT NULL,
            topping TEXT NOT NULL,
            mood TEXT NOT NULL DEFAULT 'Chill',
            note TEXT NOT NULL DEFAULT '',
            likes INTEGER NOT NULL DEFAULT 0,
            dislikes INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    existing_columns = {
        row["name"] for row in db.execute("PRAGMA table_info(slushies)").fetchall()
    }
    if "mood" not in existing_columns:
        db.execute("ALTER TABLE slushies ADD COLUMN mood TEXT NOT NULL DEFAULT 'Chill'")
    if "note" not in existing_columns:
        db.execute("ALTER TABLE slushies ADD COLUMN note TEXT NOT NULL DEFAULT ''")

    db.commit()


def fetch_slushie(slushie_id: int) -> sqlite3.Row:
    slushie = get_db().execute(
        "SELECT * FROM slushies WHERE id = ?", (slushie_id,)
    ).fetchone()
    if slushie is None:
        abort(404)
    return slushie


def slug_name(flavor: str) -> str:
    return f"{flavor} {random.choice(['Blast', 'Storm', 'Rush'])}"


@app.before_request
def bootstrap_database() -> None:
    init_db()


@app.route("/")
def index():
    db = get_db()
    total = db.execute("SELECT COUNT(*) AS c FROM slushies").fetchone()["c"]
    newest = db.execute(
        "SELECT * FROM slushies ORDER BY id DESC LIMIT 3"
    ).fetchall()
    day_seed = datetime.date.today().isoformat()
    rng = random.Random(day_seed)
    today_prompt = rng.choice(MOODS)
    return render_template(
        "index.html",
        total=total,
        newest=newest,
        color_map=COLOR_MAP,
        today_prompt=today_prompt,
    )


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        flavor = request.form.get("flavor", "").strip()
        topping = request.form.get("topping", "").strip()
        name = request.form.get("name", "").strip()
        mood = request.form.get("mood", "").strip()
        note = request.form.get("note", "").strip()

        if flavor not in FLAVORS or topping not in TOPPINGS or mood not in MOODS:
            flash("Choose valid flavor, topping, and mood values.", "error")
            return redirect(url_for("create"))
        if len(note) > 280:
            flash("Memory note must be 280 characters or fewer.", "error")
            return redirect(url_for("create"))

        if not name:
            name = slug_name(flavor)

        db = get_db()
        cursor = db.execute(
            "INSERT INTO slushies (name, flavor, topping, mood, note) VALUES (?, ?, ?, ?, ?)",
            (name, flavor, topping, mood, note),
        )
        db.commit()
        flash("Capsule created.", "success")
        return redirect(url_for("view_slushie", slushie_id=cursor.lastrowid))

    return render_template(
        "create.html",
        flavors=FLAVORS,
        toppings=TOPPINGS,
        moods=MOODS,
        color_map=COLOR_MAP,
    )


@app.route("/explore")
def explore():
    slushies = get_db().execute("SELECT * FROM slushies ORDER BY id DESC").fetchall()
    return render_template("explore.html", slushies=slushies, color_map=COLOR_MAP)


@app.route("/slushie/<int:slushie_id>")
def view_slushie(slushie_id: int):
    slushie = fetch_slushie(slushie_id)
    return render_template("slushie.html", slushie=slushie, color_map=COLOR_MAP)


@app.route("/slushie/<int:slushie_id>/edit", methods=["GET", "POST"])
def edit_slushie(slushie_id: int):
    slushie = fetch_slushie(slushie_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        flavor = request.form.get("flavor", "").strip()
        topping = request.form.get("topping", "").strip()
        mood = request.form.get("mood", "").strip()
        note = request.form.get("note", "").strip()

        if (
            not name
            or flavor not in FLAVORS
            or topping not in TOPPINGS
            or mood not in MOODS
        ):
            flash("Provide valid values for all fields.", "error")
            return redirect(url_for("edit_slushie", slushie_id=slushie_id))
        if len(note) > 280:
            flash("Memory note must be 280 characters or fewer.", "error")
            return redirect(url_for("edit_slushie", slushie_id=slushie_id))

        db = get_db()
        db.execute(
            "UPDATE slushies SET name = ?, flavor = ?, topping = ?, mood = ?, note = ? WHERE id = ?",
            (name, flavor, topping, mood, note, slushie_id),
        )
        db.commit()
        flash("Capsule updated.", "success")
        return redirect(url_for("view_slushie", slushie_id=slushie_id))

    return render_template(
        "create.html",
        flavors=FLAVORS,
        toppings=TOPPINGS,
        moods=MOODS,
        color_map=COLOR_MAP,
        slushie=slushie,
        edit_mode=True,
    )


@app.route("/visualizer")
def visualizer():
    flavor = request.args.get("flavor", FLAVORS[0]).strip()
    topping = request.args.get("topping", TOPPINGS[0]).strip()
    name = request.args.get("name", "Live Slushie Preview").strip()

    if flavor not in FLAVORS:
        flavor = FLAVORS[0]
    if topping not in TOPPINGS:
        topping = TOPPINGS[0]
    if not name:
        name = "Live Slushie Preview"

    slushie = {
        "name": name,
        "flavor": flavor,
        "topping": topping,
    }

    return render_template(
        "visualizer.html",
        slushie=slushie,
        flavors=FLAVORS,
        toppings=TOPPINGS,
        color_map=COLOR_MAP,
    )


@app.route("/slushie/<int:slushie_id>/delete", methods=["POST"])
def delete_slushie(slushie_id: int):
    fetch_slushie(slushie_id)
    db = get_db()
    db.execute("DELETE FROM slushies WHERE id = ?", (slushie_id,))
    db.commit()
    flash("Capsule deleted.", "success")
    return redirect(url_for("explore"))


@app.route("/on-this-day")
def on_this_day():
    db = get_db()
    date_key = datetime.date.today().strftime("%m-%d")
    matches = db.execute(
        "SELECT * FROM slushies WHERE strftime('%m-%d', created_at) = ? ORDER BY id DESC",
        (date_key,),
    ).fetchall()

    chosen = random.choice(matches) if matches else None
    return render_template(
        "on_this_day.html",
        chosen=chosen,
        total_matches=len(matches),
        color_map=COLOR_MAP,
    )


@app.route("/roulette")
def roulette():
    flavor = random.choice(FLAVORS)
    topping = random.choice(TOPPINGS)

    slushie = {
        "id": None,
        "name": f"{flavor} Chaos",
        "flavor": flavor,
        "topping": topping,
        "likes": 0,
        "dislikes": 0,
    }
    return render_template(
        "slushie.html", slushie=slushie, color_map=COLOR_MAP, preview_mode=True
    )


@app.route("/today")
def today():
    seed = str(datetime.date.today())
    rng = random.Random(seed)

    flavor = rng.choice(FLAVORS)
    topping = rng.choice(TOPPINGS)

    slushie = {
        "id": None,
        "name": f"{flavor} of the Day",
        "flavor": flavor,
        "topping": topping,
        "likes": 0,
        "dislikes": 0,
    }
    return render_template(
        "slushie.html", slushie=slushie, color_map=COLOR_MAP, preview_mode=True
    )


@app.route("/vote/<int:slushie_id>/<action>")
def vote(slushie_id: int, action: str):
    if action not in {"like", "dislike"}:
        abort(400)

    fetch_slushie(slushie_id)
    field = "likes" if action == "like" else "dislikes"

    db = get_db()
    db.execute(f"UPDATE slushies SET {field} = {field} + 1 WHERE id = ?", (slushie_id,))
    db.commit()

    return redirect(url_for("view_slushie", slushie_id=slushie_id))


if __name__ == "__main__":
    app.run(debug=True)




