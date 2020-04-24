import os
import datetime
import json
import sqlite3

class FrontendDataExtractor:

	def __init__(self, db_filepath, datajs_filepath):
		self.db_filepath = db_filepath
		self.datajs_filepath = datajs_filepath

		filesplit = os.path.splitext(datajs_filepath)
		self.datajson_filepath = filesplit[0] + '.json'
		self.repostatsjs = 'frontend/repo-stats.js'

		self.connection = self.get_connection(db_filepath)
		self.connection.row_factory = sqlite3.Row

		self.datetime_format = '%Y-%m-%dT%H:%M:%SZ'

	def get_connection(self, db_filepath):
		return sqlite3.connect(db_filepath)

	def extract_db_data_to_datajs(self):
		print('Frontend data extractor, db filepath: {}'.format(self.db_filepath))
		print('Data js: {}, json: {}'.format(self.datajs_filepath, self.datajson_filepath))

		current_utc_datetime = datetime.datetime.utcnow()
		datetime_string = current_utc_datetime.strftime(self.datetime_format)
		print('Current utc datetime: ' + datetime_string)


		global views

		repo_names = self.run_query('SELECT full_repo_name FROM totals GROUP BY full_repo_name')
		repo_names_list = list(map(lambda x: x['full_repo_name'], repo_names))

		totals = self.run_query('SELECT * FROM totals ORDER BY utc_datetime_update')
		referrers = self.run_query('SELECT * FROM referrers ORDER BY utc_datetime_update')
		paths = self.run_query('SELECT * FROM paths ORDER BY utc_datetime_update')
		clones = self.run_query('SELECT * FROM clones ORDER BY timestamp')
		views = self.run_query('SELECT * FROM views ORDER BY timestamp')

		default_clone = {
			'id': None,
			'full_repo_name': None,
			'timestamp': None,
			'count': 0,
			'uniques': 0,
			'utc_datetime_update': datetime_string
		}

		default_view = {
			'id': None,
			'full_repo_name': None,
			'timestamp': None,
			'count': 0,
			'uniques': 0,
			'utc_datetime_update': datetime_string
		}

		# clones = self.fill_dates(clones, default_clone, 'timestamp', 'full_repo_name')
		# views = self.fill_dates(views, default_view, 'timestamp', 'full_repo_name')

		data = {
			'utc_datetime': datetime_string,
			'repo_names': repo_names_list,
			'totals': totals,
			'referrers': referrers,
			'paths': paths,
			'clones': clones,
			'views': views
		}


		with open(self.datajson_filepath, 'w') as json_file:
			json.dump(data, json_file, indent=4)

		data_json = json.dumps(data, indent=4)
		with open(self.datajs_filepath, 'w') as js_file:
			print('let extractedData = {};'.format(data_json), file=js_file)


		repo_stats = self.build_repo_stats(data)

		with open(self.repostatsjs, 'w') as repo_stats_file:
			print('let repoStats = {};'.format(json.dumps(repo_stats, indent=4)), file=repo_stats_file)

		return data


	def run_query(self, query):
		cursor = self.connection.cursor()
		res = cursor.execute(query)
		fetchall = res.fetchall()
		cursor.close()
		rows = [None] * len(fetchall)
		for i, r in enumerate(fetchall):
			rows[i] = dict(r)
		return rows

	def fill_dates(self, entries, default, datetime_column, copy_column):
		copy_column_set = set(map(lambda x: x[copy_column], entries))

	def date_from_datetime(self, datetime_obj):
		datepart = datetime.datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day)
		return datepart

	def adjust_datetime_string(self, datetime_string):
		datetime_obj = datetime.datetime.strptime(datetime_string, self.datetime_format)
		date = self.date_from_datetime(datetime_obj)
		return date.strftime(self.datetime_format)

	def build_repo_stats(self, data):
		last_update = max(map(lambda x: x['utc_datetime_update'], data['totals']))
		last_update_date = self.adjust_datetime_string(last_update)

		repos = dict()
		repos['utc_datetime'] = data['utc_datetime']
		repos['last_update'] = last_update
		repos['repos'] = dict()

		for reponame in data['repo_names']:
			repo_totals = list(filter(lambda x: x['full_repo_name'] == reponame, data['totals']))
			last_views = list(filter(lambda x: x['type'] == 'views', repo_totals))[-1]
			last_clones = list(filter(lambda x: x['type'] == 'clones', repo_totals))[-1]

			repo_clones = list(filter(lambda x: x['full_repo_name'] == reponame, data['clones']))
			repo_views = list(filter(lambda x: x['full_repo_name'] == reponame, data['views']))

			first_update = min(map(lambda x: x['utc_datetime_update'], repo_totals))
			first_clones = min(map(lambda x: x['timestamp'], repo_clones), default=first_update)
			first_views = min(map(lambda x: x['timestamp'], repo_views), default=first_update)
			first_datetime = min(first_update, first_clones, first_views)
			first_update_date = self.adjust_datetime_string(first_datetime)


			def fill_dates(entries):
				new_entries = []
				timedelta = datetime.timedelta(days=1)
				start = datetime.datetime.strptime(first_update_date, self.datetime_format)
				end = datetime.datetime.strptime(last_update_date, self.datetime_format)

				def build_entry(timestamp):
					return {
						'id': None,
						'full_repo_name': reponame,
						'timestamp': timestamp,
						'count': 0,
						'uniques': 0,
						'utc_datetime_update': data['utc_datetime']
					}

				current = start
				i = 0
				while current <= end:
					if i >= len(entries):
						new_entries.append(build_entry(current.strftime(self.datetime_format)))
						current += timedelta
						continue

					if current.strftime(self.datetime_format) == entries[i]['timestamp']:
						new_entries.append(entries[i])
						current += timedelta
						i += 1
						continue

					new_entries.append(build_entry(current.strftime(self.datetime_format)))
					current += timedelta

				return new_entries


			repo_clones_filled = fill_dates(repo_clones)
			repo_views_filled = fill_dates(repo_views)

			repos['repos'][reponame] = {
				'last_totals_views': last_views,
				'last_totals_clones': last_clones,
				'clones': repo_clones_filled,
				'views': repo_views_filled
			}


		return repos



if __name__ == '__main__':

	db_filepath = 'save_stats/github-traffic-stats-history.sqlite'
	datajs_filepath = 'frontend/extracted-data.js'

	extractor = FrontendDataExtractor(db_filepath, datajs_filepath)
	extractor.extract_db_data_to_datajs()
	