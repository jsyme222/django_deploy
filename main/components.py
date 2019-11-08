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
	:param directory: str()
	:return django_dir: bool()
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
	:param root: str()
	:return env: str()
	"""
	temp = root.split('/')
	env = '/'.join(temp[:-1])
	env += '/.env'

	return env


class Collector:

	def __init__(self, file):
		self.errors = {}

		if not os.path.isfile(file):
			self.errors['file_error'] = f'Template not found at {file}'
		else:
			self.file_path = file
			with open(file, 'r') as f:
				self.file = f.read()

	def pull_vars(self):
		payload = []
		var_pattern = re.compile('(\\{[\$].*?\\})', re.IGNORECASE | re.DOTALL)
		variables = var_pattern.findall(self.file)

		if len(variables) <= 1:
			self.errors['File Format'] = 'File not formatted'

		for var in variables:
			case = var[3:-2]
			case = tuple(case.split(', '))
			prompt, required, default = case[0], case[1], case[2]
			payload.append((prompt, required, default))

		return payload

	def inputs(self, output=True):
		"""
		Takes in a file pre-formatted with {$ variable, required, default_value }
		symbols. Returns a payload dict() using {'variable': response} formatting.
		dict(added_functions) includes {SYSTEM_CALL : function} to aquire default value.
		:param added_functions: dict(optional)
		:return payload: dict()
		"""

		def send_payload(payload):
			if not self.errors:
				return payload
			else:
				return self.errors

		def read_from_file(added_functions={}):
			payload = {}

			SYSTEM_CALLS = {
				'$USER': os.getlogin(),
				'$PWD': os.getcwd(),
				'$ENV_DIR': default_env_dir(os.getcwd()),
				'$SOCK_DIR': os.getcwd() + '/' + os.getcwd().split('/')[-1] + '.sock',
				'$PROJECT_NAME': os.getcwd().split('/')[-1],
			}

			if len(added_functions.keys()) >= 1:
				SYSTEM_CALLS.update(added_functions)

			for case in self.pull_vars():
				prompt, required, default = case[0], case[1], case[2]
				if default.startswith('$'):
					default = SYSTEM_CALLS[default]

				if prompt not in payload.keys():
					if required != 'True':
						user_input = input(f'{prompt}\n[{default}] : ')
						if user_input == '':
							user_input = default
					else:
						user_input = input(f'{prompt} : ')
						while user_input == '':
							user_input = input(f'{prompt} : ')

					payload[prompt] = user_input

			return payload

		if len(self.errors.keys()) == 0:
			reading = read_from_file()
			if reading and output:
				self.outputs(reading, self.file_path)


	def outputs(self, data, file):
		"""
		Takes data as dict() and writes to file based upon
		which template is passed.
		:param data: dict()
		:return:
		"""

		filename = file.split('/')[-1]
		write_file = f'./new_{filename}'
		print(data)
		print(write_file)