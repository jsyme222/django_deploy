#!/user/bin python3.7
import settings
from main import GunicornSock as sock
from main import NginxVirtualBox as nginx


def main():

	welcome = """Django Deploy\nThis tool is meant to ease the deployment of Django projects\nutilizing the lightweight power of Nginx web server and\nWSGI application service by Gunicorn"""
	sock.center('\n', delim="*", end="")  # Text decoration function
	sock.center(welcome, delim=" ")
	sock.center('\n', delim="*", end="")

	if not settings.check_django_dir():
		sock.center(f'The current directory\n{settings.current_dir}\nDoes not contain a \'manage.py\' file.\nContinue?\n ', delim=" ", end="")
		choice = input('[Y/n]')
		if choice not in 'Yy':
			exit()
	g = sock.GunicornSock()
	complete = g.run()

	if complete:
		n = nginx.NginxVirtualBox(complete)
		n.run()


if __name__ == '__main__':
	main()
