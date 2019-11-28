"""
Helper functions for the project.
"""

import yaml


def read_yaml(file_path):
    """
	Reads a yaml file.

	Args:
		file_path (str): Path to the file.

	Returns:
		dict: The file object.
	"""
    with open(file_path, "r") as file_pointer:
        return yaml.full_load(file_pointer)


def write_yaml(object, file_path):
    """
	Writes a yaml file.

	Args:
		object: The object that should be writen to file.
		file_path: Path to the file. 
	"""
    with open(file_path, "w") as file_pointer:
        yaml.dump(object, file_pointer)
