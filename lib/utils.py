import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import json
import plotly.graph_objects as go

instrument_names = ['Voice', 'Violin', 'Mridangam', 'Ghatam']

def parse_json_file(file_name: str):
    file_path = "data/" + file_name
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the boolean interval arrays
    is_voice = data['is_voice']
    is_violin = data['is_violin']
    is_mridangam = data['is_mridangam']
    is_ghatam = data['is_ghatam']
    
    # Determine the number of intervals (assuming all arrays have the same length)
    num_intervals = len(is_voice)
    
    # Create a NumPy boolean matrix to store the intervals
    intervals_matrix = np.zeros((4, num_intervals), dtype=bool)
    
    # Populate the matrix with the intervals data
    intervals_matrix[0] = is_voice
    intervals_matrix[1] = is_violin
    intervals_matrix[2] = is_mridangam
    intervals_matrix[3] = is_ghatam
    
    return intervals_matrix

def plot_audio_from_json(json_file, save_name):
    with open(json_file, 'r') as file:
        data = json.load(file)

    audio_array = data['audio_array']

    x = list(range(len(audio_array)))
    y = audio_array

    plt.plot(x,y)
    plt.savefig(save_name, format='html')
    plt.close()

def save_boolean_matrix(bool_matrix, save_name="output.png"):
    n, m = bool_matrix.shape
    # Create a new matrix with spacing between the original matrix rows
    matrix_with_spacing = np.zeros((n*2, m), dtype=int)
    matrix_with_spacing[::2] = bool_matrix * np.arange(1, n+1).reshape(n, 1)
    
    # Define the colormap: the first color for the background (white), and the rest for instruments
    background_color = 'white'
    instrument_colors = ['red', 'green', 'blue', 'purple', 'orange', 'yellow', 'cyan', 'magenta']
    colors = [background_color] + instrument_colors[:n]
    cmap = mcolors.ListedColormap(colors)
    
    # Create the plot
    plt.imshow(matrix_with_spacing, cmap=cmap, interpolation='nearest', aspect='auto')
    
    timestep = 0.1  # assuming timestep is 0.1 seconds
    total_time_seconds = m * timestep
    total_time_minutes = total_time_seconds / 60

    # Calculate the x-ticks for every minute
    xt = np.arange(0, m, 60 / timestep)
    x = xt * timestep / 60  # convert ticks to minutes

    # Generate time labels in 'minute:second' format
    t = pd.to_datetime(x, unit='m')
    t_format = [f'{time.minute}:{time.second:02d}' for time in t]

    # Set the x-axis and y-axis labels
    plt.xlabel('Time')
    plt.ylabel('Instruments')
    
    # Set the y-ticks to the instrument names
    y_repl = np.arange(0, 2 * n, 2)
    plt.yticks(y_repl, instrument_names)
    
    # Set the x-ticks with one-minute intervals
    plt.xticks(xt, t_format, rotation=45)

    # Set the title of the plot
    plt.title('Result of Instrument Classification')
    
    # Save the plot to a file
    plt.savefig("public/" + save_name)
    plt.close()

def save_boolean_matrix_interactive(bool_matrix, save_name="output.html"):
    n, m = bool_matrix.shape
    # Create a new matrix with spacing between the original matrix rows
    matrix_with_spacing = np.zeros((n*2, m), dtype=int)
    matrix_with_spacing[::2] = bool_matrix * np.arange(1, n+1).reshape(n, 1)
    
    # Define the colormap: the first color for the background (white), and the rest for instruments
    background_color = 'white'
    instrument_colors = ['red', 'green', 'blue', 'purple']
    colors = [background_color] + instrument_colors[:n]
    
    # Create a custom colorscale for the heatmap
    colorscale = [(0, background_color)]
    for i in range(1, n+1):
        colorscale.append((i/(n), instrument_colors[i-1]))
    colorscale.append((1, instrument_colors[-1]))  # Ensure the last color is included

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix_with_spacing,
        colorscale=colorscale,
        showscale=False,
        zmin=0,
        zmax=n
    ))

    # Calculate the x-ticks for every minute
    timestep = 0.1  # assuming timestep is 0.1 seconds
    total_time_seconds = m * timestep
    total_time_minutes = total_time_seconds / 60

    xt = np.arange(0, m, 60 / timestep)
    x = xt * timestep / 60  # convert ticks to minutes

    # Generate time labels in 'minute:second' format
    t = pd.to_datetime(x, unit='m')
    t_format = [f'{time.minute}:{time.second:02d}' for time in t]

    # Set the layout
    fig.update_layout(
        title='Result of Instrument Classification',
        xaxis=dict(
            title='Time',
            tickmode='array',
            tickvals=xt,
            ticktext=t_format,
            tickangle=45
        ),
        yaxis=dict(
            title='Instruments',
            tickmode='array',
            tickvals=list(range(0, 2 * n, 2)),
            ticktext=instrument_names,
            autorange='reversed'
        ),
        showlegend=False,
        height=600,
        width=1000
    )

    # Save the plot to an HTML file
    fig.write_html("public/" + save_name)

def generate_waveform(file_name, save_name="output.html"):
    # Load JSON data
    file_path = "data/" + file_name
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract amplitude values
    amplitudes = data["audio_array"]

    # Create a time axis based on the number of amplitude samples
    time = np.linspace(0, len(amplitudes), num=len(amplitudes))

    # Plot the sound wave
    plt.figure(figsize=(10, 4))
    plt.plot(time, amplitudes)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sound Wave Visualization')
    plt.legend()
    plt.grid(True)
    plt.savefig('public/sound_wave.png')  # Save the plot as an image file
    plt.close()  # Close the plot to free up memory
