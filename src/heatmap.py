import folium

from src.get_strava_data import get_activity_polylines


def create_map(center):
    """Creates base folium map.

    Args:
        center ([lat, long]): Coordinates for center of map.

    Returns:
        folium.Map object
    """
    strava_map = folium.Map(
        location=center,
        tiles='Cartodb dark_matter',
        zoom_start=12
    )
    return strava_map


def add_polyline(folium_map, polyline):
    """Adds polyline to base map.

    Args:
        folium_map (folium.Map): Map to add polyline to.
        polyline (str): Decoded polyline string.

    Returns:
        folium.Map object.
    """
    polyline = folium.PolyLine(
        locations=polyline,
        weight=2,
        opacity=0.4
    ).add_to(folium_map)
    return folium_map
