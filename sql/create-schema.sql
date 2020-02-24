CREATE TABLE IF NOT EXISTS totals (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	full_repo_name VARCHAR(256) NOT NULL,
	type VARHCHAR(32) NOT NULL,
	count INT NOT NULL,
	uniques INT NOT NULL,
	utc_datetime_update VARCHAR(32) NOT NULL,
	-- UNIQUE(full_repo_name, type, utc_datetime_update)
	CONSTRAINT unique_constraint UNIQUE(full_repo_name, type, utc_datetime_update)
);

CREATE TABLE IF NOT EXISTS referrers (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	full_repo_name VARCHAR(256) NOT NULL,
	referrer VARHCHAR(256) NOT NULL,
	count INT NOT NULL,
	uniques INT NOT NULL,
	utc_datetime_update VARCHAR(32) NOT NULL,
	-- UNIQUE(full_repo_name, referrer, utc_datetime_update)
	CONSTRAINT unique_constraint UNIQUE(full_repo_name, referrer, utc_datetime_update)
);

CREATE TABLE IF NOT EXISTS paths (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	full_repo_name VARCHAR(256) NOT NULL,
	path VARHCHAR(512) NOT NULL,
	title VARHCHAR(512) NOT NULL,
	count INT NOT NULL,
	uniques INT NOT NULL,
	utc_datetime_update VARCHAR(32) NOT NULL,
	-- UNIQUE(full_repo_name, path, utc_datetime_update)
	CONSTRAINT unique_constraint UNIQUE(full_repo_name, path, utc_datetime_update)
);

CREATE TABLE IF NOT EXISTS clones (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	full_repo_name VARCHAR(256) NOT NULL,
	timestamp VARCHAR(32) NOT NULL,
	count INT NOT NULL,
	uniques INT NOT NULL,
	utc_datetime_update VARCHAR(32) NOT NULL,
	-- UNIQUE(full_repo_name, timestamp)
	CONSTRAINT unique_constraint UNIQUE(full_repo_name, timestamp)
);

CREATE TABLE IF NOT EXISTS views (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	full_repo_name VARCHAR(256) NOT NULL,
	timestamp VARCHAR(32) NOT NULL,
	count INT NOT NULL,
	uniques INT NOT NULL,
	utc_datetime_update VARCHAR(32) NOT NULL,
	-- UNIQUE(full_repo_name, timestamp)
	CONSTRAINT unique_constraint UNIQUE(full_repo_name, timestamp)
);