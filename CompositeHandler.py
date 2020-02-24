class CompositeHandler:

	def __init__(self, handlers):
		self.handlers = handlers

	def handle(self, totals_table, referrers_table, paths_table, clones_table, views_table):
		for handler in self.handlers:
			handler.handle(totals_table, referrers_table, paths_table, clones_table, views_table)