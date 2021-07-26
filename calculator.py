CSV_EXPECTED_LINES = 2
CSV_EXPECTED_COLUMNS = 3

class FormatException(Exception):
    pass

class CsvCalculator():
    def calculate(self, csv_content):
        csv_lines = csv_content.split("\r\n")

        if CSV_EXPECTED_LINES != len(csv_lines):
            raise FormatException("Unexpected number of lines")

        header_line = csv_lines[0].split(',')
        if CSV_EXPECTED_COLUMNS != len(header_line) or header_line[0] != "OP" or header_line[1] != "First" or header_line[2] != "Second":
           raise FormatException("Failed to parse header line")

        operation_line = csv_lines[1].split(',')
        if CSV_EXPECTED_COLUMNS != len(operation_line):
            raise FormatException("Failed to parse operation line")

        if "+" == operation_line[0]:
            result = int(operation_line[1]) + int(operation_line[2])
        elif "-" == operation_line[0]:
            result = int(operation_line[1]) - int(operation_line[2])
        elif "*" == operation_line[0]:
            result = int(operation_line[1]) * int(operation_line[2])
        elif "/" == operation_line[0]:
            result = int(operation_line[1]) / int(operation_line[2])
        else:
            raise FormatException("Operation not valid")

        return result