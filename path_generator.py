import hashlib

class BasePathGenerator:
    def generate_path(self, file_content):
        raise NotImplementedError

class HashPathGenerator(BasePathGenerator):
    def generate_path(self, file_content):
        return hashlib.md5(file_content).hexdigest() + ".csv"
