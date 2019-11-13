#!/user/bin python3.7
import os
import subprocess

import classes


def setup_gunicorn():  # TODO Docstring

	name = 'gunicorn'
	classes.center('Beginning Gunicorn Configuration', delim=' ')
	file = os.path.join(
		classes.FILE_DIR,
		'file_templates/gunicorn/gunicorn.service'
	)
	default_location = '/etc/systemd/system/gunicorn.service'

	g = classes.Collector(file)
	data = g.inputs(output_file=False)

	return g, name, data, default_location


def setup_nginx():  # TODO Docstring

	name = 'nginx'
	classes.center('Beginning Nginx Configuration', delim=' ')
	file = os.path.join(
		classes.FILE_DIR,
		'file_templates/nginx/sites-available/sites-available'
	)

	n = classes.Collector(file)
	data = n.inputs(output_file=False)

	default_location = f'/etc/nginx/sites-available/{data["project_name"]}'
	print(default_location)
	return n, name, data, default_location


def run(*args):
	outputs = []
	for arg in args:
		obj, name, data, location = arg

		if not data:
			raise Exception('Error getting file inputs')
		default_location = location
		prompt = f'location\n[{default_location}]'
		output_to = input(prompt)

		if output_to == '':
			output_to = default_location

		output = obj.outputs(data, output_to)

		if name == 'nginx':
			project = data['project_name']
			link = subprocess.run(
				[
					'ln',
					'-s',
					f'/etc/nginx/sites-available/{project}',
					'/etc/nginx/sites-enabled'
				]
			)
			if not link:
				raise Exception('Unable to link sites-available')

		outputs.append(output)

	return outputs


def main():

	if not classes.check_django_dir(classes.ROOT_DIR):  # Check for 'manage.py' in cwd
		classes.center(
			f'The current directory\n{classes.ROOT_DIR}\nDoes not contain a \'manage.py\' file.\nContinue?\n ',
			delim=" ",
			end="",
		)
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()

	run(setup_gunicorn(), setup_nginx())


if __name__ == '__main__':
	main()
