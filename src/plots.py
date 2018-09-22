import os

import matplotlib.pyplot as plt

from collections import namedtuple

from src.get_strava_data import get_activity_polylines


def create_heatmap(polylines, style='black', color='deepskyblue', save=False,
                   img_filename='heatmap.png'):
    """Creates static heatmap with activity polylines.

    Args:
        polylines (list): List of polylines to plot on map.
        style (str): Optional, background color of map. Either 'light'
            or 'dark'.
        color (str): Optional, color of activity polylines.
        save (boolean): Optional parameter, whether to save plot.
        img_filename (str): Optional, name of image, if image is to be
            saved.

    Returns:
        None
    """
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
        Namedtuple with latitude (list) and longitude (list) points.
    """
    Lat_Long = namedtuple('Lat_Long', ['latitude', 'longitude'])
    latitude, longitude = [], []
    for polyline in polylines:
        lat, lon = zip(*polyline)
        latitude += lat
        longitude += lon

    return Lat_Long(latitude, longitude)


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
