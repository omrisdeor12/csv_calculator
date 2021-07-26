import json
import hashlib

# This is the base DB, from which it is possible to write an object to the data base,
# and get this object from the database according to it's signature in the DB
class BaseDB():
    # The function receives an object, 
    # and saves it to the DB.
    # The function returns a signature of the file,
    # for future read from DB
    def write_object_to_db(self, object_to_write):
        raise NotImplementedError

    # The function receives the signature of the object returned from write_object_to_db,
    # and returns the object
    def read_object_from_db(self, object_signature):
        raise NotImplementedError

# This DB also saves to the file system the current DB
class FileSystemDB(BaseDB):
    # The init function loads the DB into the object from the file
    def __init__(self, db_file_path):
        self._db_file_path = db_file_path
        self.read_db_from_file()

    # The function should convert the DB to bytes, 
    # this is the format in which the DB will be saved to the file system
    # In case file_content is None, an empty DB should be created
    def convert_bytes_to_db(self, file_content):
        raise NotImplementedError

    # The function should convert the DB to bytes, 
    # this is the format in which the DB will be saved to the file system
    def convert_db_to_bytes(self):
        raise NotImplementedError

    def read_db_from_file(self):
        try:
            with open(self._db_file_path, "rb") as db_file_handler:
                file_content = db_file_handler.read()
        except FileNotFoundError:
            self.convert_bytes_to_db(None)
        else:
            self.convert_bytes_to_db(file_content)

    def write_db_to_file(self):
        with open(self._db_file_path, "wb") as db_file_handler:
            db_file_handler.write(self.convert_db_to_bytes())

# This class implements a FileSystemDB, in the format of JSON
class JsonDB(FileSystemDB):
    def __init__(self, db_file_path):
        FileSystemDB.__init__(self, db_file_path)

    def convert_bytes_to_db(self, file_content):
        if file_content is None:
            self._json_dict = {}
        else:
            self._json_dict = json.loads(file_content.decode())

    def convert_db_to_bytes(self):
        return json.dumps(self._json_dict).encode()

    # Usefull functions for writing and reading objects from the database
    def write_object_to_db(self, object_signature, object_to_write):
        self._json_dict[object_signature] = object_to_write
        self.write_db_to_file()

        return object_signature

    def read_object_from_db(self, object_signature):
        return self._json_dict[object_signature]

# This DB save files, when the signature of them is their content's md5 hash.
# The files are saved to the DB as their path, which is generated from the received path_generator.
# The DB is saved to the file system also, so in future execution DB will be loaded again.
class Md5HashDB(JsonDB):
    def __init__(self, db_file_path):
        JsonDB.__init__(self, db_file_path)

    # The function writes the given file to db,
    # and returns a hash to access the file in the future
    def write_object_to_db(self, file_name, file_content):
        file_hash = hashlib.md5(file_content.encode()).hexdigest()
        
        return JsonDB.write_object_to_db(self, file_hash, file_name)
