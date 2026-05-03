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
	-- , block_dur_hours REAL GENERATED ALWAYS AS (
	-- 	(strftime("%s", punch_out_ts) - strftime("%s", punch_in_ts)) / 3600.0
	-- 	) VIRTUAL
	, punch_in_ts_original TEXT
	, punch_out_ts_original TEXT
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
	(0, 0, 16.0, "2026-01-01", "2026-05-02")
	, (1, 0, 25, "2026-05-02", NULL)
	, (2, 1, 20.0, "2026-01-01", NULL)
;
