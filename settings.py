#!/user/bin python3.7
import os

current_dir = os.getcwd()


def check_django_dir():
	scan_files = os.scandir(current_dir)
	files = [x.name for x in scan_files]
	django_dir = True
	if 'manage.py' not in files:
		django_dir = False

	return django_dir
