INSERT INTO referrers
	(full_repo_name, referrer, count, uniques, utc_datetime_update)
VALUES
	(?, ?, ?, ?, ?)
ON CONFLICT(full_repo_name, referrer, utc_datetime_update) DO UPDATE SET 
	(full_repo_name, referrer, count, uniques, utc_datetime_update) = (?, ?, ?, ?, ?)
