INSERT INTO clones
	(full_repo_name, timestamp, count, uniques, utc_datetime_update)
VALUES
	(?, ?, ?, ?, ?)
ON CONFLICT(full_repo_name, timestamp) DO UPDATE SET 
	(full_repo_name, timestamp, count, uniques, utc_datetime_update) = (?, ?, ?, ?, ?)
WHERE
	utc_datetime_update < ?
