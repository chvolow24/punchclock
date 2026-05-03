SELECT
	*
	, datetime(punch_in_ts, "localtime") as punch_in_localtime
	, datetime(punch_out_ts, "localtime") as punch_out_localtime
FROM time_blocks WHERE block_id = ?
