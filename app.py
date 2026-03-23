from flask import Flask, render_template, request, redirect
import random, datetime

app = Flask(__name__)

slushies = []

flavors = ["Mango","Cola","Blue Raspberry","Strawberry","Grape","Lemon","Watermelon"]
toppings = ["Boba","Jelly","Ice Cream","Whipped Crea","Sprinkles"]

color_map = {
    "Mango": #fbbf24,
    "Cola": #7c2d12
    "Blue Raspberry": #3b82f6,
    "Strawberry": #ef4444,
    "Grape": #8b5cf6,
    "Lemon": #eab308,
    "Watermelon": #22c55e
}