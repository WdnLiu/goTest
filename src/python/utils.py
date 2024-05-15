import matplotlib.colors as mcolors
from matplotlib import patches, pyplot as plt
import numpy as np
import json

def parse_json_file(file_name: str):
    file_path = "data/" + file_name
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the instruments data
    instruments = data['instruments']
    
    # Determine the number of instruments and intervals
    num_instruments = len(instruments)
    num_intervals = len(instruments[0]['intervals']) if num_instruments > 0 else 0
    
    # Create a NumPy boolean matrix to store the intervals
    intervals_matrix = np.zeros((num_instruments, num_intervals), dtype=bool)
    
    # Populate the matrix with the intervals data
    for i, instrument in enumerate(instruments):
        intervals_matrix[i] = instrument['intervals']
    
    return intervals_matrix

def save_boolean_matrix(bool_matrix, save_name="output.png"):
    n, m = bool_matrix.shape
    matrix_with_spacing = np.zeros((n*2-1, m), dtype=bool)
    matrix_with_spacing[::2] = bool_matrix
    matrix_with_spacing[1::4] = False  # Set every second row to False (white)
    cmap = mcolors.ListedColormap(['white', 'darkgrey'])
    plt.imshow(matrix_with_spacing, cmap=cmap, interpolation='nearest')
    plt.xlabel('Timestamps')
    plt.ylabel('Instruments')
    plt.yticks(np.arange(0, 2 * n, 2), np.arange(1, n + 1))
    plt.title('Result of instrument classification')
    plt.savefig("src/html/" + save_name)