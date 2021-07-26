import json
import hashlib

DB_FILE_PATH = "db.json"

class CsvDB():
    def __init__(self):
        try:
            db_file = open(DB_FILE_PATH, "rb")
        except FileNotFoundError:
            self._db_dict = {}
        else:
            self._db_dict = json.loads(db_file.read().decode())
            db_file.close()

    # The function writes the given file to db,
    # and returns a hash to access the file in the future
    def write_file_to_db(self, file_path, file_content):
        file_hash = hashlib.md5(file_content.encode()).hexdigest()
        self._db_dict[file_hash] = file_path

        with open(DB_FILE_PATH, "wb") as db_file:
            db_file.write(json.dumps(self._db_dict).encode())

        return file_hash

    # The function receives the file hash and returns it's path
    def read_file_from_db(self, file_hash):
        return self._db_dict[file_hash]

    # The function returns whether a hash exists in DB
    def is_hash_in_db(self, file_hash):
        return file_hash in self._db_dict
