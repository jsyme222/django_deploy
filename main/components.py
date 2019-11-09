#!/user/bin python3.7
import os
import re


def center(text, width=80, delim="-", end="\n"):
    """
	Text align and decoration for terminal display

	:param text: {str}
	:param width: {int}
	:param delim: {str}
	:param end: {str}
	:return:
	"""
    lines = text.split('\n')
    for line in lines:
        print(line.center(width, delim) + end)


def check_django_dir(directory):
    """
	Checks for a 'manage.py' file to verify base directory
	of a django project

	:param directory: str()
	:return django_dir: bool()
	"""

    if 'manage.py' not in os.listdir(directory):
        django_dir = False

    return django_dir


def default_env_dir(root):
    """
	Builds a default directory for the virtual
	environment based off of the 'root' base_dir.

	:param root: str(Directory)
	:return env: str()
	"""

    temp = root.split('/')
    env = '/'.join(temp[:-1])
    env += '/.env/'

    return env


class Collector:  # TODO Get actual file path and file name
    """
    The Collector class is designed to take in any file and format
    the file with the appropriate values as defined within the symbols
    found in the formatted file.  # TODO will change as features accumulate
    """
    def __init__(self, file):
        self.errors = {}

        if not os.path.isfile(file):
            self.errors['file_error'] = f'Template not found at {file}'
            self.read_err()
        else:
            self.file_path = file
            with open(file, 'r') as f:
                self.file = f.read()

    def read_err(self):  # Reads errors
        for error in self.errors:
            print(f'{error.upper()}: {self.errors[error]}')

    def pull_vars(self, raw=False):  # TODO docstring
        payload = []
        raw_vars = []
        var_pattern = re.compile('({[$].*?\\})', re.IGNORECASE | re.DOTALL)
        variables = var_pattern.findall(self.file)

        if len(variables) < 1:
            self.errors['File Format'] = 'File not formatted'

        for var in variables:
            if var not in raw_vars:
                raw_vars.append(var)
            case = var[3:-2]
            case = tuple(case.split(', '))
            if case not in payload:
                payload.append(case)

        if raw:
            return raw_vars
        else:
            return payload

    def inputs(self, output_file=True):
        """
		Takes in a file pre-formatted with {$ variable, required, default_value }
		symbols. Returns a payload dict() using {'variable': response} formatting.
        Output declares whether or not the function should call the outputs function
        after gathering inputs.

		:param output_file: bool()
		:return payload: dict()
		"""

        SYSTEM_CALLS = {
            '$USER': os.getlogin(),
            '$PWD': os.getcwd(),
            '$ENV_DIR': default_env_dir(os.getcwd()),
            '$SOCK_DIR': os.getcwd() + '/' + os.getcwd().split('/')[-1] + '.sock',
            '$PROJECT_NAME': os.getcwd().split   ('/')[-1],
        }

        def read_from_file(added_functions={}):  # TODO docstring
            payload = {}

            if not os.path.isfile(self.file_path):
                self.errors['No File'] = 'File is not at location'

            if len(added_functions.keys()) >= 1:
                SYSTEM_CALLS.update(added_functions)

            for case in self.pull_vars():
                prompt, required, default = case[0], case[1], case[2]
                if default.startswith('$'):
                    default = SYSTEM_CALLS[default]

                if prompt not in payload.keys():
                    if required != 'True':
                        user_input = input(f'{prompt}\n[{default}] : ')
                        if user_input == '':
                            user_input = default
                    else:
                        user_input = input(f'{prompt} : ')
                        while user_input == '':
                            user_input = input(f'{prompt} : ')

                    payload[prompt] = user_input

            return payload

        if len(self.errors.keys()) == 0:
            reading = read_from_file()
            if reading and output_file:
                self.outputs(reading)
            elif reading and not output_file:
                return reading
            else:
                self.errors['File Read'] = 'Error while reading inputs from file'
                self.read_err()

    def outputs(self, data):  # TODO docstring
        """
		Takes data as dict() and writes to file based upon
		which template is passed as self.file_path.

		:param data: dict()
		:return complete: bool()
		"""

        filename = self.file_path.split('/')[-1]
        write_to = f'./new_{filename}'
        collected = [x for x in data.values()]
        to_replace = self.pull_vars(raw=True)
        ready = dict(zip(to_replace, collected))

        def write_to_file():
            with open(write_to, 'w+') as f:
                file = self.file
                for k in ready.keys():
                    file = file.replace(k, ready[k])  # Replaces all symbols in file with values

                f.write(file)

            if os.path.isfile(write_to):
                print(f'File - {write_to} created')
                return True
            else:
                self.errors['File Write'] = 'Error while writing file'
                self.read_err()
                return False

        if os.path.isfile(write_to):
            self.errors['File Exists'] = f'File {filename} already found at {write_to}'
            complete = False
        else:
            return write_to_file()  # Write new file

        return complete
