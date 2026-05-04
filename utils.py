from os import environ
from warnings import warn
from datetime import datetime

def load_file_string(filepath):
    filestr = ""
    with open(filepath, "r") as f:
        filestr = f.read()
    return filestr

def read_dotenv():
    try:
        with open(".env", "r") as f:
            line = f.readline()
            while line:
                pair = [item.strip() for item in line.split("=")]
                environ[pair[0]] = pair[1]
                line = f.readline()
    except FileNotFoundError:
        warn("No .env file found; DB filename usually included there.")
            
def get_env(key):
    return environ[key]

def datetime_sqlite_to_html(sqlite_datetime: str) -> str:
    return sqlite_datetime.replace(" ", "T")[:16]

def datetime_html_to_sqlite(html_datetime: str) -> str:
    return html_datetime.replace("T", " ")
    

def datetime_sqlite_to_table_display(sqlite_datetime: str) ->str:
    if sqlite_datetime is None:
        return "None"
    dt = datetime.strptime(sqlite_datetime, "%Y-%m-%d %H:%M:%S")
    return datetime.strftime(dt, "%A, %m/%d/%y %H:%M")
