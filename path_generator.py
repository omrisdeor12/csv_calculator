import hashlib

def generate_path(file_content):
	return hashlib.md5(file_content.encode()).hexdigest() + ".csv"
