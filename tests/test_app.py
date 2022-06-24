import pytest
import requests
import os
from weather_parse import coordinates, get_info

# @pytest.mark.skip("TODO")
# def test_coordinates_path():
#     location = "seattle"
#     location = location.replace(" ", "%20")
#     location_key = os.environ.get("LOCATIONIQ_KEY")
#     coordinates_url = f"https://us1.locationiq.com/v1/search?key={location_key}&q={location}&format=json"
#     coordinates_dict = get_info(coordinates_url)
#     actual = {
#         "lat": coordinates_dict[0]["lat"],
#         "lon": coordinates_dict[0]["lon"],
#     }
#     expected = {
#         "lat": "47.6038321",
#         "lon": "-122.3300624",
#     }
#     assert actual == expected

# @pytest.mark.skip("TODO")
def test_coordinates_path():

    assert actual == expected