#!/user/bin python3.7
import settings
from main import GunicornSock as sock
from main import NginxVirtualBox as nginx


def main():

	welcome = """Django Deploy\nThis tool is meant to ease the deployment of Django projects\nutilizing the lightweight power of Nginx web server and\nWSGI application service by Gunicorn"""
	settings.center('\n', delim="*", end="")  # Text decoration function
	settings.center(welcome, delim=" ")
	settings.center('\n', delim="*", end="")

	if not settings.check_django_dir():
		settings.center(f'The current directory\n{settings.current_dir}\nDoes not contain a \'manage.py\' file.\nContinue?\n ', delim=" ", end="")
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()
	g = sock.GunicornSock()
	sock_complete = g.run()

	if sock_complete:
		n = nginx.NginxVirtualBox(sock_complete)
		n.run()


if __name__ == '__main__':
	main()
