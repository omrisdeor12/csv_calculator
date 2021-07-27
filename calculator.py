import csv

class FormatException(Exception):
    pass

class BaseCalculator():
    def __init__(self, storage_object):
        self._storage = storage_object

    def calculate(self, file_name):
        raise NotImplementedError

class CsvCalculator(BaseCalculator):
    def calculate(self, file_name):
        file_path = self._storage.get_file_path(file_name)

        with open(file_path, "rt") as file_handler:
            csv_reader = csv.reader(file_handler, delimiter=',')

            first_line = next(csv_reader)

            if 'OP' != first_line[0] or 'First' != first_line[1] or 'Second' != first_line[2]:
                raise FormatException("Header line is in wrong format")

            operation, first, second = tuple(next(csv_reader))

            try:
                first = int(first)
                second = int(second)
            except ValueError:
                raise FormatException("First or Second is not a number")

            if '+' == operation:
                result = first + second
            elif '-' == operation:
                result = first - second
            elif '*' == operation:
                result = first * second
            elif '/' == operation:
                result = first / second
            else:
                raise FormatException("Operation is not supported")

            return result
