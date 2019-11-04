#!/user/bin python3.7
import os
import getpass


def center(text, width=80, delim="-", end="\n"):  # Center multiple line 'text' with 'delim' padding
	lines = text.split('\n')
	for line in lines:
		print(line.center(width, delim) + end)


def prompt_user(prompt, require=False):  # Prompt user and loop if required input
	ask = input(prompt)
	if require:
		while ask == '':
			ask = input(prompt)
	return ask


class GunicornSock:
	"""
	Creates the Gunicorn websocket that the Django application will
	need to have opened to work with the Nginx server.
	"""

	def __init__(self):
		intro = 'Gunicorn Service Setup'
		print('\n')
		center(intro, end="\n\n")

	def get_project_info(self):
		intro = 'Information needed to set up\nGunicorn service files'

		print('\n')
		center(intro)
		print('\n')

		def get_user():
			print('\n')

			user_prompt = f"USER to run service under-\nDEFAULT: {getpass.getuser()}\n[Username] : "
			username = prompt_user(user_prompt)
			if username == '':
				username = getpass.getuser()

			center(f"\nUSER\n{username}", width=40, delim=" ", end="")
			return username

		def get_root_dir():
			print('\n')

			user_prompt = f"DIRECTORY to project root.\nThis should be the same as the \nproject settings 'BASE_DIR'\nDEFAULT: {os.getcwd()}\n[Directory] : "

			root_dir = prompt_user(user_prompt)
			if root_dir == '':
				root_dir = os.getcwd()

			while not os.path.isdir(root_dir):
				if root_dir:
					print('\n')
					center('ERROR', width=40, delim="x")
					center(f'Directory \'{root_dir}\' not valid', width=40)
				root_dir = input(user_prompt)

			center(f"\nBASE DIRECTORY\n{root_dir}", width=40, delim=" ", end="")
			return root_dir

		def get_project_name():
			print('\n')

			user_prompt = "PORJECT NAME\n[Project] : "
			project_name = prompt_user(user_prompt, require=True)

			center(f'\nPROJECT\n{project_name}', width=40, delim=" ", end="")
			return project_name

		def get_group():
			print('\n')

			user_prompt = "GROUP for socket access\nDEFAULT : 'www-data'\n[Group] : "
			group = prompt_user(user_prompt, require=False)
			if group == '':
				group = 'www-data'

			center(f'\nGROUP\n{group}', width=40, delim=" ", end="")
			return group

		def get_sock_path(root, name):
			if not root.endswith('/'):
				root += '/'
			root += str(name) + '.sock'

			center(f'Creating sock path at\n{root}', delim="*")

			return root

		def get_env_path(root):
			print('\n')

			root = root.split('/')
			root = '/'.join(root[:-1])
			user_prompt = f"Environment path-\nDEFAULT : {root + '/.env'}\n[Env Path] : "
			path = prompt_user(user_prompt)
			if path == '':
				path = root + '/.env'
			else:
				if not path.endswith('/'):
					path = path + '/'
				path = path + 'bin/gunicorn'

			def check_env_dir(path):
				bin_dir = path.split('/')[:-1]
				bin_dir = '/'.join(bin_dir)
				checked = map(os.path.exists, [bin_dir, path])
				checked = list(checked)
				print(checked)
				if not all(checked):
					center(f'ERROR', delim="x")
					if not checked[0]:
						center(f'Environment not located at\n{bin_dir}')
					else:
						center('Gunicorn not installed\nInstall now? (Y/n)')
						input('Install Gunicorn?')
					return exit()
				else:
					return checked

			center(f'\nENV PATH\n{path}', width=40, delim=" ", end="")
			return path

		user = get_user()
		group = get_group()
		root_dir = get_root_dir()
		path_to_env = get_env_path(root_dir)
		project_name = get_project_name()
		sock_path = get_sock_path(root_dir, project_name)

		return {
			'user': user,
			'group': group,
			'path_to_env': path_to_env,
			'project_name': project_name,
			'root_dir': root_dir,
			'sock_path': sock_path,
		}

	def create_service_file(self):  # Create gunicorn.service
		"""
		Create gunicorn.service file at /etc/systemd/system/gunicorn.service
		"""

		def read_temp():
			template = './file_templates/gunicorn/gunicorn.service'
			if not os.path.isfile(template):
					print('\n')
					center('ERROR', width=40, delim="x")
					center(f'Template not found\n\'{template}\'', width=40)
					exit()
			else:
				with open(template, 'r') as temp:
					temp = temp.read()
				return temp

		info = self.get_project_info()
		print(info)
		service_file = read_temp()
		for key in info.keys():
			service_file = service_file.replace('{ ' + key + ' }', info[key])

		return service_file


def main():
	g = GunicornSock()
	info = g.get_project_info()
	for k, v in info:
		center(f'{k}\n{v}\n\n')


if __name__ == '__main__':
	main()
