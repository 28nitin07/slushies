from flask import Flask, render_template, request, redirect
import random, datetime

app = Flask(__name__)

slushies = []

flavors = ["Mango","Cola","Blue Raspberry","Strawberry","Grape","Lemon","Watermelon"]
toppings = ["Boba","Jelly","Ice Cream","Whipped Crea","Sprinkles"]

color_map = {
    "Mango": "#fbbf24",
    "Cola": "#7c2d12",
    "Blue Raspberry": "#3b82f6",
    "Strawberry": "#ef4444",
    "Grape": "#8b5cf6",
    "Lemon": "#eab308",
    "Watermelon": "#22c55e"
}

@app.route("/")
def index():
    return render_template("index.html", total=len(slushies))

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        flavor = request.form("flavor")
        topping = request.form["topping"]

        name = f"{flavor} {random.choice(['Blast','Storm','Rush'])}"

        slushie = {
            "id": len(slushies),
            "name": name,
            "flavor": flavor,
            "topping": topping,
            "color": color_map.get(flavor, '#ccc'),
            "likes": 0,
            "dislikes": 0
        }

        slushies.append(slushie)
        return redirect(f"/slushie/{slushie['id']}")
    
    return render_template("create.html", flavors=flavors, toppings=toppings)

@app.route("/explore")
def explore():
    return render_template("explore.html", slushies=slushies)

@app.route("/slushie/<int:id>")
def view_slushie(id):
    slushie = slushies[id]
    return render_template("slushie.html", slushie=slushie)

@app.route("/roulette")
def roulette():
    flavor = random.choice(flavors)
    topping = random.choice(toppings)

    slushie = {
        "name": f"{flavor} Chaos",
        "flavor": flavor,
        "topping": topping,
        "color": color_map.get(flavor)
    }

    return render_template("slushie.html", s=slushie)

@app.route("/today")
def today():
    random.seed(str(datetime.date.today()))
    
    flavor = random.choice(flavors)
    topping = random.choice(toppings)

    slushie = {
        "name": f"{flavor} of the day",
        "flavor":flavor,
        "topping":topping,
        "color":color_map.get(flavor)
    }

    return render_template("slushie.html", s=slushie)

@app.route("/vote/<int:id>/<action>")
def vote(id, action):
    slushie = slushies[id]

    if action == "like":
        slushies[id]["likes"] += 1
    elif action == "dislike":
        slushies[id]["dislikes"] += 1
    
    return redirect(f"/slushie/{id}")




