#!/usr/bin python3.7
import os
from unittest import TestCase, main
from components import Collector


class TestCollector(TestCase):
	"""Testing functionality of the Collector class.
	Takes in 'file' as a directory path to the file
	to be parsed and collected via the
	inputs() : method
	File written with collected values via the
	outputs() : method
	"""

	def setUp(self):
		"""
		Creates two(2) instances of the Collector class from test files
		stored within the tests directory.
		"""

		gunicorn_file = './file_templates/template-gunicorn.service'  # Gunicorn test file
		self.gunicorn_collector = Collector(gunicorn_file)

		nginx_file = './file_templates/template-sites-available'  # Nginx test files
		self.nginx_collector = Collector(nginx_file)

		false_file = '/file/that/does/not/exist'
		self.false_collector = Collector(false_file)

		no_format = './file_templates/no-format.txt'
		self.no_format = Collector(no_format)

	def test_pull_vars(self):
		"""
		Tests the values returned from the pull_vars() method
		on 2 pre-determined files. Tests values against constants
		pulled from the files
		"""

		nginx_vars = self.nginx_collector.pull_vars(raw=True)
		nginx_vars_constant = [
			'{$ project_name, False, $PROJECT_NAME }',
			'{$ port, False, 80 }',
			'{$ domains, True, None }',
			'{$ root_dir, False, $PWD }',
			'{$ sock_path, False, $SOCK_DIR }'
		]

		gunicorn_vars = self.gunicorn_collector.pull_vars(raw=True)
		gunicorn_vars_constant = [
			'{$ user, False, $USER }',
			'{$ group, False, www-data }',
			'{$ root_dir, False, $PWD }',
			'{$ path_to_env, False, $ENV_DIR }',
			'{$ sock_path, False, $SOCK_DIR }',
			'{$ project_name, False, $PROJECT_NAME }'
		]

		self.assertListEqual(nginx_vars, nginx_vars_constant)
		self.assertListEqual(gunicorn_vars, gunicorn_vars_constant)
		self.assertRaises(TypeError, self.no_format.pull_vars)  # Test file with no formatting

	def test_outputs(self) -> None:

		nginx_inputs_constants = {
			'project_name': 'django_deploy',
			'port': '80',
			'domains': 'domain.com www.domain.com',
			'root_dir': '/home/jsyme/projects/pycharm/django_deploy',
			'sock_path': '/home/jsyme/projects/pycharm/django_deploy/django_deploy.sock'
		}

		gunicorn_inputs_constants = {
			'user': 'jsyme',
			'group': 'www-data',
			'root_dir': '/home/jsyme/projects/pycharm/django_deploy',
			'path_to_env': '/home/jsyme/projects/pycharm/.env/',
			'sock_path': '/home/jsyme/projects/pycharm/django_deploy/django_deploy.sock',
			'project_name': 'django_deploy'
		}

		g = self.gunicorn_collector.outputs(gunicorn_inputs_constants)
		n = self.nginx_collector.outputs(nginx_inputs_constants)
		exists = self.nginx_collector.outputs(nginx_inputs_constants, './file_templates/no-format.txt')
		#  Test when file exists

		self.assertEqual(g, True)
		self.assertEqual(n, True)
		self.assertFalse(exists)

	def tearDown(self) -> None:

		g_file = './new-template-gunicorn.service'
		n_file = './new-template-sites-available'

		while os.path.isfile(g_file) or os.path.isfile(n_file):
			os.remove(g_file)
			print(f'{g_file} removed')
			os.remove(n_file)
			print(f'{n_file} removed')


if __name__ == '__main__':
	main()
