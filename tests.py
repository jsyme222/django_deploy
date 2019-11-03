#!/usr/bin python3.7
import getpass
import os
from unittest import TestCase, main
from unittest.mock import patch
from django_deploy import GunicornSock


class TestGunicornSock(TestCase):
	"""Testing functionality of tool creating
	Gunicorn files and connection
	"""

	def setUp(self):
		self.project_name = 'projectname'
		self.project_path = '/home/username/projectname/appname'
		self.project_name = 'appname'
		self.user = getpass.getuser()
		self.sock = GunicornSock()

	def test_user(self):
		sock = GunicornSock()
		self.assertEqual(self.user, sock.user)

	def test_template_loc(self):
		self.assertEqual(True, os.path.isfile(self.sock.template))

	@patch('GunicornSock.prompt_user', return_value='appname')
	def test_project_name(self, input):
		self.assertEqual(
			self.get_project_info['project_name'],
			self.project_name
		)

	def test_get_project_info(self):
		info = self.sock.get_project_info()
		self.assertEqual(getpass.getuser(), info['user'])


if __name__ == '__main__':
	main()
