#!/user/bin python3.7
import os
import getpass


class GunicornSock:
	"""Creates the Gunicorn websocket that the Django application will
	need to have opened to work with the Nginx server.
	"""

	def __init__(self):
		print('\nX_X_X_X_X_X_X_X')
		print('Gunicorn Service Setup')
		print('X_X_X_X_X_X_X_X\n')

		self.template = './file_templates/gunicorn/gunicorn.service'
		self.user = getpass.getuser()

	def get_project_info(self):
		print('\n------------------')
		print('Information needed to set up')
		print('Gunicorn service files')
		print('------------------\n')

		def get_user():
			print('\n')

			user_prompt = f"USER to run service under-\nIf left blank will use-> {getpass.getuser()}\nUsername: "
			username = input(user_prompt)
			if username == '':
				username = getpass.getuser()
			return username

		def get_root_dir():
			print('\n')

			def check_dir(dir):
				if os.path.isdir(root_dir):
					return True
				else:
					return False

			user_prompt = f"DIRECTORY to project root.\nThis should be the same as the \nproject settings 'BASE_DIR\nDirectory: "
			root_dir = ''

			while not check_dir(root_dir):
				if root_dir:
					print('Directory not valid')
				root_dir = input(user_prompt)

			return root_dir

		return {
			'user': get_user(),
			'root_dir': get_root_dir(),
		}

	def read_temp(self):
		with open(self.template, 'rb') as temp:
			temp = temp.read()
		return temp


g = GunicornSock()
print(g.get_project_info())
