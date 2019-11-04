#!/usr/bin python3.7
import getpass
import os
from unittest import TestCase, main
from main import GunicornSock as sock


class TestGunicornSock(TestCase):
	"""Testing functionality of tool creating
	Gunicorn files and connection
	"""

	def setUp(self):
		self.project_name = 'projectname'
		self.project_path = '/home/username/projectname/appname'
		self.project_name = 'appname'
		self.user = getpass.getuser()
		self.sock = sock.GunicornSock()

	def test_user(self):
		socket = sock.GunicornSock()
		self.assertEqual(self.user, socket.user)

	def test_template_loc(self):
		self.assertEqual(True, os.path.isfile(self.sock.template))

	def test_get_project_info(self):
		info = self.sock.get_project_info()
		self.assertEqual(getpass.getuser(), info['user'])


if __name__ == '__main__':
	main()
