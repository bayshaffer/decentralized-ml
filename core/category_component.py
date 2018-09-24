""" import Blockchain** as bc"""
import pandas as pd

class CategoryComponent(object):
	"""
	CategoryComponent

	- 
	""" 
	def __init__(self, DBClient):
		"""
		Initialize CategoryComponent instance.

		@param DBClient obj DBClient: object to be used for querying
		"""
		self.DBClient = DBClient

    def get_ed_with_category(self, category):
		"""
		Return ED for each data provider with the given category.

		@param str category: name of the data category of interest
		@return dict: a dictionary with status and Error (str) or Directory with data providers ED
		"""
		try:
			data_providers_df = self.DBClient._get_data_providers_with_category(category)
		except Exception as e:
			return {'Success': False, 'Error': e}
		if data_providers_df.empty: 
			return {'Success': False, 'Error': 'Category: {} has no data providers.'.format(category)}
		return {'Success': True, 'Directory': bc.get_data_providers_ED(data_providers_df)}




