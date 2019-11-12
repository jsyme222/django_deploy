#!/user/bin python3.7
import os
import subprocess
import sys
from main.components import Collector, check_django_dir, center


ROOT_DIR = os.getcwd()


def run_gunicorn():

	center('Beginning Gunicorn Configuration', delim=' ')
	file = './main/file_templates/gunicorn/gunicorn.service'
	#  self.default_location = '/etc/systemd/system/gunicorn.service'
	default_location = './NEW-GUNICORN.SERVICE'

	g = Collector(file)
	data = g.inputs(output_file=False)
	if not data:
		return False
	else:
		environment = data['path_to_env']
		prompt = f'location\n[{default_location}]'
		output_to = input(prompt)

		if output_to == '':
			output_to = default_location

		output = g.outputs(data, output_to)
		if not output:
			return False
		else:
			return environment


def run_nginx():

	center('Beginning Nginx Configuration', delim=' ')
	file = './main/file_templates/nginx/sites-available/*template*'
	#  self.default_location = '/etc/nginx/sites-available/{}'
	default_location = './NEW-{}'

	n = Collector(file)
	data = n.inputs(output_file=False)

	if not data:
		return False
	else:
		default_location = default_location.format(data['project_name'])
		prompt = f'location\n[{default_location}]'
		output_to = input(prompt)

		if output_to == '':
			output_to = default_location

		output = n.outputs(data, output_to)
		return output


def main():

	if not check_django_dir(ROOT_DIR):  # Check for 'manage.py' in cwd
		center(
			f'The current directory\n{ROOT_DIR}\nDoes not contain a \'manage.py\' file.\nContinue?\n ',
			delim=" ",
			end="",
		)
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()

	run_gunicorn()
	run_nginx()


if __name__ == '__main__':
	main()
