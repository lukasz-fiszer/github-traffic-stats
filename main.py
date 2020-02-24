from datetime import datetime
from GithubTraffic import GithubTraffic
from JsonHandler import JsonHandler
from SqliteHandler import SqliteHandler
from CompositeHandler import CompositeHandler

def main():
	# Consistent timestamp across the whole run
	current_utc_datetime = datetime.utcnow()
	datetime_format = '%Y-%m-%dT%H:%M:%SZ'

	save_stats_directory = 'save_stats/'
	json_filename = 'stats-{}.json'.format(current_utc_datetime.strftime(datetime_format))
	db_filename = 'github-traffic-stats-history.sqlite'
	db_backup_directory = 'db_backup/'

	json_handler = JsonHandler(save_stats_directory + json_filename)
	sqlite_handler = SqliteHandler(save_stats_directory + db_filename, db_backup_directory)
	composite_handler = CompositeHandler([json_handler, sqlite_handler])

	github_traffic = GithubTraffic(composite_handler, current_utc_datetime, datetime_format)
	github_traffic.run()

if __name__ == '__main__':
	main()
