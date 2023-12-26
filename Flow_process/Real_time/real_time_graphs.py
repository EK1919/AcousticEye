from constants import *
import matplotlib.pyplot as plt
import numpy as np
PAUSE = 0.1
TIME_SHOWN = 10


def initialize_graph(x_label: str, y_label: str, title: str, num_lines=1):
    fig, ax = plt.subplots()
    lines = [ax.plot([], [], label=f'Data Line {i}')[0] for i in range(num_lines)]
    data = [[] for _ in range(num_lines)]  # List of data arrays for each line
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim([-65, 65])
    ax.set_title(title)
    plt.ion()
    return fig, ax, lines, data


def update_plot(fig, ax, lines, data, new_x, new_y, vertical_line_x=False, time_of_sample=0.1):
    for i, y_values in enumerate(new_y):
        if len(data[i]) == 0:
            data[i].append((new_x, y_values))
        else:
            data[i].append((new_x, y_values))
            lines[i].set_xdata([point[0] for point in data[i]])
            lines[i].set_ydata([point[1] for point in data[i]])
            if len(data[i]) > (1 / time_of_sample) * TIME_SHOWN:
                data[i].pop(0)

    ax.relim()
    ax.autoscale_view()
    plt.xlim(new_x - 10, new_x)

    # Draw vertical red line if specified
    if vertical_line_x:
        ax.axvline(x=new_x, color='red', linestyle='--')

    fig.canvas.draw_idle()
    plt.show()


def initialize_scatter(x_label: str, y_label: str, title: str):
    fig, ax = plt.subplots()
    scatter = ax.scatter([], [], label='Data')  # Use scatter plot instead of a line
    data = {'x': [], 'y': []}
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.ion()
    return fig, ax, scatter, data


def update_scatter(fig, ax, scatter, data, new_x, new_y):
    data['x'].append(new_x)
    data['y'].append(new_y)
    scatter.set_offsets(list(zip(data['x'], data['y'])))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()
    plt.pause(0.1)  # You can adjust the pause duration if needed
    plt.show()


def update_number_plot(fig, axes, lines, data, plot_number, new_x, new_y):
    data[plot_number - 1].append((new_x, new_y))
    lines[plot_number - 1].set_xdata([point[0] for point in data[plot_number - 1]])
    lines[plot_number - 1].set_ydata([point[1] for point in data[plot_number - 1]])
    axes[plot_number - 1].relim()
    axes[plot_number - 1].autoscale_view()

    fig.canvas.draw_idle()
    plt.pause(0.1)


def initialize_all_graphs(num_plots: int, x_labels: list[str], y_labels: list[str], titles: list[str]):
    # Enable interactive mode
    plt.ion()

    # Initialize a single figure with multiple subplots
    fig, axes = plt.subplots(num_plots, 1, sharex=True)

    # Initialize empty plots and data for each subplot
    lines = [axes[i].plot([], [], label=f'Data {i + 1}')[0] for i in range(num_plots)]
    data = [[] for _ in range(num_plots)]

    # Set labels and titles for each subplot
    for i in range(num_plots):
        axes[i].set_xlabel(x_labels[i])
        axes[i].set_ylabel(y_labels[i])
        axes[i].set_title(titles[i])

    return fig, axes, lines, data


class RealTimeGraphs:
    """
    This class is responsible for the real time graphs of the system.
    """
    def __init__(self):
        self.graphs_properties = {}
        self.sample_time = SAMPLE_FROM_MIC

    def real_time_fft(curr_data, curr_time, last_time, sum_of_time, curr_lobe=0):
        """
        This function plots the fft of the data received from the system.
        """

        plt.clf()
        sum_of_time += curr_time - last_time
        last_time = curr_time
        fft_data = np.apply_along_axis(np.fft.fft, 1, curr_data)
        freq = np.fft.fftfreq(fft_data.shape[1], d=1 / SF)
        for channel_num in range(1):
            plt.plot(freq, np.abs(fft_data[channel_num, :]),label=f'Channel {channel_num + 1}', alpha=0.7)
        plt.title(f'Combined FFT for All Channels for time {sum_of_time}')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid()
        plt.ion()
        return last_time, sum_of_time, curr_lobe

    def initialize_graph_inner(self, graph_name: str, x_name: str, y_name: str, lines_num: int = 1):
        self.graphs_properties[graph_name] = initialize_graph(x_name, y_name, graph_name, lines_num)

    def update_graph_inner(self, graph_name: str, new_x: float, new_y, red_line: bool):
        if not isinstance(new_y, list):
            f, a, l, d = self.graphs_properties[graph_name]
            update_plot(f, a, l, d, new_x, [new_y], red_line, self.sample_time)
        else:
            f, a, l, d = self.graphs_properties[graph_name]
            update_plot(f, a, l, d, new_x, new_y, red_line, self.sample_time)


if __name__ == '__main__':
    num_plots = 3
    x_labels = ['X-axis'] * num_plots
    y_labels = ['Y-axis'] * num_plots
    titles = [f'Graph {i + 1}' for i in range(num_plots)]

    real_time_graphs = RealTimeGraphs()
    fig, axes, lines, data = initialize_all_graphs(num_plots, x_labels, y_labels, titles)

    # Update the plots with new data
    for i in range(10):
        for plot_number in range(1, num_plots + 1):
            update_number_plot(fig, axes, lines, data, plot_number, i, np.sin(i + plot_number))

    plt.show()
