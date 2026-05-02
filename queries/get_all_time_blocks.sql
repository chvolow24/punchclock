SELECT
	block_id
	, job_id
	, punch_in_ts
	, punch_out_ts
	, datetime(punch_in_ts, "localtime") as punch_in_localtime
	, datetime(punch_out_ts, "localtime") as punch_out_localtime
	, backed_up_ts
	, submitted_ts
	, (strftime("%s", punch_out_ts) - strftime("%s", punch_in_ts)) / 3600.0
        AS block_dur_hours
	-- , block_dur_hours
FROM time_blocks
