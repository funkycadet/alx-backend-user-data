#!/usr/bin/env python3
""" App module
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """ Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Users route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Logs in a user on the basis that the credentials provided are correct
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    new_session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", new_session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out the current user and deletes their session ID
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Returns the current user profile details
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Resets the password for the requested user
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
