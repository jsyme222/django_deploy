#!/user/bin python3.7
import os
import re


def center(text, width=80, delim="-", end="\n"):
	"""
	Text align and decoration for terminal display
	:param text: {str}
	:param width: {int}
	:param delim: {str}
	:param end: {str}
	:return:
	"""
	lines = text.split('\n')
	for line in lines:
		print(line.center(width, delim) + end)


def check_django_dir(directory):
	"""
	Checks for a 'manage.py' file to verify base directory
	of a django project
	:param directory: {str}
	:return django_dir: {bool}
	"""
	scan_files = os.scandir(directory)
	files = [x.name for x in scan_files]
	django_dir = True
	if 'manage.py' not in files:
		django_dir = False

	return django_dir


def default_env_dir(root):
	"""
	Builds a default directory for the virtual
	environment based off of the 'root' base_dir
	:param root: {str}
	:return env: {str}
	"""
	temp = root.split('/')
	env = '/'.join(temp[:-1])
	env += '/.env'

	return env


class Collect:

	def inputs(formatted_file):
		"""
		Takes in a file pre-formatted with { variable } placement.
		Returns a payload dict() using 'variable': response formatting.
		:param formatted_file: {str: directory}
		:return payload: {dict}
		"""

		payload = {}
		errors = {}

		def send_payload():
			if not errors:
				return payload
			else:
				return errors

		if not os.path.isfile(formatted_file):
			errors['file_error'] = f'Template not found at {formatted_file}'
			send_payload()

		with open(formatted_file, 'r') as f:
			opened_file = f.read()

		var_pattern = re.compile('(\\{[\$].*?\\})', re.IGNORECASE | re.DOTALL)
		variables = var_pattern.findall(opened_file)

		for var in variables:
			case = var[3:-2]
			case = tuple(case.split(', '))
			prompt, required, default = case[0], bool(case[1]), case[2]
			user_input = input(prompt)
			if required:
				while user_input == '':
					user_input = input(f'{prompt}\n[{default}] : ')
			elif not required and user_input == '':
				user_input = default
			payload[prompt] = user_input

		print(payload)
		return payload
