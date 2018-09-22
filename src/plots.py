import os

import matplotlib.pyplot as plt

from collections import namedtuple

from src.get_strava_data import get_activity_polylines


def create_heatmap(activity_params={}, style='black', color='deepskyblue',
                   save=False, img_filename='heatmap.png'):
    """Creates static heatmap with activity polylines.

    Args:
        activity_params (dict): Optional parameters for retrieved
            activities. Format below. Default plots all activities.
            {
                'after': 'YYYY-MM-DD',
                'before': 'YYYY-MM-DD',
                'limit': int
            }
        style (str): Optional, background color of map.
        color (str): Optional, color of activity polylines.
        save (boolean): Optional parameter, whether to save plot.
        img_filename (str): Optional, name of image.

    Returns:
         None
    """
    polylines = get_activity_polylines(**activity_params)
    latitude, longitude = extract_lat_long(polylines)

    fig, ax = plt.subplots(figsize=(24, 18))
    fig.set_facecolor(style)
    ax.set_axis_off()
    ax.plot(longitude, latitude, color=color, lw=0.5, alpha=0.7)

    if save:
        save_figure(fig, img_filename)

    plt.show()


def extract_lat_long(polylines):
    """Extracts latitude and longitude points from polyline data.

    Args:
        polylines (list): List of polylines

    Returns:
        namedtuple: With latitude (list) and longitude (list) points.
    """
    Lat_Long = namedtuple('Lat_Long', ['latitude', 'longitude'])
    latitude, longitude = [], []
    for polyline in polylines:
        lat, lon = zip(*polyline)
        latitude += lat
        longitude += lon

    return Lat_Long(latitude, longitude)


def create_facet_plot(activity_params={}, style='white', color='black',
                      save=False, img_filename='facet_plot.png'):
    """Creates facet plot with individual activities.

    Args:
        activity_params (dict): Optional parameters for retrieved
            activities. Format below. Default plots all activities.
            {
                'after': 'YYYY-MM-DD',
                'before': 'YYYY-MM-DD',
                'limit': int
            }
        style (str): Optional, background color of map.
        color (str): Optional, color of activity polylines.
        save(boolean): Optional parameter, whether to save plot
        img_filename (str): Optional, name of image.

    Returns:
        None
    """
    polylines = get_activity_polylines(**activity_params)
    sq_dim = facet_plot_dimensions(len(polylines))

    fig, axes = plt.subplots(figsize=(24, 24), nrows=sq_dim, ncols=sq_dim)
    fig.set_facecolor(style)

    polyline_iterator = iter(polylines)
    for row in axes:
        for col in row:
            try:
                lat, lon = zip(*polyline_iterator.__next__())
                col.plot(lat, lon, color='black', lw=0.7)
            except StopIteration:
                pass
            col.axis('off')
            plt.axis('equal')


def facet_plot_dimensions(n_activities):
    """Returns dimension N of a N x N facet plot that fits n_activities.

    Args:
        n_activities (int): Number of activities to be plotted.

    Returns:
        int: The number of rows and columns to be used.
    """
    return min(i for i in range(100) if i**2 >= n_activities)


def save_figure(fig, filename):
    """Saves figure to img directory.

    If img directory does not exist, it will be created.

    Args:
        fig (matplotlib.figure): Figure to be saved.
        name (str): Name of output image file.

    Returns:
        None
    """
    img_directory = './img'
    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)

    plt.savefig(
        os.path.join(img_directory, filename),
        facecolor=fig.get_facecolor(),
        edgecolor=None
    )
