import sys
import utils

# script.py
if len(sys.argv) < 1:
    print("Not enough arguments")

bool_matrix = utils.parse_json_file(sys.argv[1])

utils.save_boolean_matrix(bool_matrix)