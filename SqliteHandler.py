import json
import sqlite3

class SqliteHandler:

	def __init__(self, db_filepath, db_backup_directory):
		self.db_filepath = db_filepath
		self.db_backup_directory = db_backup_directory
		self.connection = self.get_connection(db_filepath)

	def get_connection(self, db_filepath):
		return sqlite3.connect(db_filepath)

	def handle(self, totals_table, referrers_table, paths_table, clones_table, views_table):
		print('Sqlite handler: database {}, backup {}'.format(self.db_filepath, self.db_backup_directory), flush=True)

		self.create_schema_if_not_exists()


		self.insert_totals(totals_table)
		self.insert_referrers(referrers_table)
		self.insert_paths(paths_table)
		self.insert_clones(clones_table)
		self.insert_views(views_table)

		self.connection.commit()
		self.connection.close()
		

	def insert_totals(self, totals):
		params = [list(total.values()) * 2 for total in totals]
		self.query_from_file('sql/insert-totals.sql', params, execute_many=True)

	def insert_referrers(self, referrers):
		params = [list(referrer.values()) * 2 for referrer in referrers]
		self.query_from_file('sql/insert-referrers.sql', params, execute_many=True)

	def insert_paths(self, paths):
		params = [list(path.values()) * 2 for path in paths]
		self.query_from_file('sql/insert-paths.sql', params, execute_many=True)

	def insert_clones(self, clones):
		params = [list(clone.values()) * 2 + [clone['utc_datetime_update']] for clone in clones]
		self.query_from_file('sql/insert-clones.sql', params, execute_many=True)

	def insert_views(self, views):
		params = [list(view.values()) * 2 + [view['utc_datetime_update']] for view in views]
		self.query_from_file('sql/insert-views.sql', params, execute_many=True)


	def create_schema_if_not_exists(self):
		with open('sql/create-schema.sql', 'r') as file:
			schema_query = file.read()

		self.query(schema_query, execute_script=True, commit=True)

	def query_from_file(self, filepath, params=(), execute_many=False, commit=False):
		with open(filepath, 'r') as file:
			query = file.read()

		cursor = self.connection.cursor()
		if execute_many:
			cursor.executemany(query, params)
		else:
			cursor.execute(query, params)
		results = cursor.fetchall()
		cursor.close()
		if commit:
			self.connect.commit()
		return results

	def query(self, query, params=(), execute_script=False, commit=False):
		cursor = self.connection.cursor()
		if execute_script:
			cursor.executescript(query)
		else:
			cursor.execute(query, params)
		results = cursor.fetchall()
		cursor.close()
		if commit:
			self.connection.commit()
		return results