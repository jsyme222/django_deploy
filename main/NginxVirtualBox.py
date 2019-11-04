#!/user/bin python3.7
import os


class NginxVirtualBox:
	"""
	Creates an Nginx virtual box that
	will host the django project.
	"""

	def __init__(self, info):
		self.info = info
		intro = 'Nginx Service Setup'
		print('\n')
		print(intro)

	def create_sites_available(self, info):

		def read_template():
			real_path = os.path.dirname(__file__)

			template = f'{real_path}/file_templates/nginx/sites-available/*template*'
			if not os.path.isfile(template):
					print('\n')
					print('ERROR')
					print('Template not found')
					exit()
			else:
				with open(template, 'r') as temp:
					temp = temp.read()
				return temp

		def create_sites_available(project_info):  # Parses and creates file
			file = read_template()
			print('Parsing File')
			for key in project_info.keys():
				file = file.replace('{ ' + key + ' }', project_info[key])

			file_dir = f'/etc/nginx/sites-available/{project_info["project_name"]}'
			print(f'Writing file to {file_dir}')
			with open(file_dir, 'w+') as f:
				print('Creating sites-available for project')
				f.write(file)

			return True

		return create_sites_available(self.info)

	def run(self):

		file = self.create_sites_available(self.info)

		if not file:
			print('Something went wrong')
		else:
			print('Created sites-available')
