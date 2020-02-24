INSERT INTO totals
	(full_repo_name, type, count, uniques, utc_datetime_update)
VALUES
	(?, ?, ?, ?, ?)
ON CONFLICT(full_repo_name, type, utc_datetime_update) DO UPDATE SET 
	(full_repo_name, type, count, uniques, utc_datetime_update) = (?, ?, ?, ?, ?)
