import sqlite3
import utils
from typing import List, Dict

def db_connect():
    utils.read_dotenv()
    try:
        db_file = utils.get_env("PUNCHCLOCK_DB_FILENAME")
    except KeyError:
        raise KeyError("Environment variable \"PUNCHCLOCK_DB_FILENAME\" must be set.")
    try:
        conn = sqlite3.connect(db_file)
    except Exception:
        raise ValueError(f"Unable to connect to database at \"{db_file}\"")
    return conn

def init() -> str:
    query = utils.load_file_string("queries/init.sql")
    conn = db_connect()
    try:
        conn.executescript(query)
    except Exception as e:
        conn.close()
        return f"<p>Error: {str(e)}</p>"
    conn.close()
    return "Initialized OK"

def get_status(job_id: int) -> dict:
    query = utils.load_file_string("queries/status.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    rows = list(cur.fetchall())
    if len(rows) < 1:
        ret: dict = {}
        ret["block_id"] = None
        ret["next_punch_type"] = 0
        conn.close()
        return ret
    if len(rows) > 1:
        conn.close()
        raise ValueError('Multiple time blocks unclosed')
    conn.close()
    return dict(rows[0])

def post_punch(job_id: int, block_id: int, punch_type: int) -> None:
    query = ""
    param: tuple[int, ...] = ()
    if punch_type == 0:
        query = utils.load_file_string("queries/post_punch_in.sql")
        param = (job_id,)
    else:
        query = utils.load_file_string("queries/post_punch_out.sql")
        param = (block_id,)
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query, param)
    conn.commit()
    conn.close()

def put_update_time_block(block_id: int, new_in_ts_local: str, new_out_ts_local: str) -> None:
    query = utils.load_file_string("queries/update_time_block.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (new_in_ts_local, new_out_ts_local, block_id)
    cur.execute(query, params)
    conn.commit()
    conn.close()

    
def get_jobs() -> list:
    query = utils.load_file_string("queries/get_jobs.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = list(cur.fetchall())
    conn.close()
    return rows

def get_job(job_id: int) -> dict:
    query = utils.load_file_string("queries/get_job.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    rows = list(cur.fetchall())
    conn.close()
    return dict(rows[0])

def get_block(block_id: int) ->dict:
    query = utils.load_file_string("queries/get_block.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (block_id,))
    rows = list(cur.fetchall())
    conn.close()
    return dict(rows[0])
    

def get_all_time_blocks_for_job(job_id: int) -> list:
    query = utils.load_file_string("queries/get_all_for_job.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    rows = list(cur.fetchall())
    conn.close()
    return rows

def get_all_time_blocks() -> list:
    query = utils.load_file_string("queries/get_all_time_blocks.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = list(cur.fetchall())
    conn.close()
    return rows

def add_job(job_name, init_pay_rate) -> None:
    query = utils.load_file_string("queries/add_job.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (job_name,)
    cur.execute(query, params)
    query = utils.load_file_string("queries/add_pay_rate_for_new_job.sql")
    params = (init_pay_rate,)
    cur.execute(query, params)
    conn.commit()
    conn.close()

def delete_job(job_id) -> None:
    query = utils.load_file_string("queries/delete_job.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (job_id,)
    cur.execute(query, params)
    conn.commit()
    conn.close()

    
def undelete_job(job_id) -> None:
    query = utils.load_file_string("queries/undelete_job.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (job_id,)
    cur.execute(query, params)
    conn.commit()
    conn.close()



def get_deleted_jobs() -> List[Dict]:
    query = utils.load_file_string("queries/get_deleted_jobs.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = list(cur.fetchall())
    conn.close()
    return rows

def get_deleted_time_blocks(job_id) -> List[Dict]:
    query = utils.load_file_string("queries/get_deleted_time_blocks.sql")
    conn = db_connect()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (job_id,)
    cur.execute(query, params)
    rows = list(cur.fetchall())
    conn.close()
    return rows
    

def delete_time_block(block_id: int) -> None:
    query = utils.load_file_string("queries/delete_time_block.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (block_id,)
    cur.execute(query, params)
    conn.commit()
    conn.close()

def undelete_time_block(block_id: int) -> None:
    query = utils.load_file_string("queries/undelete_time_block.sql")
    conn = db_connect()
    cur = conn.cursor()
    params = (block_id,)
    cur.execute(query, params)
    conn.commit()
    conn.close()
    
