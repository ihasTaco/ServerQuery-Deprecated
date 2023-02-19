import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import MaxNLocator
import json
import json_parser
import numpy as np
import logging
    
def calculate_hourly_averages(player_data):
    # This function calculates hourly averages for player data
    num_labels = len(player_data)
    hourly_averages = [sum(player_data[:i+1]) / len(player_data[:i+1]) for i in range(num_labels)]
    return hourly_averages

def generate_time_labels(current_time, interval, num_labels):
    # This function generates a list of time labels to be used on the x-axis of the plot
    time_labels = []
    for i in range(num_labels):
        if i % 24 == 0:
            # Add a label for every 24th time point in the range
            time_labels.append((current_time - interval * (num_labels - i - 1)).strftime("%I %p"))
    return time_labels

def set_plot_limits(players, hourly_averages = [0]):
    # This function sets the limits for the y-axis of the plot based on the player data and hourly averages
    max_value = max(max(players), max(hourly_averages)) + 1
    y_upper_limit = max_value + max_value/2 # Add half of the max value to the upper limit
    plt.ylim([0, y_upper_limit])

def set_plot_labels(time, time_labels):
    # This function sets the labels for the x-axis of the plot
    plt.xticks(time[::24], time_labels[::1], rotation=45)

def set_plot_style(graph_config):
    # This function sets the style and formatting options for the plot
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    if graph_config['Grid']['Display'] == True:
        ax.grid(True, alpha=graph_config['Grid']['Opacity'], color=graph_config['Grid']['Color'])

    ax.yaxis.label.set_color(graph_config['Labels']['Color'])
    ax.xaxis.label.set_color(graph_config['Labels']['Color'])
    ax.tick_params(axis='both', colors=graph_config['Tick Color'])
    plt.xlabel(graph_config['Labels']['X Label Text'], color=graph_config['Labels']['Color'])
    plt.ylabel(graph_config['Labels']['Y Label Text'], color=graph_config['Labels']['Color'])
    plt.title(graph_config['Title']['Text'], color=graph_config['Title']['Color'])

def plot_player_data(server_UUID):
    data = json_parser.load_json_file("data_management\server_info.json")

    # Get player count data for the server
    players = data[server_UUID]['Player Count']
    graph_config = data[server_UUID]['Graph']

    # Set up time range for x-axis
    current_time = datetime.datetime.now()
    interval = datetime.timedelta(minutes=5)
    num_labels = 288 # 5 minutes * 288 = 24 hours
    time = [i for i in range(num_labels)]

    # Get player count data for the server
    current_players = players[-288:] # include only the last 288 elements

    if graph_config['Trend']['Display'] == True:
        # Calculate hourly averages for trend data
        hourly_averages = calculate_hourly_averages(players)

    # Generate time labels for x-axis
    time_labels = generate_time_labels(current_time, interval, num_labels)

    # Plot the data and add labels
    plt.plot(time, current_players, label=graph_config['Online Players']['Label'], color=graph_config['Online Players']['Line Color'])
    
    if graph_config['Trend']['Display'] == True:
        # Plot the trend data
        trend_time = np.linspace(0, num_labels-1, len(hourly_averages))
        plt.plot(trend_time, hourly_averages, color=graph_config['Trend']['Line Color'], label=graph_config['Trend']['Label'], linestyle='--')

    if graph_config['Legend']['Display'] == True:
        # Create legend
        plt.legend(fontsize='medium', facecolor=graph_config['Legend']['Color'], framealpha=graph_config['Legend']['Opacity'], edgecolor=graph_config['Legend']['Edge Color'])
    
    if graph_config['Trend']['Display'] == True:
        # Set the y-axis limit based on the maximum value
        set_plot_limits(current_players, hourly_averages)
    else:
        # Set the y-axis limit based on the maximum value
        set_plot_limits(current_players)

    # Add x-axis labels
    set_plot_labels(time, time_labels)

    # Show only whole numbers on the y-axis and set plot style
    set_plot_style(graph_config)

    # Add a shaded area under the plot
    plt.fill_between(time, 0, current_players, color=graph_config['Online Players']['Fill Color'], alpha=graph_config['Online Players']['Fill Opacity'])

    # Save the plot as an image file
    plt.tight_layout()
    plt.margins(x=0)
    plt.savefig('discord_bot/images/player_data.png', facecolor='None', edgecolor='None', transparent=True)

    # Show the plot
    plt.close()