#!/usr/bin python3.7
import os
from unittest import TestCase, main

import classes


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

		self.test_dir = os.path.join(classes.FILE_DIR, 'test_file_templates')

		gunicorn_file = os.path.join(
			self.test_dir,
			'template-gunicorn.service'  # Gunicorn test file
		)
		self.gunicorn_collector = classes.Collector(gunicorn_file)

		nginx_file = os.path.join(
			self.test_dir,
			'template-sites-available'  # Nginx test files
		)
		self.nginx_collector = classes.Collector(nginx_file)

		false_file = '/file/that/does/not/exist'
		self.false_collector = classes.Collector(false_file)

		no_format = os.path.join(
			self.test_dir,
			'no-format.txt',
		)
		self.no_format = classes.Collector(no_format)

	def test_pull_vars(self):
		"""
		Tests the values returned from the pull_vars() method
		on 2 pre-determined files. Tests values against constants
		pulled from the files
		"""

		nginx_vars = self.nginx_collector.pull_vars(raw=True)
		nginx_vars_constant = [
			#'{$ project_name, $PROJECT_NAME }',
			'{$ port, 80 }',
			'{$ domains, None, True }',
			'{$ root_dir, $PWD }',
			'{$ sock_path, $SOCK_DIR }'
		]

		gunicorn_vars = self.gunicorn_collector.pull_vars(raw=True)
		gunicorn_vars_constant = [
			'{$ user, $USER }',
			'{$ group, www-data }',
			'{$ root_dir, $PWD }',
			'{$ path_to_env, $ENV_DIR }',
			'{$ sock_path, $SOCK_DIR }',
			'{$ project_name, $PROJECT_NAME }'
		]

		self.assertListEqual(nginx_vars, nginx_vars_constant)
		self.assertListEqual(gunicorn_vars, gunicorn_vars_constant)
		self.assertRaises(TypeError, self.no_format.pull_vars)  # Test file with no formatting

	def test_outputs(self) -> None:

		user = os.getlogin()

		nginx_inputs_constants = {
			'project_name': 'Project_Name',
			'port': '80',
			'domains': 'domain.com www.domain.com',
			'root_dir': self.test_dir,
			'sock_path': f'/home/jsyme/projects/pycharm/django_deploy/django_deploy.sock'
		}

		gunicorn_inputs_constants = {
			'user': user,
			'group': 'www-data',
			'root_dir': self.test_dir,
			'path_to_env': classes.default_env_dir(self.test_dir),
			'sock_path': f'/home/jsyme/projects/pycharm/django_deploy/django_deploy.sock',
			'project_name': 'django_deploy'
		}
		print(gunicorn_inputs_constants)

		g = self.gunicorn_collector.outputs(gunicorn_inputs_constants, os.path.join(self.test_dir, 'new-template-gunicorn.service')
)
		n = self.nginx_collector.outputs(nginx_inputs_constants, os.path.join(self.test_dir, 'new-sites-available'))
		exists = self.nginx_collector.outputs(
			nginx_inputs_constants,
			os.path.join(
				self.test_dir,
				'no-format.txt'
			)
		)
		#  Test when file exists

		self.assertEqual(g, True)
		self.assertEqual(n, True)
		self.assertFalse(exists)

	def tearDown(self) -> None:

		g_file = os.path.join(self.test_dir, 'new-template-gunicorn.service')
		n_file = os.path.join(self.test_dir, 'new-sites-available')

		while os.path.isfile(g_file) or os.path.isfile(n_file):
			os.remove(g_file)
			print(f'{g_file} removed')
			os.remove(n_file)
			print(f'{n_file} removed')


class TestDeploy(TestCase):

	pass


if __name__ == '__main__':
	main()
