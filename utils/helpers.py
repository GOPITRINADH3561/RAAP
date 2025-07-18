import pandas as pd
import os

# Sanitize email (e.g., gopi@cs -> gopi@uh.edu)
def sanitize_email(email: str) -> str:
    user = email.strip().split("@")[0]
    return f"{user}@uh.edu"

# Ensure data directory and base file exist
def ensure_data_file(path):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Professor Name", "Professor Mail", "Professor Department", "FollowUp"])
        df.to_csv(path, index=False)

# Load tracker data and fix column order/types
def load_data(data_path):
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        if df.empty or not set(["Professor Name", "Professor Mail", "Professor Department", "FollowUp"]).issubset(df.columns):
            df = pd.DataFrame(columns=["Professor Name", "Professor Mail", "Professor Department", "FollowUp"])
    else:
        df = pd.DataFrame(columns=["Professor Name", "Professor Mail", "Professor Department", "FollowUp"])
    return df


# Save dataframe back to CSV
def save_data(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def add_entry(name, email, department, data_path):
    df = load_data(data_path)

    new_entry = {
        "Professor Name": name,
        "Professor Mail": email,
        "Professor Department": department,
        "FollowUp": False
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df, data_path)


# Delete matching entry
def delete_entry(name: str, email: str, path: str):
    df = load_data(path)
    df = df[~((df["Professor Name"] == name) & (df["Professor Mail"] == sanitize_email(email)))]
    save_data(df, path)
