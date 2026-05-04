from flask import Flask, render_template, redirect, make_response, Response, request
import database
import csv
import io
import utils
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# @app.route("/job/<job_id>")
# def route_job(job_id):
#     job = database.get_job(job_id)
#     return render_template("job.html", job=job)

@app.route("/edit_timeblock/<block_id>/submit", methods=["POST"])
def route_edit_timeblock_submit(block_id):
    new_in_ts_local = utils.datetime_html_to_sqlite(request.form.get("punch_in_ts_local"))
    new_out_ts_local = utils.datetime_html_to_sqlite(request.form.get("punch_out_ts_local"))
    database.put_update_time_block(block_id, new_in_ts_local, new_out_ts_local)
    job_id = request.form.get("job_id")
    return redirect(f"/job/{job_id}/time_blocks")

@app.route("/edit_timeblock/<block_id>")
def route_edit_timeblock(block_id):
    block = database.get_block(block_id)
    block["in_ts_editable"] = utils.datetime_sqlite_to_html(block["punch_in_localtime"])
    if block["punch_out_localtime"] is not None:
        block["out_ts_editable"] = utils.datetime_sqlite_to_html(block["punch_out_localtime"])
    else:
        block["out_ts_editable"] = "2026-01-01T00:00:00"
    return render_template("edit_timeblock.html", block=block)

@app.route("/job/<job_id>/time_blocks")
def route_job_time_blocks(job_id):
    blocks = database.get_all_time_blocks_for_job(job_id)
    blocks = [dict(block) for block in database.get_all_time_blocks_for_job(job_id)]
    for block in blocks:
        block["punch_in_localtime"] = utils.datetime_sqlite_to_table_display(block["punch_in_localtime"])
        block["punch_out_localtime"] = utils.datetime_sqlite_to_table_display(block["punch_out_localtime"])
        if block["block_dur_hours"] is not None:
            block["block_dur_hours"] = format(block["block_dur_hours"], ".1f")
            if block["pay_rate_hourly"] is not None:
                accrued = float(block["block_dur_hours"]) * float(block["pay_rate_hourly"])
                block["accrued"] = format(accrued, ".2f")
        if block["pay_rate_hourly"] is not None:
            block["pay_rate_hourly"] = format(block["pay_rate_hourly"], ".2f")

            
    return render_template("time_blocks.html", job_id=job_id, blocks=blocks)

@app.route("/add_job_submit", methods=["POST"])
def route_add_job_submit():
    job_name = request.form.get("job_name")
    init_pay_rate = request.form.get("init_pay_rate")
    database.add_job(job_name, init_pay_rate)
    return redirect("/")    

@app.route("/add_job")
def route_add_job():
    return render_template("add_job.html")

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
        database.post_punch(job_id, None, 0)
        return redirect(f"/job/{job_id}/punchclock")
    elif status["next_punch_type"] == 1:
        # punch out
        database.post_punch(job_id, status["block_id"], 1)
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

@app.route("/delete_job/<job_id>")
def route_delete_job(job_id):
    database.delete_job(job_id)
    return redirect("/")

@app.route("/undelete_job/<job_id>")
def route_undelete_job(job_id):
    database.undelete_job(job_id)
    return redirect("/deleted_jobs")

@app.route("/deleted_jobs")
def route_deleted_jobs():
    jobs = database.get_deleted_jobs()
    return render_template("deleted_jobs.html", jobs=jobs)

@app.route("/deleted_time_blocks/<job_id>")
def route_deleted_time_blocks(job_id):
    deleted_blocks = database.get_deleted_time_blocks(job_id)
    return render_template("deleted_time_blocks.html", blocks=deleted_blocks)

@app.route("/delete_time_block/<block_id>")
def route_delete_time_block(block_id):
    database.delete_time_block(block_id)
    block = database.get_block(block_id)
    return redirect(f"/job/{block['job_id']}/time_blocks")

@app.route("/undelete_time_block/<block_id>")
def route_undelete_time_block(block_id):
    database.undelete_time_block(block_id)
    block = database.get_block(block_id)
    return redirect(f"/deleted_time_blocks/{block['job_id']}")


