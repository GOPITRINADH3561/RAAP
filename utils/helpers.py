import pandas as pd
import os

def sanitize_email(email: str) -> str:
    user = email.strip().split("@")[0]
    return f"{user}@uh.edu"

def ensure_data_file(path: str) -> pd.DataFrame:
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Professor Name", "Professor Mail", "Professor Department", "FollowUp"])
        df.to_csv(path, index=False)
    return pd.read_csv(path)

def load_data(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["Professor Name", "Professor Mail", "Professor Department", "FollowUp"])

def save_data(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def add_entry(name: str, email: str, dept: str, path: str):
    df = load_data(path)
    new_row = {
        "Professor Name": name,
        "Professor Mail": email,
        "Professor Department": dept,
        "FollowUp": False
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df, path)

def delete_entry(name: str, email: str, path: str):
    df = load_data(path)
    df = df[~((df["Professor Name"] == name) & (df["Professor Mail"] == email))]
    save_data(df, path)
