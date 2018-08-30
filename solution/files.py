from solution.models import Segment
from solution.settings import *


class FileEngine(object):
    input_filename = None
    output_filename = None

    def __init__(self, file_id):
        self.input_filename = os.path.join(INPUT_DIR, str(file_id) + INPUT_FILENAME_POSTFIX)
        self.output_filename = os.path.join(OUTPUT_DIR, str(file_id) + OUTPUT_FILE_POSTFIX)

    def read(self):
        result = []
        with open(self.input_filename, 'r') as file:
            for line in file.readlines()[1:]:
                array = [int(x) for x in line.split(' ')]
                result.append(Segment(array[0], array[1]))
        return result

    def write(self, time):
        with open(self.output_filename, 'w+') as file:
            file.write(str(time))
