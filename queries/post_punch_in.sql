INSERT INTO time_blocks VALUES(
	NULL   --          (autopop block ID)
	, datetime('now')--(punch in ts)
	, NULL --          (punch out ts)
	, ?    -- PARAM 0: job id
	, NULL --		   (backed up ts)
	, NULL --		   (submitted ts)
);
