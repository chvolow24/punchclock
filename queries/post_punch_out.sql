UPDATE time_blocks
SET punch_out_ts = datetime('now') -- new ts
WHERE block_id = ?                 -- PARAM 0: block id
