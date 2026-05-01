CREATE TABLE IF NOT EXISTS
jobs(
	job_id INTEGER PRIMARY KEY
	, job_name TEXT
);

CREATE TABLE IF NOT EXISTS
time_blocks(
    block_id INTEGER PRIMARY KEY
    , punch_in_ts TEXT
    , punch_out_ts TEXT
    , job_id INTEGER
    , backed_up_ts TEXT
    , submitted_ts TEXT
	, block_dur_hours REAL GENERATED ALWAYS AS (
		(unixepoch(punch_out_ts) - unixepoch(punch_in_ts)) / 3600.0
		) VIRTUAL
	, FOREIGN KEY(job_id) REFERENCES jobs(job_id)
);

CREATE TABLE IF NOT EXISTS
job_pay_rates(
	job_pay_rate_id INTEGER PRIMARY KEY
	, job_id INTEGER
	, pay_rate_hourly REAL
	, effective TEXT
	, deprecated TEXT
	, FOREIGN KEY(job_id) REFERENCES jobs(job_id)
);

INSERT OR IGNORE INTO jobs VALUES
	(0, "Test Job 1")
	, (1, "Test Job 2")
;

INSERT OR IGNORE INTO job_pay_rates VALUES
	(0, 0, 16.0, "2026-01-01", NULL)
	, (1, 1, 20.0, "2026-01-01", NULL)
;
