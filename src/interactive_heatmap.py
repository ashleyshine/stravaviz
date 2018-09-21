import folium

from src.get_strava_data import get_activity_polylines


def create_map(center, style):
    """Creates base folium map.

    Args:
        center ([lat, long]): Coordinates for center of map.
        style (str): Style of map - either 'dark' or 'light'.

    Returns:
        folium.Map object
    """
    tile_styles = {
        'dark': 'Cartodb dark_matter',
        'light': 'Cartodb positron'
    }

    strava_map = folium.Map(
        location=center,
        tiles=tile_styles[style],
        zoom_start=12
    )
    return strava_map


def add_polyline(folium_map, polyline, color='blue'):
    """Adds polyline to base map.

    Args:
        folium_map (folium.Map): Map to add polyline to.
        polyline (str): Decoded polyline string.
        color (str): Color of polyline.

    Returns:
        folium.Map object.
    """
    line_colors = {
        'blue': 'deepskyblue',
        'red': 'orangered'
    }

    polyline = folium.PolyLine(
        locations=polyline,
        weight=0.5,
        opacity=0.4,
        color=line_colors[color]
    ).add_to(folium_map)
    return folium_map


def create_heatmap(center, style='dark', color='blue', activity_params={}):
    """Create heatmap with activity polylines.

    Args:
        center ([lat, long]): Coordinates for center of map.
        style (str): Style of map. Either 'dark' or 'light'.
        color (str): Color of activity polylines. Either 'blue' or 'red.'
        activity_params (dict): Optional parameters for retrieved
            activities. Example below.
            {
                'after': '2017-01-01',
                'before': '2018-01-01',
                'limit': 100
            }

    Returns:
        folium.Map object
    """
    strava_map = create_map(center, style)
    polylines = get_activity_polylines(**activity_params)
    for polyline in polylines:
        add_polyline(strava_map, polyline, color)
    return strava_map
