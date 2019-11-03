#!/usr/bin python3.7
import getpass
import os
from unittest import TestCase, main
from django_deploy import GunicornSock


class TestGunicornSock(TestCase):
	"""Testing functionality of tool creating
	Gunicorn files and connection
	"""

	def setUp(self):
		self.project_name = 'projectname'
		self.project_path = '/home/username/projectname/appname'
		self.user = getpass.getuser()
		self.sock = GunicornSock()

	def test_user(self):
		sock = GunicornSock()
		self.assertEqual(self.user, sock.user)

	def test_template(self):
		self.assertEqual(True, os.path.isfile(self.sock.template))

	def test_get_project_info(self):
		info = self.sock.get_project_info()
		self.assertEqual(getpass.getuser(), info)


if __name__ == '__main__':
	main()
