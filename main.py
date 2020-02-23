from datetime import datetime
from GithubTraffic import GithubTraffic
from JsonHandler import JsonHandler

def main():
	save_stats_directory = 'save_stats/'
	json_filename = 'stats-{}.json'.format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

	json_handler = JsonHandler(save_stats_directory + json_filename)
	github_traffic = GithubTraffic(json_handler)
	github_traffic.run()

if __name__ == '__main__':
	main()
