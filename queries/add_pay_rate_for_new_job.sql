INSERT INTO job_pay_rates VALUES(
	NULL
	, (SELECT MAX(job_id) FROM jobs)
	, ?				-- PARAM 0: hourly rate
	, datetime('now', '-1 year')
	, NULL
);
	
