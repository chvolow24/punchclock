import sqlite3
import utils


def init() -> str:
    query = utils.load_file_string("queries/init.sql")
    conn = sqlite3.connect("queries/test.db")
    try:
        conn.executescript(query)
    except Exception as e:
        return f"<p>Error: {str(e)}</p>"
    return "Initialized OK"

def get_status(job_id: int) -> dict:
    query = utils.load_file_string("queries/status.sql")
    conn = sqlite3.connect("queries/test.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    rows = list(cur.fetchall())
    if len(rows) < 1:
        ret: dict = {}
        ret["block_id"] = None
        ret["next_punch_type"] = 0
        return ret
    if len(rows) > 1:
        raise ValueError('Multiple time blocks unclosed')
    return dict(rows[0])

def register_punch(job_id: int, block_id: int, punch_type: int) -> None:
    query = ""
    param: tuple[int, ...] = ()
    if punch_type == 0:
        query = utils.load_file_string("queries/post_punch_in.sql")
        param = (job_id,)
    else:
        query = utils.load_file_string("queries/post_punch_out.sql")
        param = (block_id,)
    conn = sqlite3.connect("queries/test.db")
    cur = conn.cursor()
    cur.execute(query, param)
    conn.commit()
    

def get_jobs() -> list:
    query = utils.load_file_string("queries/get_jobs.sql")
    conn = sqlite3.connect("queries/test.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = list(cur.fetchall())
    return rows

def get_job(job_id: int) -> dict:
    query = utils.load_file_string("queries/get_job.sql")
    conn = sqlite3.connect("queries/test.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    rows = list(cur.fetchall())
    return dict(rows[0])
    

def get_all_time_blocks_for_job(job_id: int) -> list:
    query = utils.load_file_string("queries/get_all_for_job.sql")
    conn = sqlite3.connect("queries/test.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (job_id,))
    return list(cur.fetchall())
