#!/usr/bin/python3
import os
import subprocess

import classes


def gunicorn():

	classes.center('Gunicorn Configuration', delim=' ')
	file = os.path.join(
		classes.FILE_DIR,
		'file_templates/gunicorn/gunicorn.service'
	)
	default_location = '/etc/systemd/system/gunicorn.service'

	g = classes.Collector(file)
	data = g.inputs(output_file=False)

	return g, data, default_location


def nginx():

	classes.center('Nginx Configuration', delim=' ')
	file = os.path.join(
		classes.FILE_DIR,
		'file_templates/nginx/sites-available/sites-available'
	)

	n = classes.Collector(file)
	data = n.inputs(output_file=False)

	default_location = f'/etc/nginx/sites-available/{data["project_name"]}'
	return n, data, default_location


def run(*args):

	output_list = []

	for arg in args:
		obj, data, location = arg()
		prompt = f'location\n[{location}]'
		output_to = input(prompt)

		if output_to == '':
			output_to = location

		out = obj.outputs(data, output_to)
		output_list.append(out)

		if arg == args[-1]:

			link_sites_available = [
				'ln',
				'-s',
				f'/etc/nginx/sites-available/{data["project_name"]}',
				'/etc/nginx/sites-enabled',
			]
			nginx_restart = [
				'sudo',
				'systemctl',
				'start',
				'nginx',
			]
			subprocess.run(link_sites_available)
			subprocess.run(nginx_restart)

	return output_list


if __name__ == '__main__':

	if not classes.check_django_dir(classes.ROOT_DIR):  # Check for 'manage.py' in cwd
		classes.center(
			f'The current directory\n{classes.ROOT_DIR}\nDoes not contain a \'manage.py\' file.\nContinue?\n ',
			delim=" ",
			end="",
		)
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()

	run(gunicorn, nginx)
