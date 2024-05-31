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
        response = {"email": email, "message": "user created"}
        return jsonify(response), 200
    except ValueError:
        response = {"message": "email already registered"}
        return jsonify(response), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
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


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """Retrieves the email from the request form and
    Find the user and return a password reset token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """Update user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    response = {"email": email, "message": "Password updated"}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
