import http.server

import db
import calculator
import path_generator
import storage

PORT = 8000

OK_STATUS = 200
BAD_FORMAT_STATUS = 400
FILE_NOT_FOUND_STATUS = 404

DB_FILE_PATH = "db.json"

STORAGE_PATH = "storage"

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args):
        path_generator_object = path_generator.HashPathGenerator()

        self._db = db.Md5HashDB(DB_FILE_PATH)
        self._storage = storage.Storage(STORAGE_PATH, path_generator_object)
        self._calculator = calculator.CsvCalculator(self._storage)

        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        # path[1:] is to skip the "/" in the beginning of the hash
        file_hash = self.path[1:]

        try:
            file_name = self._db.read_object_from_db(file_hash)
        except KeyError:
            self.send_response(FILE_NOT_FOUND_STATUS)
            self.end_headers()
            return

        file_content = self._storage.read_file_from_storage(file_name).decode()

        self.send_response(OK_STATUS)
        self.end_headers()
        self.wfile.write(file_content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length).decode()

        file_name = self._storage.save_file_to_storage(file_content.encode())

        try:
            result = self._calculator.calculate(file_name)
        except calculator.FormatException as exception:
            self._storage.remove_file_from_storage(file_name)
            self.send_response(BAD_FORMAT_STATUS)
            self.end_headers()
            self.wfile.write(str(exception).encode())
            return

        file_hash = self._db.write_object_to_db(file_name, file_content)

        response = "Result : %d\nHash : %s" % (result, file_hash)

        self.send_response(OK_STATUS)
        self.end_headers()
        self.wfile.write(response.encode())


def run():
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()
