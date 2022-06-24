import pytest
import requests
from weather_parse import get_info, coordinates, current_weather, weather_time_machine, get_time_zone


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
# def test():
#     actual =
#     expected = 
#     assert actual == expected


# @pytest.mark.skip("TODO")
# def test():
#     actual =
#     expected = 
#     assert actual == expected.
