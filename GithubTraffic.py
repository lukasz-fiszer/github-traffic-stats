import json
from datetime import datetime
from github import Github

class GithubTraffic:

	def __init__(self, data_handler, utc_datetime, datetime_format):
		self.config = self.get_json_config()
		self.connector = self.get_github_connector()
		self.data_handler = data_handler
		self.utc_datetime = utc_datetime
		self.datetime_format = datetime_format

	def get_json_config(self, filepath='config.json'):
		with open(filepath, 'r') as file:
			return json.load(file)

	def get_github_connector(self):
		return Github(self.config['github-token'])

	@staticmethod
	def build_totals_row(repo_name, type, count, uniques, utc_datetime_update):
		return {
			'full_repo_name': repo_name,
			'type': type,
			'count': count,
			'uniques': uniques,
			'utc_datetime_update': utc_datetime_update
		}

	@staticmethod
	def build_referrers_row(repo_name, referrer, count, uniques, utc_datetime_update):
		return {
			'full_repo_name': repo_name,
			'referrer': referrer,
			'count': count,
			'uniques': uniques,
			'utc_datetime_update': utc_datetime_update
		}

	@staticmethod
	def build_paths_row(repo_name, path, title, count, uniques, utc_datetime_update):
		return {
			'full_repo_name': repo_name,
			'path': path,
			'title': title,
			'count': count,
			'uniques': uniques,
			'utc_datetime_update': utc_datetime_update
		}

	@staticmethod
	def build_clones_row(repo_name, timestamp, count, uniques, utc_datetime_update):
		return {
			'full_repo_name': repo_name,
			'timestamp': timestamp,
			'count': count,
			'uniques': uniques,
			'utc_datetime_update': utc_datetime_update
		}

	@staticmethod
	def build_views_row(repo_name, timestamp, count, uniques, utc_datetime_update):
		return {
			'full_repo_name': repo_name,
			'timestamp': timestamp,
			'count': count,
			'uniques': uniques,
			'utc_datetime_update': utc_datetime_update
		}

	def run(self):
		current_datetime = self.utc_datetime
		current_datetime_string = self.utc_datetime.strftime(self.datetime_format)

		print('Running')
		print('Current utc datetime: ' + current_datetime_string)

		totals_table = []
		referrers_table = []
		paths_table = []
		clones_table = []
		views_table = []

		repos = [repo for repo in self.connector.get_user().get_repos() if repo.owner.login == self.config['github-user']]

		print('Repos count: {}'.format(len(repos)))

		for repo in repos:
			print('Repo: ' + repo.full_name)
			name = repo.full_name
			referrers = repo.get_top_referrers()
			paths = repo.get_top_paths()
			clones = repo.get_clones_traffic()
			views = repo.get_views_traffic()

			totals_table.append(self.build_totals_row(name, 'clones', clones['count'], clones['uniques'], current_datetime_string))
			totals_table.append(self.build_totals_row(name, 'views', views['count'], views['uniques'], current_datetime_string))

			for referrer in referrers:
				referrers_table.append(self.build_referrers_row(name, referrer.referrer, referrer.count, referrer.uniques, current_datetime_string))

			for path in paths:
				paths_table.append(self.build_paths_row(name, path.path, path.title, path.count, path.uniques, current_datetime_string))

			for clone in clones['clones']:
				clones_table.append(self.build_clones_row(name, clone.timestamp.strftime(self.datetime_format), clone.count, clone.uniques, current_datetime_string))

			for view in views['views']:
				views_table.append(self.build_views_row(name, view.timestamp.strftime(self.datetime_format), view.count, view.uniques, current_datetime_string))

			print('\tClones {}, unique {}'.format(clones['count'], clones['uniques']))
			print('\tViews {}, unique {}'.format(views['count'], views['uniques']))


		print('Repos data downloaded')
		print('Time taken: ' + str(datetime.utcnow() - current_datetime))

		print('Repos count: {}'.format(len(repos)))

		print('Table entries stats:')
		print('\tTotals count: {}'.format(len(totals_table)))
		print('\tReferrers count: {}'.format(len(referrers_table)))
		print('\tPaths count: {}'.format(len(paths_table)))
		print('\tClones count: {}'.format(len(clones_table)))
		print('\tViews count: {}'.format(len(views_table)))

		print('Total clone and visit stats:')
		sum_clones = sum(total['count'] for total in totals_table if total['type'] == 'clones')
		sum_clones_uniques = sum(total['uniques'] for total in totals_table if total['type'] == 'clones')
		sum_views = sum(total['count'] for total in totals_table if total['type'] == 'views')
		sum_views_uniques = sum(total['uniques'] for total in totals_table if total['type'] == 'views')
		print('\tSum clones {}, uniques {}'.format(sum_clones, sum_clones_uniques))
		print('\tSum views {}, uniques {}'.format(sum_views, sum_views_uniques))



		self.data_handler.handle(totals_table, referrers_table, paths_table, clones_table, views_table)
		
		print('Repos data handled')
		print('Time taken (in total): ' + str(datetime.utcnow() - current_datetime))


