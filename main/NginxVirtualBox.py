#!/user/bin python3.7
import os
from . import components as comp


class NginxVirtualBox:
	"""
	Creates an Nginx virtual box that
	will host the django project.
	"""

	def __init__(self, info):
		self.info = info

	def create_sites_available(self, info):

		def read_template():
			real_path = os.path.dirname(__file__)

			template = f'{real_path}/file_templates/nginx/sites-available/*template*'
			if not os.path.isfile(template):
					print('\n')
					comp.center(f' ERROR \n Template not found at \n \'{template}\'')
					exit()
			else:
				with open(template, 'r') as temp:
					temp = temp.read()
				return temp

		def create_sites_available(project_info):  # Parses and creates file
			file = read_template()
			comp.center('Parsing sites-available file', delim=" ")
			for key in project_info.keys():
				file = file.replace('{ ' + key + ' }', project_info[key])

			file_dir = f'/etc/nginx/sites-available/{project_info["project_name"]}'
			comp.center(f'Writing file to {file_dir}', delim=" ")
			# with open(file_dir, 'w+') as f:
			# 	comp.center('Creating sites-available for project')
			# 	f.write(file)

			return True

		return create_sites_available(self.info)

	def run(self):
		intro = 'Nginx Service Setup'
		print('\n')
		comp.center(intro)

		file = self.create_sites_available(self.info)

		if not file:
			comp.center(' ERROR \n Something went wrong \n', delim="x")
		else:
			comp.center(' Nginx setup \n COMPLETE ', delim=" ")
