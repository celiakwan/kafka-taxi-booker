from random import randint

THRESHOLD = 10000000

def _mock_coordinates(min, max):
    return randint(min * THRESHOLD, max * THRESHOLD) / THRESHOLD

def mock_latitude():
    return _mock_coordinates(20, 30)

def mock_longitude():
    return _mock_coordinates(50, 60)