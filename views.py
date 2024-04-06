from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
#request (for query parameters)
# Run pip install Flask-Session first
from flask_session import Session
from flask_cors import CORS, cross_origin

views = Blueprint(__name__, "views")
CORS(views)


@views.route("/")
def home():
    name = request.args.get('username')
    return render_template("homepage.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/register")
def register():
    return render_template("register.html")

@views.route("/logout")
def logout():
    return render_template("logout.html")

@views.route("/locate-CP")
def locate_CP():
    return render_template("locateCP.html")

@views.route("/extendendtime")
def extendendtime():
    return render_template("extendendtime.html")

@views.route("/nearbyAmenities")
def nearby_Amenities():
    return render_template("nearbyAmenities.html")