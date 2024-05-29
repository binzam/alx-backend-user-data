#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Retrieve form data and handles user registration"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response), 200
    except ValueError:
        response = {"message": "email already registered"}
        return jsonify(response), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Retrieve form data and handle user login"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify(
            {"email": email, "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Retrieves the session ID from the request cookies and
    Find the user.Handle logout by destroying that session and
    redirect the user to GET '/'"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Retrieves the session ID from the request cookies and
    Find the user and return user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
