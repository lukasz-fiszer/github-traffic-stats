import json

class JsonHandler:

	def __init__(self, save_filepath, json_indent=4):
		self.save_filepath = save_filepath
		self.json_indent = json_indent

	def handle(self, totals_table, referrers_table, paths_table, clones_table, views_table):
		data = {
			'totals': totals_table,
			'referrers': referrers_table,
			'paths': paths_table,
			'clones': clones_table,
			'views': views_table
		}

		with open(self.save_filepath, 'w+') as file:
			json.dump(data, file, indent=self.json_indent)
