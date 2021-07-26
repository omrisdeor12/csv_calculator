import os

class Storage():
    def __init__(self, storage_path, path_generator):
        self._storage_path = storage_path
        self._path_generator = path_generator

        if not os.path.exists(self._storage_path):
            os.makedirs(self._storage_path)

    def get_file_path(self, file_name):
        return os.path.join(self._storage_path, file_name)

    def save_file_to_storage(self, file_content):
        file_name = self._path_generator.generate_path(file_content)
        file_path = self.get_file_path(file_name)

        with open(file_path, "wb") as file_handler:
            file_handler.write(file_content)

        return file_name

    def read_file_from_storage(self, file_name):
        file_path = self.get_file_path(file_name)

        with open(file_path, "rb") as file_handler:
            file_content = file_handler.read()

        return file_content

    def remove_file_from_storage(self, file_name):
        file_path = self.get_file_path(file_name)

        os.remove(file_path)
