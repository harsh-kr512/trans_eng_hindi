# auth.py
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash

USER_CSV = "users.csv"

def load_users():
    if not os.path.exists(USER_CSV):
        return {}
    df = pd.read_csv(USER_CSV)
    return {row["username"]: row["password"] for _, row in df.iterrows()}

def save_user(username, password_hash):
    new_user = pd.DataFrame([[username, password_hash]], columns=["username", "password"])
    if os.path.exists(USER_CSV):
        new_user.to_csv(USER_CSV, mode='a', header=False, index=False)
    else:
        new_user.to_csv(USER_CSV, index=False)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    save_user(username, generate_password_hash(password))
    return True, "Registration successful!"

def verify_user(username, password):
    users = load_users()
    hashed = users.get(username)
    if hashed:
        return check_password_hash(hashed, password)
    return False
