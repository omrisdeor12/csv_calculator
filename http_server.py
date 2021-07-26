import http.server
import db
import calculator
import path_generator

PORT = 8000

OK_STATUS = 200
BAD_FORMAT_STATUS = 400
FILE_NOT_FOUND_STATUS = 404

csv_db = db.CsvDB()
csv_calculator = calculator.CsvCalculator()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # path[1:] is to skip the "/" in the beginning of the hash
        file_hash = self.path[1:]
        
        if not csv_db.is_hash_in_db(file_hash):
            self.send_response(FILE_NOT_FOUND_STATUS)
            self.end_headers()
            return

        file_path = csv_db.read_file_from_db(file_hash)
        
        with open(file_path, "rb") as file_handler:
            file_content = file_handler.read().decode()

        self.send_response(OK_STATUS)
        self.end_headers()
        self.wfile.write(file_content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length).decode()

        try:
            result = csv_calculator.calculate(file_content)
        except calculator.FormatException as exception:
            self.send_response(BAD_FORMAT_STATUS)
            self.end_headers()
            return

        file_path = path_generator.generate_path(file_content)

        with open(file_path, "wb") as file_handler:
            file_handler.write(file_content.encode())

        file_hash = csv_db.write_file_to_db(file_path, file_content)

        response = "Result : %d\nHash : %s" % (result, file_hash)

        self.send_response(OK_STATUS)
        self.end_headers()
        self.wfile.write(response.encode())


def run():
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()
