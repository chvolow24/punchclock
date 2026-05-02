from flask import Flask, render_template, redirect, make_response, Response
import database
import csv
import io
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/job/<job_id>")
def route_job(job_id):
    job = database.get_job(job_id)
    return render_template("job.html", job=job)

@app.route("/job/<job_id>/time_blocks")
def route_job_time_blocks(job_id):
    blocks = database.get_all_time_blocks_for_job(job_id)
    return render_template("time_blocks.html", job_id=job_id, blocks=blocks)

@app.route("/time_blocks_all_write_csv")
def route_time_blocks_all_csv():
    blocks = database.get_all_time_blocks()

    output = io.StringIO()

    keys = blocks[0].keys()
    writer = csv.DictWriter(output, fieldnames=keys)

    writer.writeheader()

    for row in blocks:
        writer.writerow(dict(row))

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=time_blocks_all.csv"
        }
    )

@app.route("/job/<job_id>/punchclock/submit", methods=["POST"])
def route_punchclock_submit(job_id):
    status = database.get_status(job_id)
    if status["next_punch_type"] == 0:
        # punch in
        database.register_punch(job_id, None, 0)
        return redirect(f"/job/{job_id}/time_blocks")
    elif status["next_punch_type"] == 1:
        # punch out
        database.register_punch(job_id, status["block_id"], 1)
        return redirect(f"/job/{job_id}/time_blocks")
    else:
        return f"<p>Error: 'next punch type' is {status['next_punch_type']}</p>"
    

@app.route("/job/<job_id>/punchclock")
def route_punchclock(job_id):
    job = database.get_job(job_id)
    status = database.get_status(job_id)
    resp = make_response(render_template("punchclock.html", job=job, status=status))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.route("/")
def route_index():
    jobs = database.get_jobs()
    return render_template("index.html", jobs=jobs)
    # return render_template("test.html", status=status)

@app.route("/init")
def route_init():
    return database.init()
    
