UPDATE time_blocks
SET
	punch_in_ts_original
		= CASE
			WHEN punch_in_ts_original IS NULL THEN punch_in_ts
			ELSE punch_in_ts_original
		END
	, punch_out_ts_original
		= CASE
			WHEN punch_out_ts_original IS NULL THEN punch_out_ts
			ELSE punch_out_ts_original
		END
	, punch_in_ts = datetime(?, 'utc')		-- PARAM 0: punch in localtime
	, punch_out_ts = datetime(?, 'utc')     -- PARAM 1: punch out localtime
			
WHERE block_id = ?              -- PARAM 2: block id
