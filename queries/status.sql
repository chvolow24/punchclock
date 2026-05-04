WITH tmp AS (
	SELECT * FROM time_blocks
	WHERE job_id = ? -- PARAM 0: job_id
	AND deleted = 0
	ORDER BY punch_in_ts DESC
	LIMIT 1
)

SELECT
	a.block_id
	, a.punch_out_ts IS NULL AS next_punch_type
FROM tmp a
LEFT JOIN jobs b on b.job_id = a.job_id
