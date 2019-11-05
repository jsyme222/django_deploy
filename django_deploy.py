#!/user/bin python3.7
import os
from main import GunicornSock as sock
from main import NginxVirtualBox as nginx
from main import components as comp


def main():

	ROOT_DIR = os.getcwd()

	welcome = """Django Deploy\nThis tool is meant to ease the deployment of Django projects\nutilizing the lightweight power of Nginx web server and\nWSGI application service by Gunicorn"""
	comp.center('\n', delim="*", end="")  # Text decoration function
	comp.center(welcome, delim=" ")
	comp.center('\n', delim="*", end="")

	if not nginx.comp.check_django_dir(ROOT_DIR):  # Check for 'manage.py' in cwd
		comp.center(
			f'The current directory\n{ROOT_DIR}\nDoes not contain a \'manage.py\' file.\nContinue?\n ',
			delim=" ",
			end="",
		)
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()

	user = ('user', False, os.getlogin())
	group = ('group', False, 'www-data')
	root_dir = ('root_dir', False, ROOT_DIR)
	project_name = ('project_name', True, None)
	domains = ('domains', True, None)
	path_to_env = ('path_to_env', False, comp.default_env_dir(ROOT_DIR))

	info = comp.Collect.inputs()
	g = sock.GunicornSock()
	sock_complete = g.run(info)

	if sock_complete:
		n = nginx.NginxVirtualBox(sock_complete)
		n.run()


if __name__ == '__main__':
	main()
