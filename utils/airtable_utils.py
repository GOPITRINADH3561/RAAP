import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

table = Table(AIRTABLE_TOKEN, BASE_ID, TABLE_NAME)

def get_all_entries():
    return table.all()

def add_entry(name, email, dept, followup=False):
    table.create({
        "Professor Name": name,
        "Professor Mail": email,
        "Professor Department": dept,
        "FollowUp": followup
    })

def update_followup(record_id, followup):
    table.update(record_id, {"FollowUp": followup})

def delete_entry(record_id):
    table.delete(record_id)
