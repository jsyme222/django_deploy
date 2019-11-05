#!/user/bin python3.7
import os


def center(text, width=80, delim="-", end="\n"):
	"""
	Center multiple line 'text' with 'delim' padding
	"""
	lines = text.split('\n')
	for line in lines:
		print(line.center(width, delim) + end)


def check_django_dir(directory):
	scan_files = os.scandir(directory)
	files = [x.name for x in scan_files]
	django_dir = True
	if 'manage.py' not in files:
		django_dir = False

	return django_dir


def default_env_dir(root):
	temp = root.split('/')
	env = '/'.join(temp[:-1])
	env += '/.env'

	return env


class Collect:
	"""
	Collect information from any number of
	user inputs and stores their values
	within a dict() at return.
	"""

	def inputs(obs):
		#  Takes a list() of prompts and
		#  returns a dict() of 'reponses'
		payload = {}
		for case in obs:
			prompt, require, default = case[0], case[1], case[2]
			i = input(prompt)
			if require:
				while i == '':
					i = input(prompt)
			elif i is '' and not require:
				i = default
			payload[prompt] = i

		print(payload)
		return payload
