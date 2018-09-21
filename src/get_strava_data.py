import logging

import polyline
import stravalib

import src.strava_config as strava_config

# Raise logger level since Strava frequently changes the structure of
# their models, resulting in (relatively harmless) warnings.
logger = logging.getLogger()
logger.setLevel('ERROR')


def create_client():
    """Creates client to interface with Strava API."""
    return stravalib.client.Client(strava_config.ACCESS_TOKEN)


def get_activity_polylines(before=None, after=None, limit=None):
    """Gets activity polylines for user.

    Args:
        before (datetime or str): Retrieve activities before this date.
            Format YYYY-MM-DD.
        after (datetime or str): Retrieve activities after this date.
            Format YYYY-MM-DD.
        limit (int): Maximum number of activities to return.

    Returns:
        A list of polyline strings
    """
    client = create_client()
    try:
        activities = client.get_activities(
            before=before, after=after, limit=limit
        )
        decoded_polylines = [
            polyline.decode(activity.map.summary_polyline)
            for activity in activities if activity.map.summary_polyline
        ]
        return decoded_polylines
    except stravalib.exc.AccessUnauthorized:
        print(
            "Invalid Strava access token. Set Strava access token " +
            "in strava_config.py."
        )
