import pytest
import requests
import os
from weather_parse import coordinates, get_info


# @pytest.mark.skip("TODO")
def test_create():
    url = 'https://trip-bool.herokuapp.com/data/create'
    data = {
        "name": 'test@pytest.com',
        "start_date": '2022-06-28',
        "end_date": '2022-06-30',
        "location": 'Seattle'
    }
    actual = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    expected = 201
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_get_list():
    url = 'https://trip-bool.herokuapp.com/data'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_get_trip():
    url = 'https://trip-bool.herokuapp.com/data/87'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected



# @pytest.mark.skip("TODO")
def test_trip_update():
    url = 'https://trip-bool.herokuapp.com/data/87/update'
    data = {
        "name": "MichealMcDoesn'tExist@crmsnfker.com",
        "start_date": '2022-06-28',
        "end_date": '2022-06-30',
        "location": 'Moclips'
    }
    actual = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    expected = 201
    assert actual.status_code == expected


@pytest.mark.skip("Needs Additional Helper Code to Work")
def test_get_coords():
    actual = coordinates('Seattle')
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_yelp_resturaunts():
    url = 'https://trip-bool.herokuapp.com/yelp/restaurants/47.2330393/-124.2127184/2'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_yelp_hotels():
    url = 'https://trip-bool.herokuapp.com/yelp/hotels/47.2330393/-124.2127184/3'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_yelp_outdoors():
    url = 'https://trip-bool.herokuapp.com/yelp/outdoors/47.2330393/-124.2127184'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_weather_by_name():
    url = 'https://trip-bool.herokuapp.com/weather/test@pytest.com'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_weather_by_id():
    url = 'https://trip-bool.herokuapp.com/weather/88'
    actual = requests.get(url)
    expected = 200
    assert actual.status_code == expected


# @pytest.mark.skip("TODO")
def test_trip_delete():
    url = 'https://trip-bool.herokuapp.com/data/88/delete'
    actual = requests.post(url)
    expected = 410
    assert actual.status_code == expected


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

