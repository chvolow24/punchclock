SELECT
	t.block_id
	, datetime(t.punch_in_ts, "localtime") as punch_in_localtime
	, datetime(t.punch_out_ts, "localtime") as punch_out_localtime
	, (strftime("%s", t.punch_out_ts) - strftime("%s", t.punch_in_ts)) / 3600.0
        AS block_dur_hours
	, p.pay_rate_hourly
FROM time_blocks t
LEFT JOIN job_pay_rates p ON
	p.job_id = t.job_id
	AND p.effective <= t.punch_in_ts
	AND (p.deprecated IS NULL OR p.deprecated > t.punch_out_ts)
WHERE t.job_id = ?;
