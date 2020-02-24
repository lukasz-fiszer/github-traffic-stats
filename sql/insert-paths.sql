INSERT INTO paths
	(full_repo_name, path, title, count, uniques, utc_datetime_update)
VALUES
	(?, ?, ?, ?, ?, ?)
ON CONFLICT(full_repo_name, path, utc_datetime_update) DO UPDATE SET 
	(full_repo_name, path, title, count, uniques, utc_datetime_update) = (?, ?, ?, ?, ?, ?)
