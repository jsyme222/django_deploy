#!/user/bin python3.7
import classes


def run_gunicorn():  # TODO Docstring

	classes.center('Beginning Gunicorn Configuration', delim=' ')
	file = './file_templates/gunicorn/gunicorn.service'
	#  default_location = '/etc/systemd/system/gunicorn.service'
	default_location = './NEW-GUNICORN.SERVICE'

	g = classes.Collector(file)
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


def run_nginx(): # TODO Docstring

	classes.center('Beginning Nginx Configuration', delim=' ')
	file = './file_templates/nginx/sites-available/*template*'
	#  default_location = '/etc/nginx/sites-available/{}'
	default_location = './NEW-{}'

	n = classes.Collector(file)
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

	if not classes.check_django_dir(classes.ROOT_DIR):  # Check for 'manage.py' in cwd
		classes.center(
			f'The current directory\n{classes.ROOT_DIR}\nDoes not contain a \'manage.py\' file.\nContinue?\n ',
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
