from datetime import datetime
from GithubTraffic import GithubTraffic
from JsonHandler import JsonHandler

def main():
	# Consistent timestamp across the whole run
	current_utc_datetime = datetime.utcnow()
	datetime_format = '%Y-%m-%dT%H:%M:%SZ'

	save_stats_directory = 'save_stats/'
	json_filename = 'stats-{}.json'.format(current_utc_datetime.strftime(datetime_format))

	json_handler = JsonHandler(save_stats_directory + json_filename)
	github_traffic = GithubTraffic(json_handler, current_utc_datetime, datetime_format)
	github_traffic.run()

if __name__ == '__main__':
	main()
